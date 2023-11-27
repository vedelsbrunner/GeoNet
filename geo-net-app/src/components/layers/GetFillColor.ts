export const getFillColor = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return [0, 0, 0, 150];
        case 'LineString':
            return [0, 120, 0, 20];
        case 'Polygon':
            return [0, 0, 255, 6];
    }
};