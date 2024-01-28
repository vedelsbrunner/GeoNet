from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
from scripts.layouts.GridLayoutConfig import GridLayoutConfig
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig

common_russia_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.1, hull_buffer=0.1),
    'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.3),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.3),
    'grid': GridLayoutConfig(distance_between_points_km=15, hull_buffer=0.1)
}

dataset_configs = {
    'russia': common_russia_config,
    'russia_europe': common_russia_config,
    'russia_middle_east': common_russia_config
}
