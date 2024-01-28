from scripts.layouts.Layout import LayoutConfig


class GridLayoutConfig(LayoutConfig):
    def __init__(self, distance_between_points: float, hull_buffer: float):
        super().__init__()
        self.distance_between_points = distance_between_points
        self.hull_buffer = hull_buffer
