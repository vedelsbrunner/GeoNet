from abc import ABC, abstractmethod

from graph.GeoNetwork import GeoNetwork


class ClusteringStrategy(ABC):
    @abstractmethod
    def cluster(self, network: GeoNetwork, **kwargs):
        pass