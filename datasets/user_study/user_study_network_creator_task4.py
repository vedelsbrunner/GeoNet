import random
import uuid
import networkx as nx
import numpy as np
import pandas as pd
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

# Updated list with cities from multiple countries
country_cities = {
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Leipzig"],
    "Poland": ["Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan"]
}

def create_scale_free_network(num_nodes, min_degree, max_degree):
    return nx.generators.random_graphs.barabasi_albert_graph(num_nodes, np.random.randint(min_degree, max_degree))

def select_random_cities_from_each_country(country_cities, min_cities=2, max_cities=5):
    selected_cities = {}
    for country, cities in country_cities.items():
        num_cities = random.randint(min_cities, min(max_cities, len(cities)))
        selected_cities[country] = random.sample(cities, num_cities)
    return selected_cities

def geocode_cities(cities):
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    coordinates_dict = {}
    for city in cities:  # Now `cities` is expected to be an iterable of city names
        try:
            # Assuming global search without specifying the country
            location = geolocator.geocode(city, timeout=10)
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
            # Allow overlapping nodes by assigning the same coordinates to different nodes
            G.nodes[node]['coordinates'] = (longitude, latitude)
            G.nodes[node]['city'] = city
        else:
            print(f"Coordinates not found for {city}")

def add_geographical_coordinates_and_create_nodes(G, coordinates_dict, country_cities):
    node_id = 0
    for country, cities in country_cities.items():
        for city in cities:
            coords = coordinates_dict.get(city, (None, None))
            if coords != (None, None):
                # Decide how many nodes you want per city for potential overlap
                num_nodes_per_city = random.randint(1, 10)  # For example, 2 to 4 nodes per city
                for _ in range(num_nodes_per_city):
                    G.add_node(node_id, city=city, coordinates=coords, country=country)
                    node_id += 1


def connect_countries(G, country1, country2, num_connections, increase_percentage=0):
    nodes_country1 = [node for node, data in G.nodes(data=True) if data['country'] == country1]
    nodes_country2 = [node for node, data in G.nodes(data=True) if data['country'] == country2]

    # Calculate the increased number of connections if specified
    num_connections += int(num_connections * increase_percentage)

    for _ in range(num_connections):
        if nodes_country1 and nodes_country2:
            node1 = random.choice(nodes_country1)
            node2 = random.choice(nodes_country2)
            G.add_edge(node1, node2)
def connect_nodes_within_cities(G):
    city_to_nodes = {}
    # Group nodes by city
    for node, data in G.nodes(data=True):
        city = data['city']
        if city not in city_to_nodes:
            city_to_nodes[city] = []
        city_to_nodes[city].append(node)
    # Connect nodes within the same city
    for city, nodes in city_to_nodes.items():
        for node_a in nodes:
            for node_b in nodes:
                if node_a != node_b:
                    G.add_edge(node_a, node_b)

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


def generate_and_save_networks(num_networks, coordinates_dict, country_cities):
    for i in range(num_networks):
        selected_country_cities = select_random_cities_from_each_country(country_cities)
        selected_coordinates_dict = {city: coordinates_dict[city] for country in selected_country_cities for city in selected_country_cities[country]}

        G = nx.Graph()
        add_geographical_coordinates_and_create_nodes(G, selected_coordinates_dict, selected_country_cities)
        connect_nodes_within_cities(G)

        # Assuming base number of connections as a parameter, e.g., 10
        base_connections = 100
        connect_countries(G, "France", "Spain", base_connections)
        # Germany and Poland get 25% more connections
        connect_countries(G, "Germany", "Poland", base_connections, increase_percentage=0.25)

        df = network_to_dataframe(G)
        filename = f'geo_network_cross_country_{i + 1}.csv'
        df.to_csv(filename, index=False)
        print(f"Network {i + 1} saved to '{filename}'")


# Geocode cities from the updated list
coordinates_dict = geocode_cities({city for country in country_cities for city in country_cities[country]})
# Generate and save networks with potential for overlapping nodes
generate_and_save_networks(2, coordinates_dict, country_cities)
