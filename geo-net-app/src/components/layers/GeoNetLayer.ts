import {GeoJsonLayer} from '@deck.gl/layers';
import {DataFilterExtension} from '@deck.gl/extensions';

export const createGeoNetLayer = (id, data, settings) => {
    const layer = new GeoJsonLayer({
            id: id,
            data: data,
            autoHighlight: true,
            pickable: true,
            highlightColor: [255, 255, 255, 155],
            getLineColor: getLineColor,
            getFillColor: getFillColor,
            lineWidthScale: 2,
            lineWidthMinPixels: 2,
            extruded: true,
            pointRadiusScale: 10,
            pointRadiusMinPixels: 1,
            pointRadiusMaxPixels: 150,
            getPointRadius: d => 150,
            getLineWidth: getLineWidth,
            extensions: [new DataFilterExtension({filterSize: 1})],
        })
    ;
    return layer;
}

const getLineWidth = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return 1;
        case 'LineString':
            return 1;
        default:
            return 1;
    }
};
const getLineColor = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return [255, 255, 255, 20];
        case 'LineString':
            return [0, 120, 0, 255];
        default:
            return [0, 0, 0, 255];
    }
};
const getFillColor = feature => {
    switch (feature.geometry.type) {
        case 'Point':
            return [0, 0, 0, 150];
        case 'LineString':
            return [0, 120, 0, 20];
        case 'Polygon':
            return [0, 0, 255, 255];
    }
};
