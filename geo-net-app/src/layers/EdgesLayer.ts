import {LineLayer} from 'deck.gl';

export class EdgesLayer {
    createLayer(edges, settings) {
        return new LineLayer({
            id: 'lines-layer',
            data: edges,
            autoHighlight: true,
            getSourcePosition: d => d.geometry.coordinates[0],
            getTargetPosition: d => d.geometry.coordinates[1],
            pickable: true,
            highlightColor: [255, 255, 255, 40],
            getColor: d => [0,0,0, 255 * settings.edgeOpacity],
            getWidth: d => settings.lineWidthScale / 1000,
        });
    }
}
