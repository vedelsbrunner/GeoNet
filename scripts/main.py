import copy

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.archeology import process_archeology_data, create_archeology_geo_network
from scripts.dataset_preprocessing.china import create_china_geo_network
from scripts.dataset_preprocessing.jucs import create_jucs_geo_network
from scripts.dataset_preprocessing.marie_boucher import create_marie_boucher_geo_network
from scripts.dataset_preprocessing.smith import create_smith_geo_network
from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig
from scripts.layouts.GridLayoutConfig import GridLayoutConfig
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig
from scripts.layouts.layout_creators.circular_layout_creator import create_circular_layout
from scripts.layouts.layout_creators.default_layout_creator import create_default_layout
from scripts.layouts.layout_creators.grid_layout_creator import create_grid_layout
from scripts.layouts.layout_creators.stacked_layout_creator import create_stacked_layout
from scripts.layouts.layout_creators.sunflower_layout_creator import create_sunflower_layout

CREATE_DEFAULT_LAYOUT = True
CREATE_SUNFLOWER_LAYOUT = True
CREATE_STACKED_LAYOUT = True
CREATE_CIRCULAR_LAYOUT = True
CREATE_GRID_LAYOUT = True


def main():
    # process_archeology_data()
    # prepare_jucs_data()
    # geocode_jucs_data()
    # process_jucs_data()
    # process_china_data()
    # process_smith_data()

    current_dataset = 'china'

    if current_dataset == 'china':
        network = create_china_geo_network()
    elif current_dataset == 'marieboucher':
        network = create_marie_boucher_geo_network()
    elif current_dataset == 'smith':
        network = create_smith_geo_network()
    elif current_dataset == 'jucs':
        network = create_jucs_geo_network()
    elif current_dataset == 'archeology':
        network = create_archeology_geo_network()
    else:
        raise Exception('Invalid dataset')

    if CREATE_DEFAULT_LAYOUT:
        create_default_layout(current_dataset, copy.deepcopy(network))

    if CREATE_SUNFLOWER_LAYOUT:
        sunflower_layout_config = SunflowerLayoutConfig(displacement_radius=0.15)
        create_sunflower_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), sunflower_layout_config, is_aggregated=True)
        create_sunflower_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), sunflower_layout_config, is_aggregated=False)

    if CREATE_STACKED_LAYOUT:
        stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03)
        create_stacked_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), stacked_layout_confing, is_aggregated=True)
        create_stacked_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), stacked_layout_confing, is_aggregated=False)

    if CREATE_CIRCULAR_LAYOUT:
        #TODO: Introduce configs based on dataset, e.g MarieBoucher needs scale 10 and China 25
        circular_layout_config = CircularLayoutConfig(radius_scale=25)
        create_circular_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=True)
        create_circular_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=False)

    if CREATE_GRID_LAYOUT:
        grid_layout_config = GridLayoutConfig(distance_between_points=0.4)
        create_grid_layout(current_dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), grid_layout_config, is_aggregated=True)
        create_grid_layout(current_dataset, copy.deepcopy(network), SamePositionClustering(), grid_layout_config, is_aggregated=False)


if __name__ == '__main__':
    main()
