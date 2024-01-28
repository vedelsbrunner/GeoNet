from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_sunflower_layout(dataset, network, clustering_strategy, sunflower_layout_config, is_aggregated, resolve_overlaps):
    layout_factory = LayoutFactory(clustering_strategy)
    sunflower_layout = layout_factory.get_layout(LayoutType.SUNFLOWER)
    sunflower_layout.create_layout(network, sunflower_layout_config)

    network.create_convex_hulls(buffer_distance=sunflower_layout_config.hull_buffer)

    if resolve_overlaps:
        network.resolve_overlaps()

    network.add_neighbors_and_edges()

    network.create_text_labels()

    file_name = ''
    if resolve_overlaps:
        file_name = 'no-overlap-'

    if is_aggregated:
        file_name += 'sunflower-clustered.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=True, include_labels=True)
    else:
        file_name += f'sunflower.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=True, include_labels=True)
    return
