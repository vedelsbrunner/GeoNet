from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_sunflower_layout(dataset, network, clustering_strategy, sunflower_layout_config, is_aggregated):
    layout_factory = LayoutFactory(clustering_strategy)
    sunflower_layout = layout_factory.get_layout(LayoutType.SUNFLOWER)
    sunflower_layout.create_layout(network, sunflower_layout_config)
    # network.resolve_overlaps()
    network.add_neighbors_and_edges()
    network.create_convex_hulls()
    if is_aggregated:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/sunflower-clustered.geojson', include_hulls=True, include_labels=False)
    else:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/sunflower.geojson', include_hulls=True, include_labels=False)
    return
