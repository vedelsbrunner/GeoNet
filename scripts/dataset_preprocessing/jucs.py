from collections import Counter
from itertools import combinations
from shapely import wkt as wkt

import pandas as pd
import ast
from geopandas.tools import geocode
from shapely import Point

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger


# TODO: This dataset prepration process is different because we need to prep the lists before
# TODO: Add all props to processed data...
def prepare_jucs_data():
    jucs = "../datasets/jucs_sm.csv"
    df = pd.read_csv(jucs)

    df['Authors'] = df['Authors'].apply(ast.literal_eval)
    df['Author cities'] = df['Author cities'].apply(ast.literal_eval)

    df['Keywords'] = df['Keywords'].apply(ast.literal_eval)

    expanded_data = []

    for _, row in df.iterrows():
        authors = row['Authors']
        cities = row['Author cities']
        keywords = row['Keywords']

        for author, city in zip(authors, cities):
            expanded_data.append({'Author': author, 'City': city, 'Keywords': keywords})

    combined_df = pd.DataFrame(expanded_data)
    combined_df.to_csv("../datasets/jucs_prepared.csv", index=False)
    return


def geocode_jucs_data():
    jucs = "../datasets/jucs_prepared.csv"
    df = pd.read_csv(jucs)
    geocooded = geocode(df['City'])
    df['coordinates'] = geocooded['geometry']
    df.to_csv("../datasets/jucs_geocoded.csv", index=False)


def process_jucs_data():
    jucs = "../datasets/jucs_geocoded.csv"
    df = pd.read_csv(jucs)
    df['Keywords'] = df['Keywords'].apply(lambda x: x.strip("[]").replace("'", "").split(', '))  # Convert string list to actual list

    ignored_keywords = {"computer science", "technology", ""}  # Define ignored keywords here

    author_keywords = {}
    author_locations = {}
    keyword_frequency = Counter()

    for _, row in df.iterrows():
        author = row['Author']
        keywords_raw = row['Keywords']
        coordinates = row['coordinates']

        if not author or not coordinates:
            continue

        point = wkt.loads(row['coordinates'])

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

        author_locations[author] = location_str

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
                'source_coordinates': author_locations[author1],
                'target_coordinates': author_locations[author2]
            })

    network_df = pd.DataFrame(network_data)
    network_df.to_csv("../datasets/jucs_network.csv", index=False)
    return


def create_jucs_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/jucs_network.csv")

    for index, row in df.iterrows():
        target_location = wkt.loads(row['target_coordinates'])
        source_location = wkt.loads(row['source_coordinates'])

        if source_location.is_empty or target_location.is_empty:
            logger.info('Skipping empty location')
            continue

        source_node_id = f"{row['source']}"
        target_node_id = f"{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        network.add_point(source_node_id, source_location.x, source_location.y)
        network.add_point(target_node_id, target_location.x, target_location.y)
        network.add_line(line_id, source_node_id, target_node_id)

    network.finalize()
    logger.info(network.print_network_summary())
    # TODO: Add props 2.0
    return network
