import copy

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.archeology import process_archeology_data, create_archeology_geo_network
from scripts.dataset_preprocessing.china import create_china_geo_network, process_china_data
from scripts.dataset_preprocessing.jucs import create_jucs_geo_network, process_jucs_data, prepare_jucs_data, geocode_jucs_data, create_jucs_europe_geo_network
from scripts.dataset_preprocessing.layout_configs import dataset_configs
from scripts.dataset_preprocessing.marie_boucher import create_marie_boucher_geo_network, process_marieboucher_data
from scripts.dataset_preprocessing.russia import geocode_russia_dataset, process_russia_data, create_russia_geo_network, create_russia_europe_geo_network, \
    create_russia_middle_east_geo_network
from scripts.dataset_preprocessing.region_filter import filter_european_countries, filter_middle_eastern_countries
from scripts.dataset_preprocessing.smith import create_smith_geo_network
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
        create_sunflower_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['sunflower'], is_aggregated=True, resolve_overlaps=False)
        create_sunflower_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['sunflower'], is_aggregated=False, resolve_overlaps=False)

        create_sunflower_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['sunflower'], is_aggregated=True, resolve_overlaps=True)
        create_sunflower_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['sunflower'], is_aggregated=False, resolve_overlaps=True)

    if CREATE_STACKED_LAYOUT:
        create_stacked_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['stacked'], is_aggregated=True, resolve_overlaps=False)
        create_stacked_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['stacked'], is_aggregated=False, resolve_overlaps=False)

        create_stacked_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['stacked'], is_aggregated=True, resolve_overlaps=True)
        create_stacked_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['stacked'], is_aggregated=False, resolve_overlaps=True)

    if CREATE_CIRCULAR_LAYOUT:
        create_circular_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['single-circle'], is_aggregated=True, resolve_overlaps=False)
        create_circular_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['single-circle'], is_aggregated=False, resolve_overlaps=False)

        create_circular_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['single-circle'], is_aggregated=True, resolve_overlaps=True)
        create_circular_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['single-circle'], is_aggregated=False, resolve_overlaps=True)

    if CREATE_DOUBLE_CIRCULAR_LAYOUT:
        create_circular_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['double-circle'], is_aggregated=True, resolve_overlaps=False)
        create_circular_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['double-circle'], is_aggregated=False, resolve_overlaps=False)

        create_circular_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['double-circle'], is_aggregated=True, resolve_overlaps=True)
        create_circular_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['double-circle'], is_aggregated=False, resolve_overlaps=True)

    if CREATE_GRID_LAYOUT:
        create_grid_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['grid'], is_aggregated=True, resolve_overlaps=False)
        create_grid_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['grid'], is_aggregated=False, resolve_overlaps=False)

        create_grid_layout(dataset, copy.deepcopy(network), DbscanClustering(eps=0.3), dataset_configs[dataset]['grid'], is_aggregated=True, resolve_overlaps=True)
        create_grid_layout(dataset, copy.deepcopy(network), SamePositionClustering(), dataset_configs[dataset]['grid'], is_aggregated=False, resolve_overlaps=True)


def main():
    # geocode_jucs_data()
    # prepare_jucs_data()
    # process_jucs_data()

    # filter_middle_eastern_countries()
    # filter_european_countries(file_path="../datasets/jucs/jucs_geocoded.csv", output_path="../datasets/jucs/jucs_geocoded_europe.csv")

    # process_russia_data(dataset_path="../datasets/russia/russia_geocooded_europe.csv", output_path="../datasets/russia/russia_network_europe.csv")
    # process_russia_data(dataset_path="../datasets/russia/russia_geocooded_middle_east.csv", output_path="../datasets/russia/russia_network_middle_east.csv")
    # process_russia_data(dataset_path="../datasets/russia/russia_geocooded.csv", output_path="../datasets/russia/russia_network.csv")

    # process_jucs_data("../datasets/jucs/jucs_geocoded_europe.csv", output_path="../datasets/jucs/jucs_europe_network.csv")
    # process_jucs_data("../datasets/jucs/jucs_geocoded.csv", output_path="../datasets/jucs/jucs_network.csv")

    # process_archeology_data()
    # geocode_jucs_data()
    # process_china_data()
    # process_smith_data()
    # process_marieboucher_data()

    network_creators = {
        'russia': create_russia_geo_network,
        'russia_europe': create_russia_europe_geo_network,
        'russia_middle_east': create_russia_middle_east_geo_network,
        'china': create_china_geo_network,
        'marieboucher': create_marie_boucher_geo_network,
        'smith': create_smith_geo_network,
        'jucs': create_jucs_geo_network,
        'jucs_europe': create_jucs_europe_geo_network,
        'archeology': create_archeology_geo_network
    }

    current_dataset = 'russia'

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
