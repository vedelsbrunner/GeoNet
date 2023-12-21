import pandas as pd
import shapely.wkt as wkt

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.dataset_preprocessing.china import create_china_geo_network, process_china_data
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
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger



def create_circular_layout(dataset, network, clustering_strategy, config):
    layout_factory = LayoutFactory(clustering_strategy)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, config)
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    # network.resolve_overlaps()
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


def create_sunflower_layout(dataset, network, clustering_strategy, sunflower_layout_config):
    layout_factory = LayoutFactory(clustering_strategy)
    sunflower_layout = layout_factory.get_layout(LayoutType.SUNFLOWER)
    sunflower_layout.create_layout(network, sunflower_layout_config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()
    network.write_to_disk(f'../geo-net-app/public/{dataset}/default.geojson', include_hulls=True, include_labels=False)
    network.write_to_disk(f'../geo-net-app/public/china/default.geojson', include_hulls=True, include_labels=False)
    network.write_to_disk(f'../geo-net-app/public/jucs/sunflower.geojson', include_hulls=True, include_labels=False)
    network.write_to_disk(f'../geo-net-app/public/smith/sunflower.geojson', include_hulls=True, include_labels=False)
    return network

def create_grid_layout(dataset, network, clustering_strategy, grid_layout_config):
    layout_factory = LayoutFactory(clustering_strategy)
    grid_layout = layout_factory.get_layout(LayoutType.GRID)
    grid_layout.create_layout(network, grid_layout_config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()
    network.write_to_disk(f'../geo-net-app/public/{dataset}/sunflower.geojson', include_hulls=True, include_labels=False) #TODO: sunflower vs grid
    network.write_to_disk(f'../geo-net-app/public/china/sunflower.geojson', include_hulls=True, include_labels=False)
    network.write_to_disk(f'../geo-net-app/public/jucs/sunflower.geojson', include_hulls=True, include_labels=False)
    network.write_to_disk(f'../geo-net-app/public/smith/sunflower.geojson', include_hulls=True, include_labels=False)
    return network

def main():
    # process_china_data()
    # process_smith_data()
    current_dataset = 'smith'

    if current_dataset == 'china':
        network = create_china_geo_network()
    elif current_dataset == 'marieboucher':
        network = create_marie_boucher_geo_network()
    elif current_dataset == 'smith':
        network = create_smith_geo_network()
    else:
        raise Exception('Invalid dataset')

   # logger.info("Creating stacked layout")
   # stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.005, hull_buffer=0.03)
  #  create_stacked_layout(current_dataset, network, SamePositionClustering(), stacked_layout_confing)
    #
    logger.info("Creating circular layout")
    circular_layout_config = CircularLayoutConfig(radius_scale=2)
    create_circular_layout(current_dataset, network, SamePositionClustering(), circular_layout_config)

    # sunflower_layout_config = SunflowerLayoutConfig(displacement_radius=0.02)
    # create_sunflower_layout(current_dataset, network, DbscanClustering(eps=0.3), sunflower_layout_config)

    # grid_layout_config = GridLayoutConfig(distance_between_points=0.05)
    # create_grid_layout(current_dataset, network, DbscanClustering(eps=0.3), grid_layout_config)

if __name__ == '__main__':
    main()
