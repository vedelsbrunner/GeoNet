import pandas as pd

from collections import Counter
from itertools import combinations
from shapely import Point, wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger

topics_keywords = {
    "Abstract Ideas & Thought Processes": ["modern", "history", "western", "century", "knowledge", "intellectual", "cultural", "world", "twentieth", "early"],
    "Hong Kong culture & Cinema": ["cultural", "social", "socialist", "Hong Kong", "culture", "history", "state", "historical", "film"],
    "Women & Education": ["women", "social", "medical", "education", "womens", "female", "Christian", "gender", "family", "missionaries"],
    "Religion & Buddhism in Early China": ["buddhist", "religious", "ritual", "buddhism", "practices", "religion", "zhou", "early", "period", "culture"],
    "Shanghai & Urban Culture": ["shanghai", "social", "cultural", "urban", "city", "literary", "culture", "literature", "public", "popular"],
    "International Relations": ["relations", "asia", "foreign", "states", "east", "american", "international", "policy", "world", "asian"],
    "Japan, Taiwan & Colonial Rule": ["japanese", "taiwan", "economic", "development", "state", "colonial", "rural", "taiwanese", "economy", "manchuria"],
    "Qing empire & State": ["qing", "local", "state", "imperial", "century", "empire", "system", "officials", "power", "legal"],
    "Political Movements & Revolution": ["political", "movement", "government", "communist", "party", "nationalist", "national", "revolution", "people", "military"],
    "Tang-Song-Ming, Culture and Arts": ["song", "ming", "literati", "painting", "political", "tang", "historical", "history", "dynasty", "paintings"]
}


def create_china_geo_network():
    network = GeoNetwork()
    df = pd.read_csv("../datasets/china_geocoded.csv")  # TODO: Relative always from main dir...

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


def process_china_data():
    accepted_keywords = topics_keywords["Tang-Song-Ming, Culture and Arts"]
    china = "../datasets/china.csv"
    df = pd.read_csv(china, keep_default_na=False)
    ignored_keywords = {"China", "History", ""}  # Add ignored keywords here

    normalized_accepted_keywords = {kw.lower().strip() for kw in accepted_keywords}
    normalized_ignored_keywords = {kw.lower().strip() for kw in ignored_keywords}

    author_keywords = {}
    author_locations = {}
    keyword_frequency = Counter()

    for _, row in df.iterrows():
        author = row.get('Author', None)
        keywords_raw = row.get('Keywords_Ext', '')
        lng = row.get('lng', None)
        lat = row.get('lat', None)

        if not author or lng is None or lat is None:
            continue

        keywords = set(kw.lower().strip() for kw in keywords_raw.split(',')
                       if kw.lower().strip() in normalized_accepted_keywords and
                       kw.lower().strip() not in normalized_ignored_keywords)
        location = Point(lng, lat)
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
        if shared_keywords:
            network_data.append({
                'source': author1,
                'target': author2,
                'source_coordinates': author_locations[author1],
                'target_coordinates': author_locations[author2]
            })

    network_df = pd.DataFrame(network_data)
    network_df.to_csv("../datasets/china_geocoded.csv", index=False)
    return
