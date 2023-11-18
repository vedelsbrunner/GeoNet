import numpy as np
from sklearn.cluster import DBSCAN

from cluster.ClusteringStrategy import ClusteringStrategy
from graph.GeoNetwork import GeoNetwork


class DbscanClustering(ClusteringStrategy):
    def __init__(self, eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=None):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.metric_params = metric_params
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.n_jobs = n_jobs

    def cluster(self, network: GeoNetwork):
        coordinates = np.array([[point.x, point.y] for point in network.__gdf_points.geometry])
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric=self.metric,
                    metric_params=self.metric_params, algorithm=self.algorithm,
                    leaf_size=self.leaf_size, p=self.p, n_jobs=self.n_jobs)
        labels = db.fit_predict(coordinates)
        network.__gdf_points['cluster'] = labels
