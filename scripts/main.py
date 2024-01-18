import copy

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.archeology import process_archeology_data, create_archeology_geo_network
from scripts.dataset_preprocessing.china import create_china_geo_network
from scripts.dataset_preprocessing.jucs import create_jucs_geo_network
from scripts.dataset_preprocessing.marie_boucher import create_marie_boucher_geo_network
from scripts.dataset_preprocessing.smith import create_smith_geo_network
from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig, CircularLayoutType
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
CREATE_DOUBLE_CIRCULAR_LAYOUT = True
CREATE_GRID_LAYOUT = True

EXECUTE_ALL = False


def create_layouts_for_network(dataset, network):
    if CREATE_DEFAULT_LAYOUT:
        create_default_layout(dataset, copy.deepcopy(network))

    if CREATE_SUNFLOWER_LAYOUT:
        sunflower_layout_config = SunflowerLayoutConfig(displacement_radius=0.15)
        create_sunflower_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), sunflower_layout_config, is_aggregated=True, resolve_overlaps=False)
        create_sunflower_layout(dataset, copy.deepcopy(network), SamePositionClustering(), sunflower_layout_config, is_aggregated=False, resolve_overlaps=False)

        create_sunflower_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), sunflower_layout_config, is_aggregated=True, resolve_overlaps=True)
        create_sunflower_layout(dataset, copy.deepcopy(network), SamePositionClustering(), sunflower_layout_config, is_aggregated=False, resolve_overlaps=True)

    if CREATE_STACKED_LAYOUT:
        stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.03, hull_buffer=0.03)
        create_stacked_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), stacked_layout_confing, is_aggregated=True, resolve_overlaps=False)
        create_stacked_layout(dataset, copy.deepcopy(network), SamePositionClustering(), stacked_layout_confing, is_aggregated=False, resolve_overlaps=False)

        create_stacked_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), stacked_layout_confing, is_aggregated=True, resolve_overlaps=True)
        create_stacked_layout(dataset, copy.deepcopy(network), SamePositionClustering(), stacked_layout_confing, is_aggregated=False, resolve_overlaps=True)

    if CREATE_CIRCULAR_LAYOUT:
        #TODO: Introduce configs based on dataset, e.g MarieBoucher needs scale 10 and China 25
        circular_layout_config = CircularLayoutConfig(layout_type=CircularLayoutType.SINGLE_CIRCLE, min_distance_between_nodes_km=8)
        create_circular_layout(dataset, CircularLayoutType.SINGLE_CIRCLE, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=True, resolve_overlaps=False)
        create_circular_layout(dataset, CircularLayoutType.SINGLE_CIRCLE, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=False, resolve_overlaps=False)

        create_circular_layout(dataset, CircularLayoutType.SINGLE_CIRCLE, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=True, resolve_overlaps=True)
        create_circular_layout(dataset, CircularLayoutType.SINGLE_CIRCLE, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=False, resolve_overlaps=True)

    if CREATE_DOUBLE_CIRCULAR_LAYOUT:
        circular_layout_config = CircularLayoutConfig(layout_type=CircularLayoutType.DOUBLE_CIRCLE, min_distance_between_nodes_km=8)
        create_circular_layout(dataset, CircularLayoutType.DOUBLE_CIRCLE, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=True, resolve_overlaps=False)
        create_circular_layout(dataset, CircularLayoutType.DOUBLE_CIRCLE, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=False, resolve_overlaps=False)

        create_circular_layout(dataset, CircularLayoutType.DOUBLE_CIRCLE, copy.deepcopy(network), DbscanClustering(eps=0.3), circular_layout_config, is_aggregated=True, resolve_overlaps=True)
        create_circular_layout(dataset, CircularLayoutType.DOUBLE_CIRCLE, copy.deepcopy(network), SamePositionClustering(), circular_layout_config, is_aggregated=False, resolve_overlaps=True)

    if CREATE_GRID_LAYOUT:
        grid_layout_config = GridLayoutConfig(distance_between_points=0.4)
        create_grid_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), grid_layout_config, is_aggregated=True, resolve_overlaps=False)
        create_grid_layout(dataset, copy.deepcopy(network), SamePositionClustering(), grid_layout_config, is_aggregated=False, resolve_overlaps=False)

        create_grid_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), grid_layout_config, is_aggregated=True, resolve_overlaps=True)
        create_grid_layout(dataset, copy.deepcopy(network), SamePositionClustering(), grid_layout_config, is_aggregated=False, resolve_overlaps=True)

def main():
    # process_archeology_data()
    # prepare_jucs_data()
    # geocode_jucs_data()
    # process_jucs_data()
    # process_china_data()
    # process_smith_data()

    network_creators = {
        'china': create_china_geo_network,
        'marieboucher': create_marie_boucher_geo_network,
        'smith': create_smith_geo_network,
        'jucs': create_jucs_geo_network,
        'archeology': create_archeology_geo_network
    }

    current_dataset = 'marieboucher'

    if EXECUTE_ALL:
        for dataset, creator in network_creators.items():
            network = creator()
            create_layouts_for_network(dataset, network)
    else:
        if current_dataset in network_creators:
            network = network_creators[current_dataset]()
            create_layouts_for_network(current_dataset, network)
        else:
            print(f"No network creator function found for dataset: {current_dataset}")


if __name__ == '__main__':
    main()
