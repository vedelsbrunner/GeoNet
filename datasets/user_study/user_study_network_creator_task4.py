import networkx as nx
import pandas as pd
import os
import random
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut
import uuid

# Updated list with cities from multiple countries
country_cities = {
    "Spain": ["Madrid", "Barcelona", "Bilbao"],
    "France": ["Paris", "Lyon", "Marseille"],
    "Germany": ["Berlin", "Hamburg", "Leipzig"],
    "Poland": ["Danzig", "Krakow", "Wroclaw"]
}

# Define country pairs
country_pairs = [("France", "Spain"), ("Germany", "Poland")]

# Define the hardcoded number of edges for each network and country pair
network_edges = [
    (10, 20),  # Network 1
    (25, 15),  # Network 2
    (30, 20), # Network 3
    (40, 35), # Network 4
    (27, 35), # Network 5
    (24, 42),  # Network 6
    (55, 60),  # Network 7
    (78, 60)  # Network 8
]

def geocode_cities(cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for country, cities_list in cities.items():
        for city in cities_list:
            try:
                location = geolocator.geocode(city + ", " + country, timeout=10)
                if location:
                    coordinates_dict[city] = (location.longitude, location.latitude)
            except GeocoderTimedOut:
                print(f"Geocoding timed out for {city}")
    return coordinates_dict

def create_custom_network_with_multiple_nodes(country_pairs, coordinates_dict, edge_counts):
    G = nx.Graph()
    # Create nodes for each city and add to the graph
    for country, cities_list in country_cities.items():
        for city in cities_list:
            for i in range(12):  # Fixed number of nodes per city
                node_id = f"{city}_{i}"
                G.add_node(node_id, city=city, country=country, coordinates=coordinates_dict[city])

    # Connect nodes between cities of the two countries based on the specified edge counts
    for i, (country1, country2) in enumerate(country_pairs):
        country1_cities = country_cities[country1]
        country2_cities = country_cities[country2]
        country1_nodes = [node for node in G.nodes if G.nodes[node]['country'] == country1]
        country2_nodes = [node for node in G.nodes if G.nodes[node]['country'] == country2]
        num_edges = edge_counts[i % 2]  # Alternate edge counts between country pairs for each network

        # Randomly create edges between nodes of the two countries
        while num_edges > 0:
            source = random.choice(country1_nodes)
            target = random.choice(country2_nodes)
            if not G.has_edge(source, target):
                G.add_edge(source, target)
                num_edges -= 1

    return G

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
        source_city = G.nodes[source]['city']
        target_city = G.nodes[target]['city']
        data['source'].append(source)
        data['source_location'].append(source_city)
        data['target'].append(target)
        data['target_location'].append(target_city)
        data['source_coordinates'].append(G.nodes[source]['coordinates'])
        data['target_coordinates'].append(G.nodes[target]['coordinates'])
    return pd.DataFrame(data)

def generate_and_save_networks(num_networks, coordinates_dict):
    for i in range(num_networks):
        edge_counts = network_edges[i]
        G = create_custom_network_with_multiple_nodes(country_pairs, coordinates_dict, edge_counts)

        df = network_to_dataframe(G)

        network_dir = f'task4/network{i+1}'
        os.makedirs(network_dir, exist_ok=True)

        # Export network data to CSV
        network_csv_path = os.path.join(network_dir, 'geo_network.csv')
        df.to_csv(network_csv_path, index=False)
        print(f"Network {i+1} data saved to '{network_csv_path}', Edge counts: {edge_counts}")

        # Calculate and save the number of edges and nodes for the country pairs to a text file
        summary_text_path = os.path.join(network_dir, 'country_pairs_summary.txt')
        with open(summary_text_path, 'w') as f:
            for pair_index, (country1, country2) in enumerate(country_pairs):
                country1_nodes = [node for node in G.nodes if G.nodes[node]['country'] == country1]
                country2_nodes = [node for node in G.nodes if G.nodes[node]['country'] == country2]
                country_pair_edges = [edge for edge in G.edges if G.nodes[edge[0]]['country'] == country1 and G.nodes[edge[1]]['country'] == country2]
                f.write(f"{country1}-{country2} Pair:\n")
                f.write(f"  Nodes in {country1}: {len(country1_nodes)}\n")
                f.write(f"  Nodes in {country2}: {len(country2_nodes)}\n")
                f.write(f"  Edges between {country1} and {country2}: {len(country_pair_edges)}\n")
                f.write("\n")
        print(f"Summary for {country1}-{country2} saved to '{summary_text_path}'")

# Geocode cities
coordinates_dict = geocode_cities(country_cities)

# Generate and save networks
generate_and_save_networks(8, coordinates_dict)
