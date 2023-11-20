from scripts.layouts.Layout import LayoutConfig


class CircularLayoutConfig(LayoutConfig):
    def __init__(self, radius_scale: float):
        super().__init__()
        self.radius_scale = radius_scale
        self.inner_radius_scale = 0.5
