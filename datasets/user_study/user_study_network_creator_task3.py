import networkx as nx
import pandas as pd
import os
import random
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut
import uuid

# Define the cities of interest and their pairs
cities_of_interest = ["Berlin", "Hamburg", "Hannover", "Leipzig"]
city_pairs = [("Berlin", "Hamburg"), ("Hannover", "Leipzig")]

# Define the hardcoded number of edges for each network and city pair
network_edges = [
    (5, 15),  # Network 1
    (8, 14),  # Network 2
    (10, 18),  # Network 3
    (12, 15),  # Network 4
    (20, 35),  # Network 5
    (25, 30)   # Network 6
]

def geocode_cities(cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for city in cities:
        try:
            location = geolocator.geocode(city + ", Germany", timeout=10)
            if location:
                coordinates_dict[city] = (location.longitude, location.latitude)
        except GeocoderTimedOut:
            print(f"Geocoding timed out for {city}")
    return coordinates_dict

def create_custom_network_with_multiple_nodes(city_pairs, coordinates_dict, edge_counts):
    G = nx.Graph()
    # Create 8 nodes for each city and add to the graph
    for city in cities_of_interest:
        for i in range(8):  # Fixed number of nodes per city
            node_id = f"{city}_{i}"
            G.add_node(node_id, city=city, coordinates=coordinates_dict[city])

    # Connect nodes between the two cities based on the specified edge counts
    for i, (city1, city2) in enumerate(city_pairs):
        city1_nodes = [node for node in G.nodes if G.nodes[node]['city'] == city1]
        city2_nodes = [node for node in G.nodes if G.nodes[node]['city'] == city2]
        num_edges = edge_counts[i % 2]  # Alternate edge counts between city pairs for each network

        # Randomly create edges between nodes of the two cities
        while num_edges > 0:
            source = random.choice(city1_nodes)
            target = random.choice(city2_nodes)
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
        G = create_custom_network_with_multiple_nodes(city_pairs, coordinates_dict, edge_counts)

        df = network_to_dataframe(G)

        network_dir = f'task3/network{i+1}'
        os.makedirs(network_dir, exist_ok=True)

        # Export network data to CSV
        network_csv_path = os.path.join(network_dir, 'geo_network.csv')
        df.to_csv(network_csv_path, index=False)
        print(f"Network {i+1} data saved to '{network_csv_path}', Edge counts: {edge_counts}")

        # Calculate and save the number of edges and nodes for the city pairs to a text file
        summary_text_path = os.path.join(network_dir, 'city_pairs_summary.txt')
        with open(summary_text_path, 'w') as f:
            for pair_index, (city1, city2) in enumerate(city_pairs):
                city1_nodes = [node for node in G.nodes if G.nodes[node]['city'] == city1]
                city2_nodes = [node for node in G.nodes if G.nodes[node]['city'] == city2]
                city_pair_edges = [edge for edge in G.edges if edge[0] in city1_nodes and edge[1] in city2_nodes]
                f.write(f"{city1}-{city2} Pair:\n")
                f.write(f"  Nodes in {city1}: {len(city1_nodes)}\n")
                f.write(f"  Nodes in {city2}: {len(city2_nodes)}\n")
                f.write(f"  Edges between {city1} and {city2}: {len(city_pair_edges)}\n")
                f.write("\n")
        print(f"Summary for {city1}-{city2} saved to '{summary_text_path}'")

# Geocode cities
coordinates_dict = geocode_cities(cities_of_interest)

# Generate and save networks
generate_and_save_networks(6, coordinates_dict)
