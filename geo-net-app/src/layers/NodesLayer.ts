import {ScatterplotLayer} from 'deck.gl';

export class NodesLayer {
    createLayer(nodes, settings) {
        return new ScatterplotLayer({
            id: 'nodes-layer',
            data: nodes,
            pickable: true,
            autoHighlight: true,
            highlightColor: [255, 255, 255, 155],
            getPosition: d => d.geometry.coordinates,
            radiusScale: 2,
            stroked: true,
            radiusMinPixels: 1,
            lineWidthMinPixels: 0.5,
            getLineColor: d => [0,0,0,150],
            radiusMaxPixels: 20,
            getFillColor: d => [253,253,150,255 * settings.pointOpacity],
            getRadius: d => settings.pointRadius * Math.sqrt(d.properties.degree),
        });
    }
}
