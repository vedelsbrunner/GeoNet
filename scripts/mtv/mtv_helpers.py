import numpy as np
from shapely import LineString
from shapely.affinity import translate
from shapely.ops import unary_union


def check_crossings(pair):
    line1, line2 = pair
    return LineString(line1).crosses(LineString(line2))


def calculate_centroid(hulls):
    # Combine all hulls into a single geometry to find the centroid
    all_hulls_geometry = [hull['geometry'] for hull in hulls]
    all_hulls_unified = unary_union(all_hulls_geometry)
    return all_hulls_unified.centroid


def hulls_overlap(hull1, hull2):
    return hull1.intersects(hull2)


def translate_polygon(polygon, vector):
    return translate(polygon, xoff=vector[0], yoff=vector[1])


def project_onto_axis(polygon, axis):
    projected = [np.dot(np.array(point), axis) for point in polygon.exterior.coords]
    return min(projected), max(projected)


def axis_overlap(poly_a_proj, poly_b_proj):
    return max(0, min(poly_a_proj[1], poly_b_proj[1]) - max(poly_a_proj[0], poly_b_proj[0]))


def get_axes(poly):
    axes = []
    points = list(poly.exterior.coords)
    for i in range(len(points) - 1):
        edge_vec = np.array(points[i]) - np.array(points[i + 1])
        normal = np.array([-edge_vec[1], edge_vec[0]])
        normal /= np.linalg.norm(normal)
        axes.append(normal)
    return axes


def calculate_mtv(poly_a, poly_b):
    axes = get_axes(poly_a) + get_axes(poly_b)
    mtv = None
    min_overlap = np.inf

    for axis in axes:
        poly_a_proj = project_onto_axis(poly_a, axis)
        poly_b_proj = project_onto_axis(poly_b, axis)
        overlap = axis_overlap(poly_a_proj, poly_b_proj)

        if overlap == 0:
            return None  # No MTV since there's no overlap

        if overlap < min_overlap:
            min_overlap = overlap
            mtv = axis * overlap

    return mtv
