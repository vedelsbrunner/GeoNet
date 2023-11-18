import math
from graph.GeoNetwork import GeoNetwork
from layouts.Layout import Layout, LayoutConfig
from LoggerConfig import logger

class CircularLayoutConfig(LayoutConfig):
    def __init__(self, center: tuple, radius: float):
        self.center = center
        self.radius = radius


class CircularLayout(Layout):
    def do_layout(self, network: GeoNetwork, config: CircularLayoutConfig):
        logger.debug("Creating circular layout")

        # Group points by 'cluster' and apply layout to each cluster
        for cluster, points in network.get_points().groupby('cluster'):
            num_points = len(points)
            center_x, center_y = config.center  # Center of the circle
            radius = config.radius  # Radius of the circle

            # Calculate the angle between each point
            angle_step = 2 * math.pi / num_points

            # Place each point around the circle within its cluster
            for i, (index, point) in enumerate(points.iterrows()):
                angle = angle_step * i
                new_x = center_x + radius * math.cos(angle)
                new_y = center_y + radius * math.sin(angle)
                network.update_point(point['id'], new_x, new_y)

        logger.debug("Circular layout for clusters completed")