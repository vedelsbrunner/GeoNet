import {ScatterplotLayer} from 'deck.gl';

export class NodesLayer {
    createLayer(nodes, settings) {
        return new ScatterplotLayer({
            id: 'nodes-layer',
            data: nodes,
            pickable: true,
            autoHighlight: true,
            highlightColor: [255, 255, 255, 255],
            getPosition: d => d.geometry.coordinates,
            stroked: true,
            radiusUnits: 'meters',
            radiusScale: 2,
            radiusMinPixels: 4,

            lineWidthUnits: 'meters',
            lineWidthScale: 1000,
            lineWidthMaxPixels:  10,

            getLineColor: d => [0,0,0,255],
            getFillColor: d => [255,255,255,255 * settings.pointOpacity],
            getRadius: d => settings.pointRadius * Math.sqrt(d.properties.degree * 2),
        });
    }
}
