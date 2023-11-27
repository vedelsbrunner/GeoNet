export const getLineWidth = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return 1;
        case 'LineString':
            return 1;
        default:
            return 1;
    }
};