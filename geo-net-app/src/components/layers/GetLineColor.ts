export const getLineColor = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return [255, 255, 255, 20];
        case 'LineString':
            return [0, 120, 0, 255];
        default:
            return [0, 0, 0, 255];
    }
};