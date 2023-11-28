import {LineLayer} from 'deck.gl';

export class EdgesLayer {
    createLayer(edges) {
        return new LineLayer({
            id: 'lines-layer',
            data: edges,
            autoHighlight: true,
            getSourcePosition: d => d.geometry.coordinates[0],
            getTargetPosition: d => d.geometry.coordinates[1],
            pickable: true,
            highlightColor: [255, 255, 255, 40],

            getWidth: 1,
        });
    }
}
