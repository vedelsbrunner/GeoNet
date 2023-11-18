from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout


class CircularLayout(Layout):
    def do_layout(self, network: GeoNetwork, **kwargs):
        print("Creating circular layout")