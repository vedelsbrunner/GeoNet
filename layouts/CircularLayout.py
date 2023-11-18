from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout


class CircularLayout(Layout):
    def create_layout(self, network: GeoNetwork):
        print("Creating circular layout")