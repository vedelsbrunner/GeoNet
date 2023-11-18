import pandas as pd

from cluster.SamePositionClustering import SamePositionClustering
from graph.GeoNetwork import GeoNetwork
from Geocooder import geocode_places
import shapely.wkt as wkt
from input.ColumnNormalizer import marieboucher_mapping, normalize_column_names
from layouts.LayoutFactory import LayoutFactory
from layouts.LayoutType import LayoutType


def process_marieboucher_data():
    mariebouche = "./datasets/marieboucher.csv"
    df = pd.read_csv(mariebouche)
    df = normalize_column_names(df, marieboucher_mapping)
    df = geocode_places(df)
    df.to_csv("./datasets/marieboucher_geocoded.csv", index=False)


def main():
    # process_marieboucher_data()
    network = GeoNetwork()
    df = pd.read_csv("./datasets/marieboucher_geocoded.csv")

    for index, row in df.iterrows():
        target_location = wkt.loads(row['target_location'])
        source_location = wkt.loads(row['source_location'])

        if source_location.is_empty or target_location.is_empty:
            print('Skipping empty location')
            continue

        source_node_id = f"src_{row['source']}"
        target_node_id = f"tgt_{row['target']}"
        line_id = f"edge_{source_node_id}_{target_node_id}"

        network.add_point(source_node_id, source_location.x, source_location.y)
        network.add_point(target_node_id, target_location.x, target_location.y)
        network.add_line(line_id, source_node_id, target_node_id)

    network.finalize()

    clustering_strategy = SamePositionClustering()
    layout_factory = LayoutFactory(clustering_strategy)
    stacked_layout = layout_factory.get_layout(LayoutType.STACKED)
    stacked_layout.create_layout(network)

    # crossings = network.count_edge_crossings()
    # print(crossings)

    pass

if __name__ == '__main__':
    main()
