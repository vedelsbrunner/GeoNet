import logging
import random
from itertools import combinations
from multiprocessing import Pool

import geopandas as gpd
import networkx as nx
import pandas as pd
from pyproj import CRS
from shapely.geometry import Point, LineString

from scripts.utils.LoggerConfig import logger

logging.basicConfig(level=logging.INFO)


def check_crossings(pair):
    line1, line2 = pair
    return LineString(line1).crosses(LineString(line2))


class GeoNetwork:
    def __init__(self):
        self.__gdf_points = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__gdf_edges = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__points_data = []  # Only use for optimization purposes
        self.__lines_data = []  # Only use for optimization purposes
        self.__point_to_edges = {}
        # // TODO: maybe private as well?
        self.graph = nx.Graph()

    def add_point(self, point_id, x, y, **properties):
        point = Point(x, y)
        if point_id in self.graph:
            self.graph.nodes[point_id].update({'pos': (x, y), **properties})
            for point_data in self.__points_data:
                if point_data['id'] == point_id:
                    point_data.update({'geometry': point, **properties})
                    break
        else:
            self.__points_data.append({'id': point_id, 'geometry': point, **properties})
            self.graph.add_node(point_id, pos=(x, y), **properties)
            self.__point_to_edges[point_id] = []

    def add_line(self, line_id, point_id_start, point_id_end, **properties):
        if point_id_start not in self.graph or point_id_end not in self.graph:
            logger.warning(f"One or both points for the line {line_id} do not exist: {point_id_start}, {point_id_end}")
            return

        if self.graph.has_edge(point_id_start, point_id_end):
            self.graph[point_id_start][point_id_end].update(properties)
            for line_data in self.__lines_data:
                if line_data['id'] == line_id:
                    line_data.update(properties)
                    break
        else:
            point_start = self.graph.nodes[point_id_start]['pos']
            point_end = self.graph.nodes[point_id_end]['pos']
            line = LineString([point_start, point_end])
            self.__lines_data.append({'id': line_id, 'geometry': line, **properties})
            self.graph.add_edge(point_id_start, point_id_end, **properties)
            self.__point_to_edges[point_id_start].append((line_id, point_id_end))
            self.__point_to_edges[point_id_end].append((line_id, point_id_start))

    # TODO: Ugly post-processing, refactor(!)
    def finalize(self, crs="EPSG:32633"):
        points_df = pd.DataFrame(self.__points_data)
        lines_df = pd.DataFrame(self.__lines_data)

        assert points_df['id'].nunique() == self.graph.number_of_nodes(), "Mismatch in number of points"
        assert lines_df['id'].nunique() == self.graph.number_of_edges(), "Mismatch in number of lines"

        degrees = dict(self.graph.degree())
        points_df['degree'] = points_df['id'].apply(lambda x: degrees.get(x, 0))

        closeness = nx.closeness_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph)

        points_df['closeness_centrality'] = points_df['id'].apply(lambda x: closeness.get(x, 0)).round(2)
        points_df['betweenness_centrality'] = points_df['id'].apply(lambda x: betweenness.get(x, 0)).round(2)

        crs_object = CRS(crs)
        self.__gdf_points = gpd.GeoDataFrame(points_df, geometry='geometry', crs=crs_object)
        self.__gdf_edges = gpd.GeoDataFrame(lines_df, geometry='geometry', crs=crs_object)

    def update_point(self, point_id, new_x, new_y):
        self.graph.nodes[point_id]['pos'] = (new_x, new_y)
        self.__gdf_points.loc[self.__gdf_points['id'] == point_id, 'geometry'] = Point(new_x, new_y)

        for line_id, connected_point_id in self.__point_to_edges[point_id]:
            self.__update_line_geometry(line_id, point_id, connected_point_id)

    def write_to_disk(self, output_path):
        combined_gdf = gpd.GeoDataFrame(pd.concat([self.__gdf_points, self.__gdf_edges], ignore_index=True))
        combined_gdf.to_file(output_path, driver='GeoJSON')

    def get_points(self):
        return self.__gdf_points.copy()

    def set_clusters(self, clusters):
        self.__gdf_points['cluster'] = clusters

    def __update_line_geometry(self, line_id, point_id_start, point_id_end):
        point_start_pos = self.graph.nodes[point_id_start]['pos']
        point_end_pos = self.graph.nodes[point_id_end]['pos']
        new_line_geom = LineString([point_start_pos, point_end_pos])
        self.__gdf_edges.loc[self.__gdf_edges['id'] == line_id, 'geometry'] = new_line_geom

    def update_point_properties(self, point_id, **properties):
        if point_id in self.graph:
            # Update the node properties in the graph
            for key, value in properties.items():
                self.graph.nodes[point_id][key] = value

            for key, value in properties.items():
                self.__gdf_points.loc[self.__gdf_points['id'] == point_id, key] = value
        else:
            logging.warning(f"Point with ID {point_id} not found in the graph.")

    def add_point_props(self, point_id, **props):
        if point_id not in self.graph:
            logging.warning(f"Point with ID {point_id} does not exist.")
            return

        for key, value in props.items():
            self.graph.nodes[point_id][key] = value

        if self.__gdf_points['id'].isin([point_id]).any():
            for key, value in props.items():
                self.__gdf_points.loc[self.__gdf_points['id'] == point_id, key] = value
        else:
            logging.warning(f"Point with ID {point_id} not found in GeoDataFrame.")

    def calculate_total_edge_crossings(self):
        edges = list(self.graph.edges())
        lines = [(self.graph.nodes[edge[0]]['pos'], self.graph.nodes[edge[1]]['pos']) for edge in edges]
        pairs = list(combinations(lines, 2))

        with Pool() as pool:
            results = pool.map(check_crossings, pairs)

        total_crossings = sum(results)
        logger.debug(f"Total edge crossings: {total_crossings}")
        return total_crossings


    # Used for the CircularLayout TODO: Move to CircularLayout
    def are_connections_internal(self, point_id):
        point_cluster = self.__gdf_points.loc[self.__gdf_points['id'] == point_id, 'cluster'].values[0]
        connected_points = [edge[1] for edge in self.__point_to_edges[point_id]]

        for connected_point_id in connected_points:
            connected_point_cluster = self.__gdf_points.loc[self.__gdf_points['id'] == connected_point_id, 'cluster'].values[0]
            if connected_point_cluster != point_cluster:
                return False
        return True

    # TODO: Remove - only used for testing
    def create_fixed_clusters(self, seed=42):
        random.seed(seed)

        cluster_positions = {
            'cluster_20': (2.3522, 48.8566),  # Coords for Paris, for example
            'cluster_10': (3.8767, 43.6112),  # Coords for Montpellier
            'cluster_5': (-1.6793, 48.1173),  # Coords for Rennes
        }

        cluster_sizes = {'cluster_20': 20, 'cluster_10': 10, 'cluster_5': 5}
        for cluster_name, (lon, lat) in cluster_positions.items():
            for i in range(cluster_sizes[cluster_name]):
                point_id = f'{cluster_name}_point_{i}'
                self.add_point(point_id, lon, lat)

        all_points = list(self.graph.nodes)
        num_lines = 50
        for i in range(num_lines):
            point_id_start, point_id_end = random.sample(all_points, 2)
            line_id = f'line_{i}'
            self.add_line(line_id, point_id_start, point_id_end)

    def swap_nodes(self, node1_id, node2_id):
        if node1_id not in self.graph or node2_id not in self.graph:
            logger.warning(f"One or both nodes to swap do not exist: {node1_id}, {node2_id}")
            return False

        node1_pos = self.graph.nodes[node1_id]['pos']
        node2_pos = self.graph.nodes[node2_id]['pos']
        self.graph.nodes[node1_id]['pos'], self.graph.nodes[node2_id]['pos'] = node2_pos, node1_pos

        self.__gdf_points.loc[self.__gdf_points['id'] == node1_id, 'geometry'] = Point(node2_pos)
        self.__gdf_points.loc[self.__gdf_points['id'] == node2_id, 'geometry'] = Point(node1_pos)

        for line_id, connected_point_id in self.__point_to_edges[node1_id]:
            self.__update_line_geometry(line_id, node1_id, connected_point_id)
        for line_id, connected_point_id in self.__point_to_edges[node2_id]:
            self.__update_line_geometry(line_id, node2_id, connected_point_id)

        return True
