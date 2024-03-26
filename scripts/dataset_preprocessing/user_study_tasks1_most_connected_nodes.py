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

def create_user_study_task1_7_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network7/geo_network_germany.csv")
    return create_user_study_network(df)

def create_user_study_task1_8_most_connected_nodes():
    df = pd.read_csv("../datasets/user_study/task1/network8/geo_network_germany.csv")
    return create_user_study_network(df)


def create_user_study_task2_1():
    df = pd.read_csv("../datasets/user_study/task2/network1/geo_network_1.csv")
    return create_user_study_network(df)


def create_user_study_task2_2():
    df = pd.read_csv("../datasets/user_study/task2/network2/geo_network_2.csv")
    return create_user_study_network(df)


def create_user_study_task2_3():
    df = pd.read_csv("../datasets/user_study/task2/network3/geo_network_3.csv")
    return create_user_study_network(df)


def create_user_study_task2_4():
    df = pd.read_csv("../datasets/user_study/task2/network4/geo_network_4.csv")
    return create_user_study_network(df)


def create_user_study_task2_5():
    df = pd.read_csv("../datasets/user_study/task2/network5/geo_network_5.csv")
    return create_user_study_network(df)


def create_user_study_task2_6():
    df = pd.read_csv("../datasets/user_study/task2/network6/geo_network_6.csv")
    return create_user_study_network(df)

def create_user_study_task2_7():
    df = pd.read_csv("../datasets/user_study/task2/network7/geo_network_7.csv")
    return create_user_study_network(df)

def create_user_study_task2_8():
    df = pd.read_csv("../datasets/user_study/task2/network8/geo_network_8.csv")
    return create_user_study_network(df)


def create_user_study_task3_1():
    df = pd.read_csv("../datasets/user_study/task3/network1/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task3_2():
    df = pd.read_csv("../datasets/user_study/task3/network2/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task3_3():
    df = pd.read_csv("../datasets/user_study/task3/network3/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task3_4():
    df = pd.read_csv("../datasets/user_study/task3/network4/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task3_5():
    df = pd.read_csv("../datasets/user_study/task3/network5/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task3_6():
    df = pd.read_csv("../datasets/user_study/task3/network6/geo_network.csv")
    return create_user_study_network(df)

def create_user_study_task3_7():
    df = pd.read_csv("../datasets/user_study/task3/network7/geo_network.csv")
    return create_user_study_network(df)

def create_user_study_task3_8():
    df = pd.read_csv("../datasets/user_study/task3/network8/geo_network.csv")
    return create_user_study_network(df)

def create_user_study_task4_1():
    df = pd.read_csv("../datasets/user_study/task4/network1/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_2():
    df = pd.read_csv("../datasets/user_study/task4/network2/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_3():
    df = pd.read_csv("../datasets/user_study/task4/network3/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_4():
    df = pd.read_csv("../datasets/user_study/task4/network4/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_5():
    df = pd.read_csv("../datasets/user_study/task4/network5/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_6():
    df = pd.read_csv("../datasets/user_study/task4/network6/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_7():
    df = pd.read_csv("../datasets/user_study/task4/network7/geo_network.csv")
    return create_user_study_network(df)


def create_user_study_task4_8():
    df = pd.read_csv("../datasets/user_study/task4/network8/geo_network.csv")
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
