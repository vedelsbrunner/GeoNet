from itertools import combinations

import pandas as pd
import pycountry
from geopandas.tools import geocode
from geopy import Nominatim, Point
from geopy.exc import GeocoderTimedOut
from shapely import wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger


def create_russia_europe_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/russia/russia_network_europe.csv")
    create_geo_network(df, network)
    return network


def create_russia_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/russia/russia_network.csv")
    create_geo_network(df, network)
    return network


def create_geo_network(df, network):
    df = df.dropna(subset=['source_location'])
    df = df.dropna(subset=['target_location'])

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
            'node_info': f"{df.loc[index]['PP']} ({df.loc[index]['source_location']})",
            'location': df.loc[index]['source_location']
        }

        target_node_props = {
            'node_info': f"{df.loc[index]['PP']} ({df.loc[index]['target_location']})",
            'location': df.loc[index]['target_location']
        }

        edge_props = {
            'edge_info': f"AgtId:{df.loc[index]['AgtId']} \n {df.loc[index]['agt_description']}"
        }

        network.add_point(source_node_id, source_location.x, source_location.y, **source_node_props)
        network.add_point(target_node_id, target_location.x, target_location.y, **target_node_props)
        network.add_line(line_id, source_node_id, target_node_id, **edge_props)

    network.finalize()
    logger.info(network.print_network_summary())
    return network


def process_russia_data(dataset_path, output_path):
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
                'source_location': source_data['location_address'],
                'target_location': target_data['location_address'],
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

    network_df.to_csv(output_path, index=False)


def geocode_russia_dataset(dataset_path='../datasets/russia.json', output_path="../datasets/russia_geocooded.csv"):
    df = pd.read_json(dataset_path)

    geocooded = geocode(df['To Node Name'])
    df['location'] = geocooded['geometry']
    df['location_address'] = geocooded['address']
    df.to_csv(output_path, index=False)


def is_european_country(latitude, longitude, geolocator, european_country_codes):
    try:
        query = f"{latitude}, {longitude}"
        location = geolocator.reverse(query, exactly_one=True)
        if location:
            country_code = location.raw['address'].get('country_code', '').upper()
            is_in_europe = country_code in european_country_codes
            logger.debug(f"{location} - is {is_in_europe} in Europe")
            return is_in_europe

        return False
    except GeocoderTimedOut:
        return False


def get_european_country_codes():
    # List of European ISO country codes including Russia (RU)
    european_country_codes = ['AL', 'AD', 'AM', 'AT', 'AZ', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
                              'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'XK', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC',
                              'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'UA', 'GB', 'VA']
    return european_country_codes


def get_european_countries():
    countries = list(pycountry.countries)
    european_countries = [country.name for country in countries if country.region == 'Europe']
    european_countries.append('Russia')  # Explicitly add Russia
    return european_countries


def filter_european_countries(file_path="../datasets/russia/russia_geocooded.csv", output_path="../datasets/russia/russia_geocooded_europe.csv"):
    geolocator = Nominatim(user_agent="GeoNet")
    european_country_codes = get_european_country_codes()

    df = pd.read_csv(file_path)
    df = df.dropna(subset=['location_address'])

    european_indices = []

    for index, row in df.iterrows():
        try:
            location = wkt.loads(row['location'])
            if location.is_empty:
                logger.info("Skipping empty locations..")
                continue
            if is_european_country(location.y, location.x, geolocator, european_country_codes):
                european_indices.append(index)
        except ValueError as e:
            print(f"Error processing row {index}: {e}")
            continue

    european_df = df.loc[european_indices]
    european_df.to_csv(output_path, index=False)
    return european_df
