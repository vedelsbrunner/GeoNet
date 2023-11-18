from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout


class StackedLayout(Layout):
    def do_layout(self, network: GeoNetwork):
        print("Creating stacked layout")