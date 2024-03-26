from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
from scripts.layouts.GridLayoutConfig import GridLayoutConfig
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig

common_russia_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.1, hull_buffer=0.1),
    'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.1),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.1),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.1),
    'grid': GridLayoutConfig(distance_between_points_km=15, hull_buffer=0.1)
}

common_jucs_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.1, hull_buffer=0.1),
    'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.06),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.06),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=25, hull_buffer=0.06),
    'grid': GridLayoutConfig(distance_between_points_km=15, hull_buffer=0.1)
}

common_marieboucher_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.07, hull_buffer=0.07),
    'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=8, hull_buffer=0.06),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=8, hull_buffer=0.06),
    'grid': GridLayoutConfig(distance_between_points_km=8, hull_buffer=0.08)
}

common_user_study_task1_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.11, hull_buffer=0.1),
    'stacked': StackedLayoutConfig(stack_points_offset=0.04, hull_buffer=0.07),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=16, hull_buffer=0.05),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=16, hull_buffer=0.05),
    'grid': GridLayoutConfig(distance_between_points_km=17, hull_buffer=0.11)
}

common_user_study_task4_config = {
    'sunflower': SunflowerLayoutConfig(displacement_radius=0.2, hull_buffer=0.2),
    'stacked': StackedLayoutConfig(stack_points_offset=0.08, hull_buffer=0.1),
    'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=32, hull_buffer=0.1),
    'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=32, hull_buffer=0.1),
    'grid': GridLayoutConfig(distance_between_points_km=32, hull_buffer=0.2)
}

dataset_configs = {
    'russia': common_russia_config,
    'russia_europe': common_russia_config,
    'russia_middle_east': common_russia_config,
    'jucs': common_jucs_config,
    'jucs_europe': common_jucs_config,
    'marieboucher': common_marieboucher_config,
    'china': {
        'sunflower': SunflowerLayoutConfig(displacement_radius=0.1, hull_buffer=0.1),
        'stacked': StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03),
        'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=15, hull_buffer=0.07),
        'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=15, hull_buffer=0.07),
        'grid': GridLayoutConfig(distance_between_points_km=15, hull_buffer=0.1)
    },
    'user_study_task1_1': common_user_study_task1_config,
    'user_study_task1_2': common_user_study_task1_config,
    'user_study_task1_3': common_user_study_task1_config,
    'user_study_task1_4': common_user_study_task1_config,
    'user_study_task1_5': common_user_study_task1_config,
    'user_study_task1_6': common_user_study_task1_config,
    'user_study_task1_7': common_user_study_task1_config,
    'user_study_task1_8': common_user_study_task1_config,

    'user_study_task2_1': common_user_study_task1_config,
    'user_study_task2_2': common_user_study_task1_config,
    'user_study_task2_3': common_user_study_task1_config,
    'user_study_task2_4': common_user_study_task1_config,
    'user_study_task2_5': common_user_study_task1_config,
    'user_study_task2_6': common_user_study_task1_config,
    'user_study_task2_7': common_user_study_task1_config,
    'user_study_task2_8': common_user_study_task1_config,

    'user_study_task3_1': common_user_study_task1_config,
    'user_study_task3_2': common_user_study_task1_config,
    'user_study_task3_3': common_user_study_task1_config,
    'user_study_task3_4': common_user_study_task1_config,
    'user_study_task3_5': common_user_study_task1_config,
    'user_study_task3_6': common_user_study_task1_config,
    'user_study_task3_7': common_user_study_task1_config,
    'user_study_task3_8': common_user_study_task1_config,

    'user_study_task4_1': common_user_study_task4_config,
    'user_study_task4_2': common_user_study_task4_config,
    'user_study_task4_3': common_user_study_task4_config,
    'user_study_task4_4': common_user_study_task4_config,
    'user_study_task4_5': common_user_study_task4_config,
    'user_study_task4_6': common_user_study_task4_config,
    'user_study_task4_7': common_user_study_task4_config,
    'user_study_task4_8': common_user_study_task4_config,

    'user_study_task2': common_marieboucher_config,
    'user_study_task3': {
        'sunflower': SunflowerLayoutConfig(displacement_radius=0.18, hull_buffer=0.15),
        'stacked': StackedLayoutConfig(stack_points_offset=0.1, hull_buffer=0.05),
        'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=40, hull_buffer=0.07),
        'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=40, hull_buffer=0.07),
        'grid': GridLayoutConfig(distance_between_points_km=40, hull_buffer=0.1)
    },
    'user_study_task4': {
        'sunflower': SunflowerLayoutConfig(displacement_radius=0.18, hull_buffer=0.15),
        'stacked': StackedLayoutConfig(stack_points_offset=0.1, hull_buffer=0.05),
        'single-circle': CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=40, hull_buffer=0.15),
        'double-circle': CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=40, hull_buffer=0.15),
        'grid': GridLayoutConfig(distance_between_points_km=40, hull_buffer=0.1)
    },

}
