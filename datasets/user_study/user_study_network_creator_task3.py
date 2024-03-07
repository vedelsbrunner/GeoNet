import random
import uuid
import networkx as nx
import numpy as np
import pandas as pd
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

# Updated list with 5 cities for each country
country_cities = {
    "Portugal": ["Lisbon", "Porto", "Coimbra"],
    "Spain": ["Madrid", "Barcelona", "Murcia", "Sevilla", "Bilbao"],
    "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Leipzig"],
    "France": ["Paris", "Lyon","Toulouse", "Nantes"],
    "Italy": ["Florenz", "Rome", "Milan", "Naples", "Bari", "Sicilia"],
    "Austria": ["Vienna", "Graz", "Liezen"]
}

def create_scale_free_network(num_nodes, min_degree, max_degree):
    return nx.generators.random_graphs.barabasi_albert_graph(num_nodes, np.random.randint(min_degree, max_degree))

def geocode_cities(selected_cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for city in selected_cities:
        try:
            location = geolocator.geocode(city, timeout=10)
            if location:
                coordinates_dict[city] = (location.longitude, location.latitude)
            else:
                print(f"Location not found for {city}")
        except GeocoderTimedOut:
            print(f"Geocoding timed out for {city}")
    return coordinates_dict

def select_random_cities(country_cities):
    selected_cities = {}
    for country, cities in country_cities.items():
        # Ensure not to select more cities than available in the list
        num_cities_to_select = random.randint(1, min(5, len(cities)))
        selected_cities[country] = random.sample(cities, num_cities_to_select)
    return selected_cities
def add_geographical_coordinates(G, coordinates_dict, node_distribution):
    for node in G.nodes():
        city = random.choices(list(node_distribution.keys()), weights=node_distribution.values(), k=1)[0]
        if city in coordinates_dict:
            longitude, latitude = coordinates_dict[city]
            G.nodes[node]['coordinates'] = (longitude, latitude)
            G.nodes[node]['city'] = city
        else:
            print(f"Coordinates not found for {city}")

def network_to_dataframe(G):
    data = {
        'source': [],
        'source_location': [],
        'target': [],
        'target_location': [],
        'source_coordinates': [],
        'target_coordinates': []
    }
    for edge in G.edges():
        source, target = edge
        data['source'].append(source)
        data['source_location'].append(G.nodes[source]['city'])
        data['target'].append(target)
        data['target_location'].append(G.nodes[target]['city'])
        data['source_coordinates'].append(G.nodes[source]['coordinates'])
        data['target_coordinates'].append(G.nodes[target]['coordinates'])
    return pd.DataFrame(data)

def generate_and_save_networks(num_networks, num_nodes, coordinates_dict, node_distribution):
    for i in range(num_networks):
        min_degree = max(int(num_nodes * 0.01), 1)
        max_degree = max(int(num_nodes * 0.1), 3)

        G = create_scale_free_network(num_nodes, min_degree, max_degree)
        add_geographical_coordinates(G, coordinates_dict, node_distribution)
        df = network_to_dataframe(G)
        df.to_csv(f'geo_network_task3_{i + 1}.csv', index=False)
        print(f"Network {i + 1} saved to 'geo_network_task3_{i + 1}.csv'")

# Randomly select cities
selected_cities_per_country = select_random_cities(country_cities)
# Flatten the list of selected cities for geocoding
selected_cities = [city for cities in selected_cities_per_country.values() for city in cities]
coordinates_dict = geocode_cities(selected_cities)

# Create a node distribution that maps each selected city to a random value
node_distribution = {city: random.randint(1, 50) for city in selected_cities}
generate_and_save_networks(2, 100, coordinates_dict, node_distribution)
