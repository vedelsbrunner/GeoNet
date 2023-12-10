from collections import Counter
from itertools import combinations

import pandas as pd
from shapely import Point

from scripts.utils.LoggerConfig import logger


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
                'source_location': author_locations[author1],
                'target_location': author_locations[author2]
            })

    network_df = pd.DataFrame(network_data)
    network_df.to_csv("../datasets/china_geocoded.csv", index=False)
    return
