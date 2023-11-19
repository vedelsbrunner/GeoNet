from math import cos, sin, pi, sqrt, radians
from math import atan2, degrees

import numpy as np
from geopy.distance import geodesic, great_circle
from pyproj import Geod
from shapely import Point
import geopandas as gpd
from graph.GeoNetwork import GeoNetwork
from layouts.Layout import LayoutConfig, Layout
from utils.LoggerConfig import logger


class CircularLayoutConfig(LayoutConfig):
    def __init__(self, radius_scale: float):
        self.radius_scale = radius_scale


class CircularLayout(Layout):
    def __init__(self, clustering_strategy):
        super().__init__(clustering_strategy)
        self.cluster_radius = {}

    def do_layout(self, network: GeoNetwork, config: CircularLayoutConfig):
        # The base radius value can be set or calculated from the config
        base_radius = config.base_radius if hasattr(config, 'base_radius') else 1

        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)
            if num_points > 1:
                radius = base_radius * config.radius_scale * num_points
                self.cluster_radius[cluster] = radius

                circle_center = cluster_points.geometry.unary_union.centroid

                for i, point in enumerate(cluster_points.itertuples()):
                    bearing = 360 / num_points * i
                    new_point = geodesic(kilometers=radius).destination((circle_center.y, circle_center.x), bearing)
                    network.update_point(point.id, new_point.longitude, new_point.latitude)
            else:
                logger.debug(f"Skipping cluster {cluster} because it has only one point")

    def minimize_edge_crossings(self, network: GeoNetwork):
        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            logger.debug(f"Minimizing edge crossings for cluster {cluster}")

            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)
            if num_points > 1:
                radius = self.cluster_radius[cluster]
                circle_center = cluster_points.geometry.unary_union.centroid

                for point in cluster_points.itertuples():
                    neighbors = list(network.graph.neighbors(point.id))
                    if len(neighbors) > 0:
                        neighbor_coords = [network.graph.nodes[neighbor]['pos'] for neighbor in neighbors]
                        barycenter = np.mean(neighbor_coords, axis=0)

                        angle_to_barycenter = atan2(barycenter[1] - circle_center.y, barycenter[0] - circle_center.x)
                        angle_degrees = degrees(angle_to_barycenter)

                        new_point = geodesic(kilometers=radius).destination((circle_center.y, circle_center.x), angle_degrees)
                        network.update_point(point.id, new_point.longitude, new_point.latitude)

                    else:
                        logger.debug(f"Skipping point {point.id} because it has no neighbors")
                        continue
