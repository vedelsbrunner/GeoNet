from LoggerConfig import logger
from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout, LayoutConfig


class StackedLayoutConfig(LayoutConfig):
    def __init__(self, stack_points_offset: float, hull_buffer: float):
        self.stack_points_offset = stack_points_offset
        self.hull_buffer = hull_buffer


def create_stack(network, group, stack_point_offset):
    for i, (index, row) in enumerate(group.iterrows()):
        new_y = row.geometry.y + (i * stack_point_offset) # create stack along y-axis
        network.update_point(row.id, row.geometry.x, new_y)



class StackedLayout(Layout):
    def do_layout(self, network: GeoNetwork, config: StackedLayoutConfig):
        logger.debug(f"Creating stacked layout with point offset {config.stack_points_offset} and hull buffer {config.hull_buffer}")

        # Assume 'network.get_points()' returns a DataFrame with 'degree' and 'cluster' columns #TODO: Imrpove implicit assumption
        clusters = network.get_points().groupby('cluster')
        logger.debug(f"Found {len(clusters)} clusters for stacked layout")

        for _, points in clusters:
            sorted_points = self.sort_points_by_degree(network, points)
            create_stack(network, sorted_points, config.stack_points_offset)
        logger.debug(f"Repositioned points in clusters")

    def sort_points_by_degree(self, network: GeoNetwork, points):
        sorted_points = points.sort_values(by='degree', ascending=False)
        return sorted_points