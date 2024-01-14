from scripts.layouts.Layout import LayoutConfig

from enum import Enum, auto


class CircularLayoutType(Enum):
    SINGLE_CIRCLE = auto()
    DOUBLE_CIRCLE = auto()
    CIRCLE_PACKING = auto()


class CircularLayoutConfig(LayoutConfig):
    def __init__(self, layout_type: CircularLayoutType, min_distance_between_nodes_meters: int):
        super().__init__()
        self.layout_type = layout_type
        self.min_distance_between_nodes = min_distance_between_nodes_meters
