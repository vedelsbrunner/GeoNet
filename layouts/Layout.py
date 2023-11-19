from abc import ABC, abstractmethod

from graph.GeoNetwork import GeoNetwork
from utils.LoggerConfig import logger


class LayoutConfig(ABC):
    pass

class Layout(ABC):
    def __init__(self, clustering_strategy):
        if clustering_strategy is None:
            raise ValueError("Clustering strategy cannot be None")
        self.clustering_strategy = clustering_strategy

    def create_layout(self, network: GeoNetwork, config: LayoutConfig):
        self.clustering_strategy.cluster(network)
        logger.debug(f"Finished clustering network with {self.clustering_strategy.__class__.__name__}")
        self.do_layout(network, config)
        logger.debug(f"Finished layout {self.__class__.__name__}")
        return

    @abstractmethod
    def do_layout(self, network: GeoNetwork, config: LayoutConfig):
        pass
