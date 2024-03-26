import random
import uuid
import networkx as nx
import numpy as np
import pandas as pd
import math
import os
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

german_cities = [
    "Berlin", "Munich", "Frankfurt", "Hamburg",
    "Cologne", "Stuttgart", "Dresden", "Leipzig", "Bremen", "Hanover"
]

def create_scale_free_network(num_nodes, min_degree, max_degree):
    return nx.generators.random_graphs.barabasi_albert_graph(num_nodes, np.random.randint(min_degree, max_degree))

def geocode_cities(cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for city in cities:
        try:
            location = geolocator.geocode(city + ", Germany", timeout=10)
            if location:
                coordinates_dict[city] = (location.longitude, location.latitude)
            else:
                print(f"Location not found for {city}")
        except GeocoderTimedOut:
            print(f"Geocoding timed out for {city}")
    return coordinates_dict

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

def write_city_node_counts(G, filename):
    city_counts = {}
    for node in G.nodes():
        city = G.nodes[node]['city']
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1

    sorted_cities = sorted(city_counts.items(), key=lambda item: item[1], reverse=True)

    with open(filename, 'w') as f:
        for city, count in sorted_cities:
            f.write(f"{city}: {count}\n")

def generate_and_save_networks(num_networks, num_nodes, coordinates_dict, node_distribution):
    for i in range(1, num_networks + 1):
        min_degree = max(int(num_nodes * 0.01), 1)
        max_degree = max(int(num_nodes * 0.1), 3)

        G = create_scale_free_network(num_nodes, min_degree, max_degree)
        add_geographical_coordinates(G, coordinates_dict, node_distribution)
        df = network_to_dataframe(G)

        current_network_dir = f'task1/network{i}'
        os.makedirs(current_network_dir, exist_ok=True)

        network_csv_path = os.path.join(current_network_dir, f'geo_network_germany.csv')
        df.to_csv(network_csv_path, index=False)
        print(f"Network {i} saved to '{network_csv_path}'")

        city_counts_txt_path = os.path.join(current_network_dir, 'city_node_counts.txt')
        write_city_node_counts(G, city_counts_txt_path)
        print(f"City node counts for network {i} saved to '{city_counts_txt_path}'")

# Prepare for network generation
coordinates_dict = geocode_cities(german_cities)
node_distribution = {city: random.randint(1, 100) for city in german_cities}

# Calculate the maximum number of nodes and increase for one random city
max_nodes = max(node_distribution.values())
increased_max_nodes = math.ceil(max_nodes * 1.25)
city_with_increase = random.choice(list(node_distribution.keys()))
node_distribution[city_with_increase] = increased_max_nodes

# Generate the networks
generate_and_save_networks(8, 100, coordinates_dict, node_distribution)
