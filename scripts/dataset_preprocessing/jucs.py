import ast
from collections import Counter
from itertools import combinations

import pandas as pd
from geopandas.tools import geocode
from shapely import Point
from shapely import wkt as wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger


# TODO: This dataset prepration process is different because we need to prep the lists before
# TODO: Add all props to processed data...
def prepare_jucs_data():
    jucs = "../datasets/jucs/jucs_sm.csv"
    df = pd.read_csv(jucs)

    df['Authors'] = df['Authors'].apply(ast.literal_eval)
    df['Author cities'] = df['Author cities'].apply(ast.literal_eval)
    df['Keywords'] = df['Keywords'].apply(ast.literal_eval)
    df['Author institutions'] = df['Author institutions'].apply(ast.literal_eval)

    expanded_data = []

    for _, row in df.iterrows():
        authors = row['Authors']
        cities = row['Author cities']
        keywords = row['Keywords']
        institutions = row['Author institutions']

        for author, city, institution in zip(authors, cities, institutions):
            expanded_data.append({'Author': author, 'City': city, 'Institution': institution, 'Keywords': keywords})

    combined_df = pd.DataFrame(expanded_data)
    combined_df.to_csv("../datasets/jucs/jucs_prepared.csv", index=False)
    return


def geocode_jucs_data():
    jucs = "../datasets/jucs/jucs_prepared.csv"
    df = pd.read_csv(jucs)
    geocooded = geocode(df['City'])
    df['location'] = geocooded['geometry']
    df['location_address'] = geocooded['address']
    df.to_csv("../datasets/jucs/jucs_geocoded.csv", index=False)


def process_jucs_data(input_path="../datasets/jucs/jucs_geocoded.csv", output_path="../datasets/jucs/jucs_network.csv"):
    df = pd.read_csv(input_path)
    df['Keywords'] = df['Keywords'].apply(lambda x: x.strip("[]").replace("'", "").split(', '))

    ignored_keywords = {"computer science", "technology", ""}  # Define ignored keywords here

    author_keywords = {}
    author_coordinates = {}
    author_locations = {}
    author_institutions = {}
    keyword_frequency = Counter()

    for _, row in df.iterrows():
        author = row['Author']
        keywords_raw = row['Keywords']
        coordinates = row['location']

        if not author or not coordinates:
            continue

        point = wkt.loads(row['location'])

        location = Point(point.x, point.y)
        location_str = str(location)

        # Filter keywords: accept all except ignored
        keywords = set(kw.lower().strip() for kw in keywords_raw
                       if kw.lower().strip() not in ignored_keywords)

        keyword_frequency.update(keywords)

        if author in author_keywords:
            author_keywords[author].update(keywords)
        else:
            author_keywords[author] = keywords

        author_coordinates[author] = location_str
        author_institutions[author] = row['Institution']
        author_locations[author] = row['location_address']

    logger.debug("Keyword Frequency (Ascending Order):")
    for keyword, freq in sorted(keyword_frequency.items(), key=lambda item: item[1]):
        logger.debug(f"{keyword}: {freq}")

    network_data = []

    for author1, author2 in combinations(author_keywords, 2):
        shared_keywords = author_keywords[author1].intersection(author_keywords[author2])
        if shared_keywords:
            network_data.append({
                'source': author1,
                'target': author2,
                'source_coordinates': author_coordinates[author1],
                'target_coordinates': author_coordinates[author2],
                'shared_keywords': ','.join(shared_keywords),
                'source_institution': author_institutions[author1],
                'target_institution': author_institutions[author2],
                'source_location': author_locations[author1],
                'target_location': author_locations[author2]
            })

    network_df = pd.DataFrame(network_data)
    network_df.to_csv(output_path, index=False)
    return


def create_jucs_europe_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/jucs/jucs_europe_network.csv")
    return create_geo_network(df, network)


def create_jucs_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/jucs/jucs_network.csv")
    return create_geo_network(df, network)


def create_geo_network(df, network):
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
            'node_info': f"{df.loc[index]['source']} ({df.loc[index]['source_institution']})",
            'location': df.loc[index]['source_location']
        }

        target_node_props = {
            'node_info': f"{df.loc[index]['target']} ({df.loc[index]['target_institution']})",
            'location': df.loc[index]['target_location']
        }

        edge_props = {
            'edge_info': f"{df.loc[index]['shared_keywords']}"
        }

        network.add_point(source_node_id, source_location.x, source_location.y, **source_node_props)
        network.add_point(target_node_id, target_location.x, target_location.y, **target_node_props)
        network.add_line(line_id, source_node_id, target_node_id, **edge_props)

    network.finalize()
    logger.info(network.print_network_summary())
    return network
