from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout


class GridLayout(Layout):
    def create_layout(self, network: GeoNetwork):
        print("Creating grid layout")