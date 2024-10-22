from geopandas.tools import geocode

from scripts.utils.LoggerConfig import logger


def geocode_places(df, source_places="source_location", target_places="target_location"):
    if source_places not in df.columns or target_places not in df.columns:
        raise ValueError("Error: source_places or target_places not in df.columns")

    logger.debug(f"Geocoding {source_places} with {len(df)} places...")
    source_geocooded = geocode(df[source_places])
    logger.debug(f"Geocoded {len(source_geocooded)} places.")

    df['source_coordinates'] = source_geocooded['geometry']
    df['source_address'] = source_geocooded['address']

    logger.debug(f"Geocoding {target_places} with {len(df)} places...")
    target_geocoded = geocode(df[target_places])
    logger.debug(f"Geocoded {len(target_geocoded)} places.")

    df['target_coordinates'] = target_geocoded['geometry']
    df['target_address'] = target_geocoded['address']

    return df
