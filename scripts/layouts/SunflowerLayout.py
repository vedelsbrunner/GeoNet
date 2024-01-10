import math
from scripts.layouts.Layout import Layout
from scripts.layouts.SunflowerLayoutConfig import SunflowerLayoutConfig
from scripts.utils.LoggerConfig import logger

class SunflowerLayout(Layout):
    def __init__(self, clustering_strategy):
        super().__init__(clustering_strategy)

    def do_layout(self, network, config: SunflowerLayoutConfig):
        logger.debug(f"Creating sunflower layout with displacement radius {config.displacement_radius}")

        points_gdf = network.get_points()
        clusters = points_gdf['cluster'].unique()

        for cluster in clusters:
            cluster_points = points_gdf[points_gdf['cluster'] == cluster]

            cluster_points = cluster_points.sort_values(by='degree', ascending=False)

            num_points = len(cluster_points)
            if num_points <= 1:
                logger.debug("Skipping cluster with only one point")
                continue

            sunflower_center = cluster_points.geometry.unary_union.centroid
            alpha = (2 * math.pi) / ((1 + math.sqrt(5)) / 2)  # golden ratio

            for i, point in enumerate(cluster_points.itertuples()):
                r = math.sqrt(i) * config.displacement_radius
                theta = i * alpha
                new_x = sunflower_center.x + r * math.cos(theta)
                new_y = sunflower_center.y + r * math.sin(theta)
                network.update_point(point.id, new_x, new_y)
