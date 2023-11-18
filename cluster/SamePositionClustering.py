from cluster.ClusteringStrategy import ClusteringStrategy
from graph.GeoNetwork import GeoNetwork


class SamePositionClustering(ClusteringStrategy):
    def cluster(self, network: GeoNetwork, **kwargs):
        network.gdf_points['cluster'] = network.gdf_points.groupby('geometry').ngroup()