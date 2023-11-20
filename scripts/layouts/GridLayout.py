from scripts.graph.GeoNetwork import GeoNetwork
from scripts.layouts.Layout import Layout


class GridLayout(Layout):
    def create_layout(self, network: GeoNetwork):
        print("Creating grid layout")