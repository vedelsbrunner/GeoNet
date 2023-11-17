import logging
import time

import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import Point, LineString

logging.basicConfig(level=logging.INFO)


class GeoNetwork:
    def __init__(self):
        self.gdf_points = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.gdf_lines = gpd.GeoDataFrame(columns=['id', 'geometry'])
        self.graph = nx.Graph()
        self.points_data = []
        self.lines_data = []

    def add_point(self, point_id, x, y, **properties):
        point = Point(x, y)
        self.points_data.append({'id': point_id, 'geometry': point, **properties})
        self.graph.add_node(point_id, pos=(x, y), **properties)

    def add_line(self, line_id, point_id_start, point_id_end, **properties):
        point_start = self.graph.nodes[point_id_start]['pos']
        point_end = self.graph.nodes[point_id_end]['pos']
        line = LineString([point_start, point_end])
        self.lines_data.append({'id': line_id, 'geometry': line, **properties})
        self.graph.add_edge(point_id_start, point_id_end, **properties)

    def finalize(self):
        points_df = pd.DataFrame(self.points_data)
        lines_df = pd.DataFrame(self.lines_data)

        points_df = points_df.drop_duplicates(subset='id')
        lines_df = lines_df.drop_duplicates(subset='id')

        self.gdf_points = gpd.GeoDataFrame(points_df, geometry='geometry')
        self.gdf_lines = gpd.GeoDataFrame(lines_df, geometry='geometry')

    # TODO: Verify that this works (!)
    def count_edge_crossings(self):
        start_time = time.time()
        self.finalize()
        crossings = 0
        line_geometries = self.gdf_lines['geometry'].tolist()

        for i in range(len(line_geometries)):
            for j in range(i + 1, len(line_geometries)):
                line1 = line_geometries[i]
                line2 = line_geometries[j]
                if line1.intersects(line2) and not line1.touches(line2):
                    crossings += 1

        elapsed_time = time.time() - start_time
        logging.info(f"Counted edge crossings in {elapsed_time:.2f} seconds.")
        return crossings

    def to_geojson(self):
        self.finalize()
        points_geojson = self.gdf_points.to_json()
        lines_geojson = self.gdf_lines.to_json()
        return points_geojson, lines_geojson
