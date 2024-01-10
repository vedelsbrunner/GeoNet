import {GeoJsonLayer} from 'deck.gl';

export class HullsLayer {
    createHullsLayer(hulls) {
        return new GeoJsonLayer({
            id: 'hulls-layer',
            data: hulls,
            extruded: false,
            getFillColor: [120, 188, 237, 50],
            pickable: false,
            autoHighlight: false,
        });
    }
}