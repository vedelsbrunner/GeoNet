from abc import ABC, abstractmethod

from scripts.graph.GeoNetwork import GeoNetwork


class ClusteringStrategy(ABC):
    @abstractmethod
    def cluster(self, network: GeoNetwork):
        pass