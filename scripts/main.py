import copy

import pandas as pd
import shapely.wkt as wkt

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.china import create_china_geo_network, process_china_data
from scripts.dataset_preprocessing.jucs import prepare_jucs_data, geocode_jucs_data, process_jucs_data, create_jucs_geo_network
from scripts.dataset_preprocessing.marie_boucher import create_marie_boucher_geo_network
from scripts.dataset_preprocessing.smith import process_smith_data, create_smith_geo_network
from scripts.graph.GeoNetwork import GeoNetwork
from scripts.input.ColumnNormalizer import marieboucher_mapping, normalize_column_names
from scripts.layouts.GridLayoutConfig import GridLayoutConfig
from scripts.layouts.GridLayout import GridLayout
from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig
from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig
from scripts.layouts.layout_creators.circular_layout_creator import create_circular_layout
from scripts.layouts.layout_creators.default_layout_creator import create_default_layout
from scripts.layouts.layout_creators.grid_layout_creator import create_grid_layout
from scripts.layouts.layout_creators.stacked_layout_creator import create_stacked_layout
from scripts.layouts.layout_creators.sunflower_layout_creator import create_sunflower_layout
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger










def main():
    # prepare_jucs_data()
    # geocode_jucs_data()
    # process_jucs_data()
    # process_china_data()
    # process_smith_data()

    current_dataset = 'marieboucher'

    if current_dataset == 'china':
        network = create_china_geo_network()
    elif current_dataset == 'marieboucher':
        network = create_marie_boucher_geo_network()
    elif current_dataset == 'smith':
        network = create_smith_geo_network()
    elif current_dataset == 'jucs':
        network = create_jucs_geo_network()
    else:
        raise Exception('Invalid dataset')

    create_default_layout(current_dataset, copy.deepcopy(network))

    sunflower_layout_config = SunflowerLayoutConfig(displacement_radius=0.1)
    create_sunflower_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), sunflower_layout_config, is_aggregated=False)
    create_sunflower_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), sunflower_layout_config, is_aggregated=True)

    stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.005, hull_buffer=0.03)
    create_stacked_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), stacked_layout_confing, is_aggregated=False)
    create_stacked_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), stacked_layout_confing, is_aggregated=True)

    circular_layout_config = CircularLayoutConfig(radius_scale=10)
    create_circular_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=False)
    create_circular_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=True)

    grid_layout_config = GridLayoutConfig(distance_between_points=0.1)
    create_grid_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), grid_layout_config, is_aggregated=False)
    create_grid_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), grid_layout_config, is_aggregated=True)


if __name__ == '__main__':
    main()
