import os
import random
import uuid
import networkx as nx
import numpy as np
import pandas as pd
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

cities = {
    'scotland': ['Aberdeen', 'Edinburgh', 'Glasgow'],
    'england': ['London', 'Plymouth', 'Manchester'],
    'ireland': ['Dublin', 'Cork', 'Galway']
}


def create_scale_free_network(num_nodes, min_degree, max_degree):
    return nx.generators.random_graphs.barabasi_albert_graph(num_nodes, np.random.randint(min_degree, max_degree))


def geocode_cities(cities_dict):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for country, cities in cities_dict.items():
        coordinates_dict[country] = {}
        for city in cities:
            try:
                location = geolocator.geocode(f"{city}, {country}", timeout=10)  # Improve geocoding accuracy
                if location:
                    coordinates_dict[country][city] = (location.longitude, location.latitude)
                else:
                    print(f"Location not found for {city}")
            except GeocoderTimedOut:
                print(f"Geocoding timed out for {city}")
    return coordinates_dict


def add_geographical_coordinates(G, coordinates_dict, country_focus, network_idx, total_networks):
    node_cities = {}
    # Calculate node increase factors for focused country
    increase_start, increase_end = 1.25, 1.05  # Starting and ending increase factors
    increase_factor = increase_start - ((increase_start - increase_end) / (total_networks - 1)) * network_idx

    for country, cities in coordinates_dict.items():
        for city, coords in cities.items():
            base_node_count = random.randint(4, 10)
            if country == country_focus:
                node_count = int(base_node_count * increase_factor)
            else:
                node_count = base_node_count

            # Ensure not to sample more nodes than exist in the graph
            available_nodes = list(G.nodes())
            if len(available_nodes) < node_count:
                node_count = len(available_nodes)

            selected_nodes = random.sample(available_nodes, node_count)
            for node in selected_nodes:
                G.nodes[node]['coordinates'] = coords
                G.nodes[node]['city'] = city
                node_cities[city] = node_cities.get(city, 0) + 1

    return node_cities

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
        if 'city' in G.nodes[source] and 'city' in G.nodes[target]:
            data['source'].append(source)
            data['source_location'].append(G.nodes[source]['city'])
            data['target'].append(target)
            data['target_location'].append(G.nodes[target]['city'])
            data['source_coordinates'].append(G.nodes[source]['coordinates'])
            data['target_coordinates'].append(G.nodes[target]['coordinates'])
    return pd.DataFrame(data)


def generate_and_save_networks(num_networks, num_nodes, coordinates_dict):
    countries = list(cities.keys())
    for i in range(num_networks):
        network_dir = f'task2/network{i + 1}'
        os.makedirs(network_dir, exist_ok=True)

        # Rotate focus among countries for each network
        country_focus = countries[i % len(countries)]

        G = create_scale_free_network(num_nodes, 2, 3)  # Adjusted for simplicity
        node_distribution_update = add_geographical_coordinates(G, coordinates_dict, country_focus, i, num_networks)

        df = network_to_dataframe(G)
        df.to_csv(f'{network_dir}/geo_network_{i + 1}.csv', index=False)

        # Calculate and write node counts for each network
        country_node_counts = {country: sum(node_distribution_update.get(city, 0) for city in cities_list) for country, cities_list in cities.items()}
        with open(f'{network_dir}/aggregated_node_counts.txt', 'w') as f:
            for country, cities_list in cities.items():
                f.write(f"{country.capitalize()}:\n")
                for city in cities_list:
                    f.write(f"  {city}: {node_distribution_update.get(city, 0)}\n")
                f.write(f"Total {country.capitalize()} nodes: {country_node_counts[country]}\n\n")


coordinates_dict = geocode_cities(cities)
generate_and_save_networks(8, 100, coordinates_dict)
