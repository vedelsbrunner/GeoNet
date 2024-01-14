from math import sqrt, pi, cos, sin
from geopy.distance import geodesic
import random

from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
from scripts.layouts.Layout import Layout
from scripts.utils.LoggerConfig import logger


def place_nodes_on_circle(network, nodes, center, radius):
    for i, node_id in enumerate(nodes):
        bearing = 360 / len(nodes) * i
        new_point = geodesic(kilometers=radius).destination((center.y, center.x), bearing)
        network.update_point(node_id, new_point.longitude, new_point.latitude)


def place_nodes(network, cluster_points, circle_center, radius, config):
    inner_radius = radius * config.inner_radius_scale
    inner_points = [p.id for p in cluster_points.itertuples() if network.are_connections_internal(p.id)]
    outer_points = [p.id for p in cluster_points.itertuples() if p.id not in inner_points]
    place_nodes_on_circle(network, inner_points, circle_center, inner_radius)
    place_nodes_on_circle(network, outer_points, circle_center, radius)
    return outer_points


class CircularLayout(Layout):
    def __init__(self, clustering_strategy):
        super().__init__(clustering_strategy)
        self.cluster_info = {}

    def do_layout(self, network, config: CircularLayoutConfig):
        base_radius = getattr(config, 'base_radius', 1)
        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)
            cluster_points = cluster_points.sort_values(by='degree', ascending=False)

            if num_points > 1:
                if config.layout_type == CircularLayoutType.SINGLE_CIRCLE:
                    self.place_nodes_single_circle(network, cluster_points, config)
                logger.info(f"Placed nodes for cluster {cluster}.")

    def place_nodes_single_circle(self, network, cluster_points, config):
        num_points = len(cluster_points)
        circle_center = cluster_points.geometry.unary_union.centroid

        # Calculate the distance between nodes along the circle's circumference
        circumference = num_points * config.min_distance_between_nodes
        radius = circumference / (2 * pi)

        for i, point in enumerate(cluster_points.itertuples()):
            # Calculate the bearing for each node on the circle
            bearing = 360 * i / num_points
            # Use geodesic to find the new point on the circle
            new_point = geodesic(kilometers=radius).destination((circle_center.y, circle_center.x), bearing)
            # Update the point in the network with the new coordinates
            network.update_point(point.id, new_point.longitude, new_point.latitude)

        self.cluster_info[cluster_points['cluster'].iloc[0]] = {'radius': radius, 'center': (circle_center.x, circle_center.y)}

