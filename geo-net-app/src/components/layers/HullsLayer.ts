import {GeoJsonLayer} from 'deck.gl';

export class HullsLayer {
    createHullsLayer(hulls)
    {
        console.log(hulls)
        return new GeoJsonLayer({
            id: 'hulls-layer',
            data: hulls,
            extruded: true,
            getFillColor: [160, 160, 180, 50],
        });
    }
}