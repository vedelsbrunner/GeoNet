from cluster.ClusteringStrategy import ClusteringStrategy
from graph.GeoNetwork import GeoNetwork


class SamePositionClustering(ClusteringStrategy):
    def cluster(self, network: GeoNetwork, **kwargs):
        print("Clustering with same position")
