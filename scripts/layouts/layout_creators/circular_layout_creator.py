import logging

from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType


def create_circular_layout(dataset, layout_type, network, clustering_strategy, config, is_aggregated, resolve_overlaps):
    layout_factory = LayoutFactory(clustering_strategy)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, config)
    network.create_convex_hulls()  # Assuming that the network is already clustered #TODO

    if resolve_overlaps:
        network.resolve_overlaps(15)

    network.add_neighbors_and_edges()

    # circular_layout.optimize_layout(network, max_iterations_per_cluster=1, improvement_threshold=1)

    network.create_text_labels()

    file_name = ''
    if resolve_overlaps:
        file_name = 'no-overlap-'

    if is_aggregated:
        file_name += f'{layout_type.name.lower()}-circular-clustered.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=False, include_labels=True)
    else:
        file_name += f'{layout_type.name.lower()}-circular.geojson'
        network.write_to_disk(f'../geo-net-app/public/{dataset}/{file_name}', include_hulls=False, include_labels=True)
    return
