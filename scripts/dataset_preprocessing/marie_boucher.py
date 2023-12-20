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

        source_node_id = f"src_{row['source']}"
        target_node_id = f"tgt_{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        network.add_point(source_node_id, source_location.x, source_location.y)
        network.add_point(target_node_id, target_location.x, target_location.y)
        network.add_line(line_id, source_node_id, target_node_id)

    network.finalize()

    for index, row in df.iterrows():
        source_node_id = f"src_{row['source']}"  # TODO: Duplicate code / Remove the finalize !!
        target_node_id = f"tgt_{row['target']}"

        props = {
            'content': df.loc[index]['Content'],
            'source': df.loc[index]['source'],
            'target': df.loc[index]['target'],
            'location': df.loc[index]['source_location'],
        }

        network.add_point_props(source_node_id, **props)

        props = {
            'content': df.loc[index]['Content'],
            'source': df.loc[index]['source'],
            'target': df.loc[index]['target'],
            'location': df.loc[index]['target_location'],
        }
        network.add_point_props(target_node_id, **props)
    return network


def process_marieboucher_data():
    mariebouche = "../datasets/marieboucher.csv"
    df = pd.read_csv(mariebouche)
    df.replace("Bouffay, Nantes", "Bouffay 44000 Nantes Frankreich", inplace=True)
    df.replace("Ile Saint Christophe", "Saint-Christophe-et-Niévès", inplace=True)
    df.replace(to_replace=r'\bSt\b', value='Saint', regex=True, inplace=True)

    df = normalize_column_names(df, marieboucher_mapping)
    df = geocode_places(df)
    df.to_csv("./datasets/marieboucher_geocoded.csv", index=False)
