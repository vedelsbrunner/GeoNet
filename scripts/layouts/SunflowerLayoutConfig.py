from scripts.layouts.Layout import LayoutConfig


class SunflowerLayoutConfig(LayoutConfig):
    def __init__(self, displacement_radius: float, hull_buffer: float):
        super().__init__()
        self.displacement_radius = displacement_radius
        self.hull_buffer = hull_buffer
