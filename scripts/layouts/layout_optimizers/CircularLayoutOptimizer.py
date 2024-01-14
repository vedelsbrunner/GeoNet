from scripts.layouts.CircularLayout import CircularLayout
from scripts.utils.LoggerConfig import logger

#TODO: Improve inheritance, I think this is broken


class CircularLayoutOptimizer(CircularLayout):
    def __init__(self, clustering_strategy):
        super().__init__(clustering_strategy)

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
