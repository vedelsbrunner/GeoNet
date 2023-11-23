import { ScatterplotLayer } from 'deck.gl';

export class NodesLayer {
    createLayer(nodes) {
        return new ScatterplotLayer({
            id: 'nodes-layer',
            data: nodes,
            getPosition: d => d.geometry.coordinates,
            radiusScale: 6,
            radiusMinPixels: 1,
            radiusMaxPixels: 100,
            getRadius: d => 10000
        });
    }
}
