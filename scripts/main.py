import pandas as pd
import shapely.wkt as wkt

from scripts.cluster.DbscanClustering import DbscanClustering
from scripts.cluster.SamePositionClustering import SamePositionClustering
from scripts.graph.GeoNetwork import GeoNetwork
from scripts.input.ColumnNormalizer import marieboucher_mapping, normalize_column_names
from scripts.layouts.CircularLayoutConfig import CircularLayoutConfig
from scripts.layouts.LayoutFactory import LayoutFactory
from scripts.layouts.LayoutType import LayoutType
from scripts.layouts.StackedLayout import StackedLayoutConfig
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger


def process_marieboucher_data():
    mariebouche = "./datasets/marieboucher.csv"
    df = pd.read_csv(mariebouche)
    df.replace("Bouffay, Nantes", "Bouffay 44000 Nantes Frankreich", inplace=True)
    df.replace("Ile Saint Christophe", "Saint-Christophe-et-Niévès", inplace=True)
    df.replace(to_replace=r'\bSt\b', value='Saint', regex=True, inplace=True)

    df = normalize_column_names(df, marieboucher_mapping)
    df = geocode_places(df)
    df.to_csv("./datasets/marieboucher_geocoded.csv", index=False)


def create_marie_boucher_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/marieboucher_geocoded.csv")

    for index, row in df.iterrows():
        target_location = wkt.loads(row['target_coordinates'])
        source_location = wkt.loads(row['source_coordinates'])

        if source_location.is_empty or target_location.is_empty:
            logger.info('Skipping empty location')
            continue

        source_node_id = f"src_{row['source']}"
        target_node_id = f"tgt_{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        network.add_point(source_node_id, source_location.x, source_location.y)
        network.add_point(target_node_id, target_location.x, target_location.y)
        network.add_line(line_id, source_node_id, target_node_id)
    network.finalize()
    return network


def main():
    # process_marieboucher_data()
    network = create_marie_boucher_geo_network()
    clustering_strategy = DbscanClustering(eps=0.3)  # TODO: Cluster -1 ?
    # stack_layout_config = StackedLayoutConfig(stack_points_offset=0.008, hull_buffer=0.01)
    # clustering_strategy = SamePositionClustering()
    layout_factory = LayoutFactory(clustering_strategy)
    # stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    # stacked_layout.create_layout(network, stack_layout_config)

    circular_layout_config = CircularLayoutConfig(radius_scale=2)
    circular_layout = layout_factory.get_layout(LayoutType.CIRCULAR)
    circular_layout.create_layout(network, circular_layout_config)
    #
    network.create_convex_hulls() #Assuming that the network is already clustered #TODO
    # network.resolve_overlaps()
    # circular_layout.optimize_layout(network, max_iterations_per_cluster=5, improvement_threshold=1)

    network.add_neighbors_and_edges()

    network.write_to_disk('../geo-net-app/public/mb-stacked.geojson', include_hulls=True)


if __name__ == '__main__':
    main()