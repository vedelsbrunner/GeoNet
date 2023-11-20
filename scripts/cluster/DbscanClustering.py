import numpy as np
from sklearn.cluster import DBSCAN

from scripts.cluster.ClusteringStrategy import ClusteringStrategy
from scripts.graph.GeoNetwork import GeoNetwork


class DbscanClustering(ClusteringStrategy):
    def __init__(self, eps=0.5, min_samples=1, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=None):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.metric_params = metric_params
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.n_jobs = n_jobs

    def cluster(self, network: GeoNetwork):
        coordinates = np.array([[point.x, point.y] for point in network.get_points().geometry])
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric=self.metric,
                    metric_params=self.metric_params, algorithm=self.algorithm,
                    leaf_size=self.leaf_size, p=self.p, n_jobs=self.n_jobs)
        labels = db.fit_predict(coordinates)
        network.set_clusters(labels)

        self.update_centroids(network, labels)

    def update_centroids(self, network, labels):
        points = network.get_points()
        points['cluster'] = labels
        for cluster_label in np.unique(labels):
            if cluster_label != -1:
                cluster_points = points[points['cluster'] == cluster_label]
                centroid = cluster_points.geometry.unary_union.centroid
                for point_id in cluster_points['id']:
                    network.update_point(point_id, centroid.x, centroid.y)
