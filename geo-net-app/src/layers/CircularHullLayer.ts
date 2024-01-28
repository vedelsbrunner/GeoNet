import {ScatterplotLayer} from 'deck.gl';

export class CircularHullLayer {
    createLayer(nodes, settings) {
        return new ScatterplotLayer({
            id: 'circular-hull-layer',
            data: nodes,
            getPosition: d => d.geometry.coordinates,

            pickable: false,

            radiusUnits: 'meters',
            filled: true,
            getFillColor: d => [255,255,255,25],
            getRadius: d => d.properties.radius * 1000 + 6000,

            // Node Border settings
            stroked: true,
            lineWidthUnits: 'meters',
            getLineWidth: d => settings.nodeBorderWidth,
            getLineColor: d => [0,0,0,140]
        });
    }
}
