import logging
from itertools import combinations
from multiprocessing import Pool
import itertools
import numpy as np
from shapely.affinity import translate

import geopandas as gpd
import networkx as nx
import pandas as pd
from pyproj import CRS
from shapely.geometry import Point, LineString
from shapely.ops import unary_union

from scripts.mtv.mtv_helpers import check_crossings, hulls_overlap, calculate_mtv
from scripts.utils.LoggerConfig import logger

logging.basicConfig(level=logging.INFO)


class GeoNetwork:
    def __init__(self):
        self.gdf_points = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.gdf_edges = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.gdf_hulls = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__gdf_labels = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__points_data = []  # Only use for optimization purposes
        self.__lines_data = []  # Only use for optimization purposes
        self.__point_to_edges = {}
        # // TODO: maybe private as well?
        self.graph = nx.Graph()

    def add_neighbors_and_edges(self):
        self.gdf_points['neighbors'] = None
        self.gdf_points['connecting_edges'] = None
        for index, row in self.gdf_points.iterrows():
            point_id = row['id']
            neighbor_ids = list(self.graph.neighbors(point_id))
            connecting_edges = []
            connecting_edges.append([tup[0] for tup in self.__point_to_edges[point_id]])
            self.gdf_points.at[index, 'neighbors'] = neighbor_ids
            self.gdf_points.at[index, 'connecting_edges'] = list(itertools.chain(*connecting_edges))

    def add_point_gdf(self, point_id, x, y, **properties):
        point_geom = Point(x, y)

        if self.gdf_points['id'].isin([point_id]).any():
            logger.warning(f"Point with ID {point_id} already exists in gdf_points.")
            return

        new_row = {'id': point_id, 'geometry': point_geom, **properties}
        self.gdf_points = self.gdf_points._append(new_row, ignore_index=True)

        if point_id not in self.graph:
            self.graph.add_node(point_id, pos=(x, y), **properties)
            self.__point_to_edges[point_id] = []

        for connected_point_id in self.graph.neighbors(point_id):
            self.__update_line_geometry(f'{point_id}_{connected_point_id}', point_id, connected_point_id)

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

    def create_convex_hulls(self, buffer_distance=0.06):
        hulls_data = []

        for cluster_id, points in self.gdf_points.groupby('cluster'):
            if cluster_id == -1:
                logger.error(f"Skipping cluster with ID {cluster_id} (noise)")
                continue

            if not points.empty:
                buffered_points = points.buffer(buffer_distance)
                hull = unary_union(buffered_points).convex_hull
                hulls_data.append({'cluster_id': cluster_id, 'geometry': hull})

        self.gdf_hulls = gpd.GeoDataFrame(hulls_data, crs=self.gdf_points.crs)


    # TODO: Ugly post-processing, refactor(!)
    def finalize(self, crs="EPSG:32633"):
        points_df = pd.DataFrame(self.__points_data)
        lines_df = pd.DataFrame(self.__lines_data)

        assert points_df['id'].nunique() == self.graph.number_of_nodes(), "Mismatch in number of points"
        assert lines_df['id'].nunique() == self.graph.number_of_edges(), "Mismatch in number of lines"

        degrees = dict(self.graph.degree())
        points_df['degree'] = points_df['id'].apply(lambda x: degrees.get(x, 0))

        crs_object = CRS(crs)
        self.gdf_points = gpd.GeoDataFrame(points_df, geometry='geometry', crs=crs_object)
        self.gdf_edges = gpd.GeoDataFrame(lines_df, geometry='geometry', crs=crs_object)

    def update_point(self, point_id, new_x, new_y):
        self.graph.nodes[point_id]['pos'] = (new_x, new_y)
        self.gdf_points.loc[self.gdf_points['id'] == point_id, 'geometry'] = Point(new_x, new_y)

        for line_id, connected_point_id in self.__point_to_edges[point_id]:
            self.__update_line_geometry(line_id, point_id, connected_point_id)

    def write_to_disk(self, output_path, include_hulls=False, include_labels=False):
        gdf_points_copy = self.gdf_points.copy()
        gdf_edges_copy = self.gdf_edges.copy()
        gdf_hulls_copy = self.gdf_hulls.copy() if include_hulls else None
        gdf_labels_copy = self.__gdf_labels.copy() if include_labels else None

        gdf_points_copy['neighbors'] = gdf_points_copy['neighbors'].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
        gdf_points_copy['connecting_edges'] = gdf_points_copy['connecting_edges'].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)


        if 'geometry' in gdf_points_copy.columns:
            gdf_points_copy['longitude'] = gdf_points_copy.geometry.apply(lambda geom: geom.y) #No suer if geom.y is long or lat..

        # Sort by 'cluster', 'degree', and then 'longitude' --> TODO: Only relevant for the stacked layout..
        if 'cluster' in gdf_points_copy.columns and 'degree' in gdf_points_copy.columns and 'longitude' in gdf_points_copy.columns:
            gdf_points_copy.sort_values(by=['cluster', 'degree', 'longitude'], ascending=[True, False, True], inplace=True)

        dfs_to_combine = [gdf_points_copy, gdf_edges_copy]

        if include_hulls:
            if 'cluster_id' in gdf_hulls_copy.columns and 'id' not in gdf_hulls_copy.columns:
                gdf_hulls_copy.rename(columns={'cluster_id': 'id'}, inplace=True)
            dfs_to_combine.append(gdf_hulls_copy)

        if include_labels:
            if 'text' not in gdf_labels_copy.columns:
                logger.warning("Text labels are not available to include.")
            else:
                dfs_to_combine.append(gdf_labels_copy)

        combined_gdf = gpd.GeoDataFrame(pd.concat(dfs_to_combine, ignore_index=True))
        combined_gdf.to_file(output_path, driver='GeoJSON')
        logger.info(f"GeoNetwork data written to {output_path}{' with hulls' if include_hulls else ''}{' and labels' if include_labels else ''}")

    def get_points(self):
        return self.gdf_points.copy()

    def set_clusters(self, clusters):
        self.gdf_points['cluster'] = clusters

    def __update_line_geometry(self, line_id, point_id_start, point_id_end):
        point_start_pos = self.graph.nodes[point_id_start]['pos']
        point_end_pos = self.graph.nodes[point_id_end]['pos']
        new_line_geom = LineString([point_start_pos, point_end_pos])
        self.gdf_edges.loc[self.gdf_edges['id'] == line_id, 'geometry'] = new_line_geom

    def update_point_properties(self, point_id, **properties):
        if point_id in self.graph:
            for key, value in properties.items():
                self.graph.nodes[point_id][key] = value

            for key, value in properties.items():
                self.gdf_points.loc[self.gdf_points['id'] == point_id, key] = value
        else:
            logging.warning(f"Point with ID {point_id} not found in the graph.")

    def add_point_props(self, point_id, **props):
        if point_id not in self.graph:
            logging.warning(f"Point with ID {point_id} does not exist.")
            return

        for key, value in props.items():
            self.graph.nodes[point_id][key] = value

        if self.gdf_points['id'].isin([point_id]).any():
            for key, value in props.items():
                self.gdf_points.loc[self.gdf_points['id'] == point_id, key] = value
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
        point_cluster = self.gdf_points.loc[self.gdf_points['id'] == point_id, 'cluster'].values[0]
        connected_points = [edge[1] for edge in self.__point_to_edges[point_id]]

        for connected_point_id in connected_points:
            connected_point_cluster = self.gdf_points.loc[self.gdf_points['id'] == connected_point_id, 'cluster'].values[0]
            if connected_point_cluster != point_cluster:
                return False
        return True

    def swap_nodes(self, node1_id, node2_id):
        if node1_id not in self.graph or node2_id not in self.graph:
            logger.warning(f"One or both nodes to swap do not exist: {node1_id}, {node2_id}")
            return False

        node1_pos = self.graph.nodes[node1_id]['pos']
        node2_pos = self.graph.nodes[node2_id]['pos']
        self.graph.nodes[node1_id]['pos'], self.graph.nodes[node2_id]['pos'] = node2_pos, node1_pos

        self.gdf_points.loc[self.gdf_points['id'] == node1_id, 'geometry'] = Point(node2_pos)
        self.gdf_points.loc[self.gdf_points['id'] == node2_id, 'geometry'] = Point(node1_pos)

        for line_id, connected_point_id in self.__point_to_edges[node1_id]:
            self.__update_line_geometry(line_id, node1_id, connected_point_id)
        for line_id, connected_point_id in self.__point_to_edges[node2_id]:
            self.__update_line_geometry(line_id, node2_id, connected_point_id)

        return True

    def resolve_overlaps(self, max_iterations=10):
        logger.info("Resolving hull overlaps")
        iteration = 0
        overlapping = True

        while overlapping and iteration < max_iterations:
            overlapping = False
            hull_pairs_to_check = list(combinations(range(len(self.gdf_hulls)), 2))

            for idx1, idx2 in hull_pairs_to_check:
                hull1 = self.gdf_hulls.iloc[idx1]['geometry']
                hull2 = self.gdf_hulls.iloc[idx2]['geometry']
                if hulls_overlap(hull1, hull2):
                    overlapping = True
                    mtv = calculate_mtv(hull1, hull2)
                    if mtv is not None:
                        translation_vector_1 = (-mtv / 2) - np.array([0.01, 0.01])
                        translation_vector_2 = (mtv / 2) + np.array([0.01, 0.01])

                        cluster_id_1 = self.gdf_hulls.iloc[idx1]['cluster_id']
                        cluster_id_2 = self.gdf_hulls.iloc[idx2]['cluster_id']
                        self.apply_translation_to_cluster(cluster_id_1, translation_vector_1)
                        self.apply_translation_to_cluster(cluster_id_2, translation_vector_2)

            iteration += 1
            logger.debug(f"Completed iteration {iteration}")

        if iteration == max_iterations:
            logger.warning("Max iterations reached, there might still be overlaps.")

    def apply_translation_to_cluster(self, cluster_id, translation_vector):
        points_in_cluster = self.gdf_points[self.gdf_points['cluster'] == cluster_id]
        for point_id in points_in_cluster['id']:
            point = self.gdf_points.loc[self.gdf_points['id'] == point_id, 'geometry'].iloc[0]
            translated_point = translate(point, xoff=translation_vector[0], yoff=translation_vector[1])
            self.update_point(point_id, translated_point.x, translated_point.y)

        # Apply the same translation to the hull
        hull_index = self.gdf_hulls[self.gdf_hulls['cluster_id'] == cluster_id].index[0]
        hull = self.gdf_hulls.loc[hull_index, 'geometry']
        translated_hull = translate(hull, xoff=translation_vector[0], yoff=translation_vector[1])
        self.gdf_hulls.at[hull_index, 'geometry'] = translated_hull

        # Apply the same translation to the

    def print_network_summary(self):
        num_nodes = self.gdf_points.count()[0]
        num_edges = self.gdf_edges.count()[0]
        logger.info("This graph as {} nodes and {} edges.".format(num_nodes, num_edges))
    def create_text_labels(self):
        self.__gdf_labels = gpd.GeoDataFrame(columns=['id', 'geometry', 'text'])

        cluster_locations = self.gdf_points.groupby('cluster')['location'].apply(set)


        labels = []
        for cluster_id, locations in cluster_locations.items():
            if cluster_id == -1:
                logger.info(f"Skipping cluster with ID {cluster_id} (noise)")
                continue

            if 'nan' in str(locations):
                logger.error('TODO: Handle nan cluster / location, why are u here?')
                continue

            # Enable if u want to use the centroid for text positon
            #points_in_cluster = self.gdf_points[self.gdf_points['cluster'] == cluster_id]
            # centroid = points_in_cluster.unary_union.centroid

            cluster_hull = self.gdf_hulls.loc[self.gdf_hulls['cluster_id'] == cluster_id, 'geometry'].values[0]
            southernmost_point = min(cluster_hull.exterior.coords, key=lambda p: p[1])
            min_x, max_x = cluster_hull.bounds[0], cluster_hull.bounds[2]
            label_x = (min_x + max_x) / 2
            label_y = southernmost_point[1]
            label_geom = Point(label_x, label_y)

            location_string = "\n".join(map(str, locations))
            labels.append({
                'id': f"location_label'{cluster_id}",
                'geometry': label_geom,
                'text': location_string
            })

        self.__gdf_labels = gpd.GeoDataFrame(labels, crs=self.gdf_points.crs)

