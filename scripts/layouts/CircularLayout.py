import math
from math import pi, radians

from geopy.distance import geodesic

from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
from scripts.layouts.Layout import Layout
from scripts.utils.LoggerConfig import logger
from math import sqrt, pi, cos, sin


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
        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)
            cluster_points = cluster_points.sort_values(by='degree', ascending=False)

            if num_points > 1:
                if config.layout_type == CircularLayoutType.SINGLE_CIRCLE:
                    self.place_nodes_single_circle(network, cluster_points, config)
                    network.add_point_gdf(f'{cluster}_circle_hull_radius', self.cluster_info[cluster]['center'][0], self.cluster_info[cluster]['center'][1], radius=self.cluster_info[cluster]['radius'], cluster=cluster)
                elif config.layout_type == CircularLayoutType.DOUBLE_CIRCLE:
                    self.place_nodes_double_circle(network, cluster_points, config)
                    network.add_point_gdf(f'{cluster}_circle_hull_radius', self.cluster_info[cluster]['center'][0], self.cluster_info[cluster]['center'][1], radius=self.cluster_info[cluster]['outer_radius'], cluster=cluster)
                else:
                    logger.error("Wrong CircularLayoutType selected")

                logger.info(f"Placed nodes for cluster {cluster}.")

    def place_nodes_double_circle(self, network, cluster_points, config):
        inner_points = [p.id for p in cluster_points.itertuples() if network.are_connections_internal(p.id)]
        outer_points = [p.id for p in cluster_points.itertuples() if p.id not in inner_points]

        circle_center = cluster_points.geometry.unary_union.centroid

        inner_circumference = len(inner_points) * config.min_distance_between_nodes_km
        inner_radius = inner_circumference / (2 * pi)

        if outer_points:
            outer_circumference = len(outer_points) * config.min_distance_between_nodes_km
            outer_radius = outer_circumference / (2 * pi)

            # Check for edge case where inner circle has more points than the outer
            if len(inner_points) > len(outer_points):
                outer_radius = inner_radius + config.min_distance_between_nodes_km * 2

            place_nodes_on_circle(network, outer_points, circle_center, outer_radius)
        else:
            # If there are no outer points, outer_radius is not defined
            outer_radius = inner_radius

        place_nodes_on_circle(network, inner_points, circle_center, inner_radius)

        self.cluster_info[cluster_points['cluster'].iloc[0]] = {
            'inner_radius': inner_radius,
            'outer_radius': outer_radius if outer_radius is not None else 'N/A',
            'center': (circle_center.x, circle_center.y)
        }

    def place_nodes_single_circle(self, network, cluster_points, config):

        num_points = len(cluster_points)
        circle_center = cluster_points.geometry.unary_union.centroid

        circumference = num_points * config.min_distance_between_nodes_km
        radius = circumference / (2 * pi)

        for i, point in enumerate(cluster_points.itertuples()):
            bearing = 360 * i / num_points
            new_point = geodesic(kilometers=radius).destination((circle_center.y, circle_center.x), bearing)
            network.update_point(point.id, new_point.longitude, new_point.latitude)

        self.cluster_info[cluster_points['cluster'].iloc[0]] = {'radius': radius, 'center': (circle_center.x, circle_center.y)}
