from abc import ABC, abstractmethod

from graph.GeoNetwork import GeoNetwork


class Layout(ABC):
    def __init__(self, clustering_strategy):
        if clustering_strategy is None:
            raise ValueError("Clustering strategy cannot be None")
        self.clustering_strategy = clustering_strategy

    def create_layout(self, network: GeoNetwork):
        self.clustering_strategy.cluster(network)
        return self.do_layout(network)

    @abstractmethod
    def do_layout(self, network: GeoNetwork):
        pass
