import {GeoJsonLayer} from 'deck.gl';

export class HullsLayer {
    createHullsLayer(hulls) {
        return new GeoJsonLayer({
            id: 'hulls-layer',
            data: hulls,
            extruded: false,
            getFillColor: [240, 128, 128, 150],
            pickable: false,
            autoHighlight: false,
        });
    }
}