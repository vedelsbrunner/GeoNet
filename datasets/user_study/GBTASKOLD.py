import random
import uuid
import networkx as nx
import numpy as np
import pandas as pd
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

cities = [
    "Aberdeen", "Belfast", "Birmingham", "Cardiff", "Cork",
    "Edinburgh", "Galway", "Glasgow", "Norwich", "Plymouth"
]


def create_scale_free_network(num_nodes, min_degree, max_degree):
    return nx.generators.random_graphs.barabasi_albert_graph(num_nodes, np.random.randint(min_degree, max_degree))


def geocode_cities(cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for city in cities:
        try:
            location = geolocator.geocode(city, timeout=10)
            if location:
                coordinates_dict[city] = (location.longitude, location.latitude)
            else:
                print(f"Location not found for {city}")
        except GeocoderTimedOut:
            print(f"Geocoding timed out for {city}")
    return coordinates_dict


def modify_network_with_highly_connected_node(G):
    max_degree_node, max_degree = max(G.degree(), key=lambda item: item[1])

    additional_connections = int(max_degree * 0.25)
    target_degree = max_degree + additional_connections

    new_node = max(G.nodes) + 1
    G.add_node(new_node)

    connected_nodes = set()
    while G.degree(new_node) < target_degree:
        node_to_connect = random.choice([node for node in G.nodes() if node != new_node and node not in connected_nodes])
        G.add_edge(new_node, node_to_connect)
        connected_nodes.add(node_to_connect)

        if len(connected_nodes) >= len(G.nodes()) - 1:
            break

    return new_node  # Return the new highly connected node


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
        print(f"Min degree {min_degree}")
        print(f"Max degree {max_degree}")

        G = create_scale_free_network(num_nodes, min_degree, max_degree)
        add_geographical_coordinates(G, coordinates_dict, node_distribution)
        new_node = modify_network_with_highly_connected_node(G)
        highly_connected_city = random.choices(list(node_distribution.keys()), weights=node_distribution.values(), k=1)[0]
        G.nodes[new_node]['coordinates'] = coordinates_dict[highly_connected_city]
        G.nodes[new_node]['city'] = highly_connected_city
        df = network_to_dataframe(G)
        df.to_csv(f'task1/geo_network_{i + 1}.csv', index=False)


coordinates_dict = geocode_cities(cities)
node_distribution = {city: random.randint(1, 50) for city in cities}
generate_and_save_networks(2, 100, coordinates_dict, node_distribution)
