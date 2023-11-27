import {ScatterplotLayer} from 'deck.gl';

export class NodesLayer {
    createLayer(nodes) {
        return new ScatterplotLayer({
            id: 'nodes-layer',
            data: nodes,
            pickable: true,
            autoHighlight: true,
            highlightColor: [255, 255, 255, 155],

            getPosition: d => d.geometry.coordinates,
            radiusScale: 6,
            radiusMinPixels: 1,
            radiusMaxPixels: 10,
            getRadius: d => 400,
            onHover: info => console.log('hovered:', info),
            onClick: info => console.log('clicked:', info),
        });
    }
}
