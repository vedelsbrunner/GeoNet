from cluster.ClusteringStrategy import ClusteringStrategy
from graph.GeoNetwork import GeoNetwork


class DbscanClustering(ClusteringStrategy):
    def cluster(self, network: GeoNetwork, **kwargs):
        print("Clustering with DBSCAN")