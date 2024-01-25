from itertools import combinations

import pandas as pd
from geopandas.tools import geocode
from shapely import wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.Geocooder import geocode_places
from scripts.utils.LoggerConfig import logger


def create_russia_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/russia_network_with_properties.csv")

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
            'node_info': df.loc[index]['PP'],
        }

        target_node_props = {
            'node_info': df.loc[index]['PP'],
        }

        edge_props = {
            'edge_info': df.loc[index]['agt_description']
        }

        network.add_point(source_node_id, source_location.x, source_location.y, **source_node_props)
        network.add_point(target_node_id, target_location.x, target_location.y, **target_node_props)
        network.add_line(line_id, source_node_id, target_node_id, **edge_props)

    network.finalize()
    return network


def process_russia_data():
    dataset_path = '../datasets/russia_geocooded.csv'
    df = pd.read_csv(dataset_path)

    location_to_id = {}
    unique_locations = df['location'].unique()
    for idx, location in enumerate(unique_locations):
        location_to_id[location] = f"location_{idx}"

    network_data = []

    for agt_id in df['AgtId'].unique():
        subset_df = df[df['AgtId'] == agt_id]
        locations = subset_df['location'].unique()

        for loc1, loc2 in combinations(locations, 2):
            source_data = subset_df[subset_df['location'] == loc1].iloc[0]
            target_data = subset_df[subset_df['location'] == loc2].iloc[0]

            edge_data = {
                'source': f"{source_data['PP']}_{location_to_id[loc1]}",
                'target': f"{target_data['PP']}_{location_to_id[loc2]}",
                'source_address': source_data['location_address'],
                'target_address': target_data['location_address'],
                'source_coordinates': source_data['location'],
                'target_coordinates': target_data['location'],
                'Con': source_data['Con'],
                'Date': source_data['date'],
                'Year': source_data['year'],
                'From_Node_Full_Name': source_data['From Node (Full Name)'],
                'PP': source_data['PP'],
                'agt_description': source_data['agt_description'],
                'AgtId': source_data['AgtId']
            }

            network_data.append(edge_data)

    network_df = pd.DataFrame(network_data)

    network_df.to_csv('../datasets/russia_network_with_properties.csv', index=False)


process_russia_data()


def geocode_russia_dataset():
    dataset_path = '../datasets/russia.json'
    df = pd.read_json(dataset_path)

    geocooded = geocode(df['To Node Name'])
    df['location'] = geocooded['geometry']
    df['location_address'] = geocooded['address']
    df.to_csv("../datasets/russia_geocooded.csv", index=False)
