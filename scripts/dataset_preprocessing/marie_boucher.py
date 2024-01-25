import pandas as pd
from shapely import wkt as wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.input.ColumnNormalizer import normalize_column_names, marieboucher_mapping
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger


def create_marie_boucher_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/marieboucher_geocoded.csv")

    for index, row in df.iterrows():
        target_location = wkt.loads(row['target_coordinates'])
        source_location = wkt.loads(row['source_coordinates'])

        if source_location.is_empty or target_location.is_empty:
            logger.info('Skipping empty location')
            continue

        source_node_id = f"{row['source']}"
        target_node_id = f"{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        source_node_props = {
            'node_info': df.loc[index]['source'],
            'location': df.loc[index]['source_location']
        }

        target_node_props = {
            'node_info': df.loc[index]['target'],
            'location': df.loc[index]['target_location']
        }

        edge_props = {
            'edge_info': df.loc[index]['Content']
        }

        network.add_point(source_node_id, source_location.x, source_location.y, **source_node_props)
        network.add_point(target_node_id, target_location.x, target_location.y, **target_node_props)
        network.add_line(line_id, source_node_id, target_node_id, **edge_props)

    network.finalize()
    logger.info(network.print_network_summary())
    return network

def drop_null_entries(df):
    null_count = df[df['source_location'].isnull() | df['target_location'].isnull()].shape[0]
    if null_count > 0:
        logger.info(f"Dropping {null_count} entries where 'source_location' or 'target_location' is null.")
        df = df.dropna(subset=['source_location', 'target_location'])
    else:
        logger.info("No entries found with null 'source_location' or 'target_location'.")
    return df

def process_marieboucher_data():
    marieboucher = "../datasets/marieboucher.csv"
    df = pd.read_csv(marieboucher)
    df.replace("Bouffay, Nantes", "Bouffay 44000 Nantes Frankreich", inplace=True)
    df.replace("Ile Saint Christophe", "Saint-Christophe-et-Niévès", inplace=True)
    df.replace(to_replace=r'\bSt\b', value='Saint', regex=True, inplace=True)

    df = normalize_column_names(df, marieboucher_mapping)
    df = drop_null_entries(df)
    df = geocode_places(df)
    df.to_csv("../datasets/marieboucher_geocoded.csv", index=False)
