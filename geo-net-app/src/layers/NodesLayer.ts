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
            radiusMinPixels: 1,
            radiusMaxPixels: 20,
            getFillColor: d => [0,0,0, 255 * settings.pointOpacity],
            getRadius: d => settings.pointRadius,
            onHover: info => console.log('hovered:', info),
            onClick: info => console.log('clicked:', info),
        });
    }
}
