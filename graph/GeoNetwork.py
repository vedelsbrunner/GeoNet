import logging
import time

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from shapely.geometry import Point, LineString
from sklearn.cluster import DBSCAN

logging.basicConfig(level=logging.INFO)


class GeoNetwork:
    def __init__(self):
        self.__gdf_points = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__gdf_edges = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.__points_data = []
        self.__lines_data = []
        self.__point_to_edges = {}

        # // TODO: maybe private as well?
        self.graph = nx.Graph()

    def add_point(self, point_id, x, y, **properties):
        point = Point(x, y)
        self.__points_data.append({'id': point_id, 'geometry': point, **properties})
        self.graph.add_node(point_id, pos=(x, y), **properties)
        self.__point_to_edges[point_id] = []

    def add_line(self, line_id, point_id_start, point_id_end, **properties):
        point_start = self.graph.nodes[point_id_start]['pos']
        point_end = self.graph.nodes[point_id_end]['pos']
        line = LineString([point_start, point_end])
        self.__lines_data.append({'id': line_id, 'geometry': line, **properties})
        self.graph.add_edge(point_id_start, point_id_end, **properties)
        # Update the point_to_edges lookup
        self.__point_to_edges[point_id_start].append((line_id, point_id_end))
        self.__point_to_edges[point_id_end].append((line_id, point_id_start))

    def finalize(self):
        points_df = pd.DataFrame(self.__points_data)
        lines_df = pd.DataFrame(self.__lines_data)

        points_df = points_df.drop_duplicates(subset='id')
        lines_df = lines_df.drop_duplicates(subset='id')

        self.__gdf_points = gpd.GeoDataFrame(points_df, geometry='geometry')
        self.__gdf_edges = gpd.GeoDataFrame(lines_df, geometry='geometry')

    def update_point(self, point_id, new_x, new_y):
        # Update the position of a point and its associated lines
        self.graph.nodes[point_id]['pos'] = (new_x, new_y)
        self.__gdf_points.loc[self.__gdf_points['id'] == point_id, 'geometry'] = Point(new_x, new_y)

        for line_id, connected_point_id in self.__point_to_edges[point_id]:
            self.__update_line_geometry(line_id, point_id, connected_point_id)

    def write_to_disk(self, points_path, lines_path):
        self.__gdf_points.to_file(points_path, drive='GeoJSON')
        self.__gdf_edges.to_file(lines_path, driver='GeoJSON')

    def get_points(self):
        # Provide a copy of the points GeoDataFrame to avoid direct manipulation.
        return self.__gdf_points.copy()

    def set_clusters(self, clusters):
        # Update the GeoDataFrame with the cluster information.
        self.__gdf_points['cluster'] = clusters

    def __update_line_geometry(self, line_id, point_id_start, point_id_end):
        point_start_pos = self.graph.nodes[point_id_start]['pos']
        point_end_pos = self.graph.nodes[point_id_end]['pos']
        new_line_geom = LineString([point_start_pos, point_end_pos])
        self.__gdf_edges.loc[self.__gdf_edges['id'] == line_id, 'geometry'] = new_line_geom
