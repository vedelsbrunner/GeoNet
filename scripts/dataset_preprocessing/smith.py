from scripts.graph.GeoNetwork import GeoNetwork
import pandas as pd
from shapely import wkt as wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.input.ColumnNormalizer import normalize_column_names, marieboucher_mapping, smith_mapping
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger


def create_smith_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/smith_geocoded.csv")

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
    logger.info(network.print_network_summary())
    # TODO: Add props
    return network


def process_smith_data():
    smith = "../datasets/Smith_network.csv"
    df = pd.read_csv(smith)
    df = normalize_column_names(df, smith_mapping)
    df = geocode_places(df)
    df.to_csv("../datasets/smith_geocoded.csv", index=False)
