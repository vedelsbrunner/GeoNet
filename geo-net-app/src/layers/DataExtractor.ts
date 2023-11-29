export const ExtractDataLayers = (geoJson) => {
    let nodes = [];
    let edges = [];
    let hulls = {type: 'FeatureCollection', features: []};
    let location_labels = [];

    if (!geoJson) {
        console.error('Invalid or undefined geoJson data:', geoJson);
    }

    if (!Array.isArray(geoJson.features)) {
        console.log('Converting geoJson to array of features in case of filtering'); // TODO
        geoJson.features = geoJson
    }

    geoJson.features.forEach(feature => {
        if (!feature || !feature.geometry) {
            console.error('Invalid feature in geoJson:', feature);
            return;
        }

        switch (feature.geometry.type) {
            case 'Point':
                if (feature.properties.id.includes('location_label')) {
                    location_labels.push(feature);

                } else {
                    nodes.push(feature);
                }
                break;
            case 'LineString':
                edges.push(feature);
                break;
            case 'Polygon':
                hulls.features.push(feature);
                break;
            default:
                console.warn('Unhandled geometry type:', feature.geometry.type);
                break;
        }
    });

    return {nodes, edges, hulls, location_labels};
}
