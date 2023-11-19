from math import cos, sin, pi, sqrt

from geopy.distance import geodesic
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

                circle_center = cluster_points.geometry.unary_union.centroid

                for i, point in enumerate(cluster_points.itertuples()):
                    bearing = 360 / num_points * i
                    new_point = geodesic(kilometers=radius).destination((circle_center.y, circle_center.x), bearing)
                    network.update_point(point.id, new_point.longitude, new_point.latitude)
            else:
                logger.debug(f"Skipping cluster {cluster} because it has only one point")
