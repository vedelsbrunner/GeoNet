from scripts.layouts.CircularLayout import CircularLayout
from scripts.layouts.GridLayout import GridLayout
from scripts.layouts.LayoutType import LayoutType
from scripts.layouts.StackedLayout import StackedLayout


class LayoutFactory:
    def __init__(self, clustering_strategy):
        self.clustering_strategy = clustering_strategy

    def get_layout(self, layout_type: LayoutType):
        if layout_type == LayoutType.CIRCULAR:
            return CircularLayout(self.clustering_strategy)
        elif layout_type == LayoutType.GRID:
            return GridLayout(self.clustering_strategy)
        elif layout_type == LayoutType.STACKED:
            return StackedLayout(self.clustering_strategy)
        else:
            raise ValueError(f"Unknown layout type: {layout_type}")
