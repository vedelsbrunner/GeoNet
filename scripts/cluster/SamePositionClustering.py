from scripts.cluster.ClusteringStrategy import ClusteringStrategy
from scripts.graph.GeoNetwork import GeoNetwork


class SamePositionClustering(ClusteringStrategy):
    def cluster(self, network: GeoNetwork):
        clusters = network.get_points().groupby('geometry').ngroup()
        network.set_clusters(clusters)