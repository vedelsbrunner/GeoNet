import pandas as pd
from shapely import wkt

from scripts.graph.GeoNetwork import GeoNetwork
from scripts.utils.LoggerConfig import logger


def create_user_study_task1_1_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network1/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task1_2_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network2/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task1_3_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network3/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task1_4_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network4/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task1_5_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network5/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task1_6_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network6/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task3_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/geo_network_task3_1.csv")
    return create_user_study_network(df)


def create_user_study_task4_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/geo_network_cross_country_1.csv")
    return create_user_study_network(df)


def create_user_study_network(df):
    network = GeoNetwork()

    for index, row in df.iterrows():
        target_location = row['target_coordinates']
        source_location = row['source_coordinates']

        source_node_id = f"{row['source']}"
        target_node_id = f"{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        source_node_props = {
            'location': df.loc[index]['source_location']
        }

        target_node_props = {
            'location': df.loc[index]['target_location']
        }

        network.add_point(source_node_id, source_location.replace("(", "").replace(")", "").split(",")[0], source_location.replace("(", "").replace(")", "").split(",")[1], **source_node_props)
        network.add_point(target_node_id, target_location.replace("(", "").replace(")", "").split(",")[0], target_location.replace("(", "").replace(")", "").split(",")[1], **target_node_props)
        network.add_line(line_id, source_node_id, target_node_id)

    network.finalize()
    logger.info(network.print_network_summary())
    return network
