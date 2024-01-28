from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_grid_layout(dataset, network, clustering_strategy, config, is_aggregated, resolve_overlaps):
    layout_factory = LayoutFactory(clustering_strategy)
    grid_layout = layout_factory.get_layout(LayoutType.GRID)
    grid_layout.create_layout(network, config)

    network.create_convex_hulls(config.hull_buffer)

    if resolve_overlaps:
        network.resolve_overlaps(15)

    network.add_neighbors_and_edges()

    network.create_text_labels()

    file_name = ''
    if resolve_overlaps:
        file_name = 'no-overlap-'
    if is_aggregated:
        file_name += f'grid-clustered.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=True, include_labels=True)
    else:
        file_name += f'grid.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=True, include_labels=True)
    return
