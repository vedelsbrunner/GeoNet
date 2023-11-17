import numpy as np
from shapely import unary_union
from shapely.affinity import translate


def calculate_centroid(hulls):
    # Combine all hulls into a single geometry to find the centroid
    all_hulls_geometry = [hull['geometry'] for hull in hulls]
    all_hulls_unified = unary_union(all_hulls_geometry)
    return all_hulls_unified.centroid


def calculate_and_apply_mtv(hulls_with_id, new_gdf):
    for idx1, hull1 in enumerate(hulls_with_id):
        for idx2, hull2 in enumerate(hulls_with_id):
            if idx1 < idx2:  # Avoid checking the same pair twice
                if hulls_overlap(hull1['geometry'], hull2['geometry']):
                    mtv = calculate_mtv(hull1['geometry'], hull2['geometry'])
                    if mtv is None:
                        print("Warning: No MTV calculated, skipping.")
                        continue  # Skip to the next pair

                    # Apply half the MTV to each hull in opposite directions with an additional fixed offset
                    translation_vector_1 = (-mtv / 2) - 0.01  # Offset to prevent hulls from touching
                    translation_vector_2 = (mtv / 2) + 0.01
                    hulls_with_id[idx1]['geometry'] = translate(hull1['geometry'], *translation_vector_1)
                    hulls_with_id[idx2]['geometry'] = translate(hull2['geometry'], *translation_vector_2)

                    # Displace points in the new_gdf corresponding to the hulls
                    group_id_1 = hull1['group_id']
                    group_id_2 = hull2['group_id']
                    new_gdf.loc[new_gdf['group_id'] == group_id_1, 'geometry'] = new_gdf.loc[new_gdf['group_id'] == group_id_1, 'geometry'].apply(lambda x: translate(x, *translation_vector_1))
                    new_gdf.loc[new_gdf['group_id'] == group_id_2, 'geometry'] = new_gdf.loc[new_gdf['group_id'] == group_id_2, 'geometry'].apply(lambda x: translate(x, *translation_vector_2))


def hulls_overlap(hull1, hull2):
    return hull1.intersects(hull2)


def translate_polygon(polygon, vector):
    # Translates the polygon by the given vector and returns a new polygon
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
