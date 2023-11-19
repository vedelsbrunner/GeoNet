import logging
import time

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from pyproj import CRS
from shapely.geometry import Point, LineString
from sklearn.cluster import DBSCAN

from utils.LoggerConfig import logger

logging.basicConfig(level=logging.INFO)

class GeoNetwork:
    def __init__(self):
        self.__gdf_points = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__gdf_edges = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__points_data = [] # Only use for optimization purposes
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

    def finalize(self, crs="EPSG:32633"): #TODO: Ugly work around
        points_df = pd.DataFrame(self.__points_data)
        lines_df = pd.DataFrame(self.__lines_data)

        # Assert that the number of nodes and edges matches
        assert points_df['id'].nunique() == self.graph.number_of_nodes(), "Mismatch in number of points"
        assert lines_df['id'].nunique() == self.graph.number_of_edges(), "Mismatch in number of lines"

        # Compute the degree for each node (point) in the NetworkX graph
        degrees = dict(self.graph.degree())
        # Add a 'degree' column to the points DataFrame
        points_df['degree'] = points_df['id'].apply(lambda x: degrees.get(x, 0))

        closeness = nx.closeness_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph)

        # Add 'closeness_centrality' and 'betweenness_centrality' columns to the points DataFrame
        points_df['closeness_centrality'] = points_df['id'].apply(lambda x: closeness.get(x, 0))
        points_df['betweenness_centrality'] = points_df['id'].apply(lambda x: betweenness.get(x, 0))


        # Create the GeoNetwork as dataframes using the same crs
        crs_object = CRS(crs)
        self.__gdf_points = gpd.GeoDataFrame(points_df, geometry='geometry', crs=crs_object)
        self.__gdf_edges = gpd.GeoDataFrame(lines_df, geometry='geometry', crs=crs_object)

    def update_point(self, point_id, new_x, new_y):
        self.graph.nodes[point_id]['pos'] = (new_x, new_y)
        self.__gdf_points.loc[self.__gdf_points['id'] == point_id, 'geometry'] = Point(new_x, new_y)

        for line_id, connected_point_id in self.__point_to_edges[point_id]:
            self.__update_line_geometry(line_id, point_id, connected_point_id)

    def write_to_disk(self, points_path, lines_path):
        self.__gdf_points.to_file(points_path, drive='GeoJSON')
        self.__gdf_edges.to_file(lines_path, driver='GeoJSON')

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
        # Check if the point exists in the graph
        if point_id in self.graph:
            # Update the node properties in the graph
            for key, value in properties.items():
                self.graph.nodes[point_id][key] = value

            # Update the properties in the points GeoDataFrame
            for key, value in properties.items():
                self.__gdf_points.loc[self.__gdf_points['id'] == point_id, key] = value
        else:
            logging.warning(f"Point with ID {point_id} not found in the graph.")


    def add_point_props(self, point_id, **props):
        if point_id not in self.graph:
            logging.warning(f"Point with ID {point_id} does not exist.")
            return

        # Update properties in the networkx graph node
        for key, value in props.items():
            self.graph.nodes[point_id][key] = value

        # Update properties in the GeoDataFrame
        if self.__gdf_points['id'].isin([point_id]).any():
            for key, value in props.items():
                self.__gdf_points.loc[self.__gdf_points['id'] == point_id, key] = value
        else:
            logging.warning(f"Point with ID {point_id} not found in GeoDataFrame.")