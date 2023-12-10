import pandas as pd

from collections import Counter
from itertools import combinations
from shapely import Point, wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger

def create_china_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/china_geocoded.csv") #TODO: Relative always from main dir...

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
    # TODO: Add props 2.0
    return network


def process_china_data(min_matching_keywords=3):
    china = "../datasets/china.csv"
    df = pd.read_csv(china, keep_default_na=False)

    author_keywords = {}
    author_locations = {}
    keyword_frequency = Counter()
    ignore_keywords = ['', 'History', 'China']
    for _, row in df.iterrows():
        author = row['Author']
        keywords = set(kw.strip() for kw in row['Keywords_Ext'].split(',')) - set(ignore_keywords)
        location = Point(row['lng'], row['lat'])
        location_str = str(location)
        keyword_frequency.update(keywords)

        if author in author_keywords:
            author_keywords[author].update(keywords)
        else:
            author_keywords[author] = keywords

        author_locations[author] = location_str

    frequent_keywords = set(keyword for keyword, freq in keyword_frequency.items() if freq > 2)

    for author in author_keywords:
        author_keywords[author] = author_keywords[author].intersection(frequent_keywords)

    logger.debug("Keyword Frequency (Ascending Order):")
    for keyword, freq in sorted(keyword_frequency.items(), key=lambda item: item[1]):
        logger.debug(f"{keyword}: {freq}")

    network_data = []

    for author1, author2 in combinations(author_keywords, 2):
        shared_keywords = author_keywords[author1].intersection(author_keywords[author2])
        if len(shared_keywords) >= min_matching_keywords:
            network_data.append({
                'source': author1,
                'target': author2,
                'source_coordinates': author_locations[author1],
                'target_coordinates': author_locations[author2]
            })

    network_df = pd.DataFrame(network_data)
    # TODO: Add prop 1.0
    network_df.to_csv("../datasets/china_geocoded.csv", index=False)
    return