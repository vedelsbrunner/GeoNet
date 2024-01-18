from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_stacked_layout(dataset, network, clustering_strategy, config, is_aggregated, resolve_overlaps):
    layout_factory = LayoutFactory(clustering_strategy)
    stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    stacked_layout.create_layout(network, config)
    network.add_neighbors_and_edges()
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO

    if resolve_overlaps:
        network.resolve_overlaps(15)

    # network.create_text_labels()

    file_name = ''
    if resolve_overlaps:
        file_name = 'no-overlap-'

    if is_aggregated:
        file_name += 'stacked-clustered.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=False, include_labels=True)
    else:
        file_name += f'stacked.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=False, include_labels=True)
    return