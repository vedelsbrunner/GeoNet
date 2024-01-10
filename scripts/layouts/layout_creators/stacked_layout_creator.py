from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_stacked_layout(dataset, network, clustering_strategy, config, is_aggregated):
    layout_factory = LayoutFactory(clustering_strategy)
    stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    stacked_layout.create_layout(network, config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO
    # network.resolve_overlaps()
    # network.create_text_labels()
    if is_aggregated:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/stacked-clustered.geojson', include_hulls=False, include_labels=True)
    else:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/stacked.geojson', include_hulls=False, include_labels=True)
    return