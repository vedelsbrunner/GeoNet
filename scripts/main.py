import pandas as pd
import shapely.wkt as wkt

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.china import create_china_geo_network, process_china_data
from scripts.dataset_preprocessing.marie_boucher import create_marie_boucher_geo_network
from scripts.graph.GeoNetwork import GeoNetwork
from scripts.input.ColumnNormalizer import marieboucher_mapping, normalize_column_names
from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig
from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger



def create_circular_layout(dataset, network, clustering_strategy, config):
    layout_factory = LayoutFactory(clustering_strategy)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, config)
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    network.resolve_overlaps()
    network.add_neighbors_and_edges()
    # circular_layout.optimize_layout(network, max_iterations_per_cluster=1, improvement_threshold=1)
    # network.create_text_labels()
    network.write_to_disk(f'../geo-net-app/public/{dataset}/circular.geojson', include_hulls=True, include_labels=True)
    return network


def create_stacked_layout(dataset, network, clustering_strategy, config):
    layout_factory = LayoutFactory(clustering_strategy)
    stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    stacked_layout.create_layout(network, config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    network.resolve_overlaps()
    # network.create_text_labels()
    network.write_to_disk(f'../geo-net-app/public/{dataset}/stacked.geojson', include_hulls=False, include_labels=True)
    return network


def main():
    process_china_data()
    current_dataset = 'china'

    if current_dataset == 'china':
        network = create_china_geo_network()
    elif current_dataset == 'marieboucher':
        network = create_marie_boucher_geo_network()
    else:
        raise Exception('Invalid dataset')

    logger.info("Creating stacked layout")
    stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.005, hull_buffer=0.03)
    create_stacked_layout(current_dataset, network, SamePositionClustering(), stacked_layout_confing)
    #
    logger.info("Creating circular layout")
    circular_layout_config = CircularLayoutConfig(radius_scale=300)
    create_circular_layout(current_dataset, network, DbscanClustering(eps=0.3), circular_layout_config)


if __name__ == '__main__':
    main()
