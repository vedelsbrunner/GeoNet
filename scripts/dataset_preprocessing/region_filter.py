import pandas as pd
import pycountry
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut
from shapely import wkt

from scripts.utils.LoggerConfig import logger


def get_european_country_codes():
    # List of European ISO country codes including Russia (RU)
    european_country_codes = ['AL', 'AD', 'AM', 'AT', 'AZ', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
                              'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'XK', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC',
                              'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'UA', 'GB', 'VA']
    return european_country_codes


def get_middle_eastern_country_codes():
    # List of Middle Eastern ISO country codes including Russia and neighboring African countries
    middle_eastern_country_codes = [
        'SA',  # Saudi Arabia
        'IR',  # Iran
        'IQ',  # Iraq
        'IL',  # Israel
        'JO',  # Jordan
        'LB',  # Lebanon
        'OM',  # Oman
        'QA',  # Qatar
        'SY',  # Syria
        'TR',  # Turkey
        'AE',  # United Arab Emirates
        'YE',  # Yemen
        'RU',  # Russia
        'EG',  # Egypt
        'SD',  # Sudan
        'LY',  # Libya
        'DZ',  # Algeria
        'MA',  # Morocco
        'TN',  # Tunisia
        'DJ',  # Djibouti
        'SO',  # Somalia
        'ER',  # Eritrea
    ]
    return middle_eastern_country_codes


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


def is_middle_eastern_country(latitude, longitude, geolocator, middle_eastern_country_codes):
    try:
        query = f"{latitude}, {longitude}"
        location = geolocator.reverse(query, exactly_one=True)
        if location:
            country_code = location.raw['address'].get('country_code', '').upper()
            is_in_middle_east = country_code in middle_eastern_country_codes
            logger.debug(f"{location} - is {is_in_middle_east} in Middle East")
            return is_in_middle_east

        return False
    except GeocoderTimedOut:
        return False


def get_european_countries():
    countries = list(pycountry.countries)
    european_countries = [country.name for country in countries if country.region == 'Europe']
    european_countries.append('Russia')  # Explicitly add Russia
    return european_countries


def filter_middle_eastern_countries(file_path="../datasets/russia/russia_geocooded.csv", output_path="../datasets/russia/russia_geocooded_middle_east.csv"):
    geolocator = Nominatim(user_agent="GeoNet")
    middle_eastern_country_codes = get_middle_eastern_country_codes()

    df = pd.read_csv(file_path)
    df = df.dropna(subset=['location_address'])

    middle_eastern_indices = []

    for index, row in df.iterrows():
        try:
            location = wkt.loads(row['location'])
            if location.is_empty:
                logger.info("Skipping empty locations..")
                continue
            if is_middle_eastern_country(location.y, location.x, geolocator, middle_eastern_country_codes):
                middle_eastern_indices.append(index)
        except ValueError as e:
            print(f"Error processing row {index}: {e}")
            continue

    middle_eastern_df = df.loc[middle_eastern_indices]
    middle_eastern_df.to_csv(output_path, index=False)
    return middle_eastern_df
