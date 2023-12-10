from scripts.dataset_preprocessing.china import process_china_data
from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_circular_layout(network, clustering_strategy, config):
    layout_factory = LayoutFactory(clustering_strategy)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, config)
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    network.resolve_overlaps()
    network.add_neighbors_and_edges()
    circular_layout.optimize_layout(network, max_iterations_per_cluster=50, improvement_threshold=1)
    network.create_text_labels()
    network.write_to_disk('../geo-net-app/public/default.geojson', include_hulls=True, include_labels=True)
    return network


def create_stacked_layout(network, clustering_strategy, config):
    layout_factory = LayoutFactory(clustering_strategy)
    stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    stacked_layout.create_layout(network, config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    network.resolve_overlaps()
    network.create_text_labels()
    network.write_to_disk('../geo-net-app/public/stacked.geojson', include_hulls=False, include_labels=True)
    return network


def main():
    process_china_data()

    # network = create_marie_boucher_geo_network()
    #

    # logger.info("Creating stacked layout")
    # stacked_layout_confing = StackedLayoutConfig(stack_points_offset=0.005, hull_buffer=0.03)
    # create_stacked_layout(network, SamePositionClustering(), stacked_layout_confing)

    # logger.info("Creating circular layout")
    # circular_layout_config = CircularLayoutConfig(radius_scale=3)
    # create_circular_layout(network, DbscanClustering(eps=0.3), circular_layout_config)


if __name__ == '__main__':
    main()
