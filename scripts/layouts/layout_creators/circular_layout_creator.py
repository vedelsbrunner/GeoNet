from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_circular_layout(dataset, network, clustering_strategy, config, is_aggregated):
    layout_factory = LayoutFactory(clustering_strategy)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, config)
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    # network.resolve_overlaps()
    network.add_neighbors_and_edges()
    # circular_layout.optimize_layout(network, max_iterations_per_cluster=1, improvement_threshold=1)
    # network.create_text_labels()
    if is_aggregated:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/circular-clustered.geojson', include_hulls=False, include_labels=True)
    else:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/circular.geojson', include_hulls=False, include_labels=True)
    return
