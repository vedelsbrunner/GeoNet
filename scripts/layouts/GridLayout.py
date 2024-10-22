import math

from geopy.distance import geodesic
from shapely.geometry import Point

from scripts.layouts import GridLayoutConfig
from scripts.layouts.Layout import Layout
from scripts.utils.LoggerConfig import logger


class GridLayout(Layout):
    def __init__(self, clustering_strategy):
        super().__init__(clustering_strategy)

    def do_layout(self, network, config: GridLayoutConfig):
        logger.debug(f"Creating grid layout with {config.distance_between_points} distance between the points")

        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)
            if num_points <= 1:
                logger.debug("Skipping cluster with only one point")
                continue

            cluster_points = cluster_points.sort_values(by='degree', ascending=False)

            grid_center = cluster_points.geometry.unary_union.centroid
            grid_size = math.ceil(math.sqrt(num_points))

            for i, point in enumerate(cluster_points.itertuples()):
                dx, dy = i % grid_size, i // grid_size
                new_point = geodesic(kilometers=dx * config.distance_between_points).destination((grid_center.y, grid_center.x), bearing=90)
                new_point = geodesic(kilometers=dy * config.distance_between_points).destination((new_point.latitude, new_point.longitude), bearing=0)
                network.update_point(point.id, new_point.longitude, new_point.latitude)
