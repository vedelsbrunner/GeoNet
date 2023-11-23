import {LineLayer} from 'deck.gl';

export class EdgesLayer {
    createLayer(edges) {
        return new LineLayer({
            id: 'lines-layer',
            data: edges,
            getSourcePosition: d => d.geometry.coordinates[0],
            getTargetPosition: d => d.geometry.coordinates[1],
            pickable: true,
            getWidth: 50,
        });
    }
}
