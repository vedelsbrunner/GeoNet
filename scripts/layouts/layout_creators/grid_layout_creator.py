from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_grid_layout(dataset, network, clustering_strategy, grid_layout_config, is_aggregated):
    layout_factory = LayoutFactory(clustering_strategy)
    grid_layout = layout_factory.get_layout(LayoutType.GRID)
    grid_layout.create_layout(network, grid_layout_config)
    # network.resolve_overlaps()
    network.add_neighbors_and_edges()
    network.create_convex_hulls()
    if is_aggregated:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/grid-clustered.geojson', include_hulls=True, include_labels=False)  # TODO: sunflower vs grid
    else:
        network.write_to_disk(f'../geo-net-app/public/{dataset}/grid.geojson', include_hulls=True, include_labels=False)  # TODO: sunflower vs grid
    return