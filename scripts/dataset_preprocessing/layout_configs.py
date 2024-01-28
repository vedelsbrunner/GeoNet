from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
from scripts.layouts.GridLayoutConfig import GridLayoutConfig
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig

dataset_configs = {
    'russia': {
        'sunflower': SunflowerLayoutConfig(displacement_radius=0.05, hull_buffer=0.07),
        'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03),
        'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=10),
        'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=10),
        'grid': GridLayoutConfig(distance_between_points=0.2)
    },
    'russia_europe': {
        'sunflower': SunflowerLayoutConfig(displacement_radius=0.05, hull_buffer=0.07),
        'stacked': StackedLayoutConfig(stack_points_offset=0.04, hull_buffer=0.03),
        'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=10),
        'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=10),
        'grid': GridLayoutConfig(distance_between_points=0.2)
    }
}
