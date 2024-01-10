def create_default_layout(dataset, network):
    network.add_neighbors_and_edges()
    network.write_to_disk(f'../geo-net-app/public/{dataset}/default.geojson', include_hulls=False, include_labels=False)

