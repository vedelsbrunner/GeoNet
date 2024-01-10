from math import sqrt
from geopy.distance import geodesic
import random

from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig
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
        self.cluster_radius = {}
        self.outer_nodes = {}

    def do_layout(self, network, config: CircularLayoutConfig):
        base_radius = getattr(config, 'base_radius', 1)
        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]
            num_points = len(cluster_points)

            cluster_points = cluster_points.sort_values(by='degree', ascending=False)

            if num_points > 1:
                radius = base_radius * config.radius_scale * sqrt(num_points)
                circle_center = cluster_points.geometry.unary_union.centroid
                self.cluster_radius[cluster] = {'radius': radius, 'center': (circle_center.x, circle_center.y)}
                outer_nodes = place_nodes(network, cluster_points, circle_center, radius, config)
                self.outer_nodes[cluster] = outer_nodes
                logger.info(f"Placed nodes for cluster {cluster} with radius {radius}.")

    def optimize_layout(self, network, max_iterations_per_cluster=100, improvement_threshold=20):
        clusters = self.sort_clusters_by_size(network)
        for i in range(1, 50):
            logger.info(f"Starting optimization round {i}.")
            for cluster in clusters:
                logger.info(f"Starting optimization for cluster {cluster}.")
                self.reduce_edge_crossings(network, cluster, max_iterations_per_cluster, improvement_threshold)

    def sort_clusters_by_size(self, network):
        cluster_sizes = network.get_points().groupby('cluster').size()
        sorted_clusters = cluster_sizes.sort_values(ascending=False).index.tolist()
        return sorted_clusters

    def reduce_edge_crossings(self, network, cluster, max_iterations, improvement_threshold):
        logger.debug(f"Trying to reduce edge crossing: Improvemnet threshold: {improvement_threshold}")
        if cluster not in self.outer_nodes or len(self.outer_nodes[cluster]) < 2:
            logger.warn(f"Cluster {cluster} does not have enough nodes for optimization.")
            return

        best_crossings = network.calculate_total_edge_crossings()
        iterations_since_last_improvement = 0

        for iteration in range(max_iterations):
            if iterations_since_last_improvement >= improvement_threshold:
                logger.info(f"No improvement for {improvement_threshold} iterations, stopping optimization for cluster {cluster}.")
                break

            node1_id, node2_id = self.select_random_outer_nodes(cluster)
            if not node1_id or not node2_id:
                logger.info(f"Not enough outer nodes to perform a swap in cluster {cluster}.")
                break

            network.swap_nodes(node1_id, node2_id)
            current_crossings = network.calculate_total_edge_crossings()
            if current_crossings < best_crossings:
                best_crossings = current_crossings
                iterations_since_last_improvement = 0
                logger.debug(f"Improved layout for cluster {cluster}, reduced crossings to {current_crossings}.")
            else:
                network.swap_nodes(node1_id, node2_id)  # Revert the swap
                iterations_since_last_improvement += 1

    def select_random_outer_nodes(self, cluster):
        try:
            node1_id, node2_id = random.sample(self.outer_nodes[cluster], 2)
            return node1_id, node2_id
        except ValueError:
            logger.error(f"Not enough outer nodes in cluster {cluster} to select a random pair.")
            return None, None
