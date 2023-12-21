import {LineLayer} from 'deck.gl';

export class EdgesLayer {
    createLayer(edges, settings) {
        return new LineLayer({
            id: 'lines-layer',
            data: edges,
            autoHighlight: true,
            pickable: true,
            getSourcePosition: d => d.geometry.coordinates[0],
            getTargetPosition: d => d.geometry.coordinates[1],
            highlightColor: [255, 255, 255, 200],
            getColor: d => [169,169,169, 255 * settings.edgeOpacity],
            getWidth: d => settings.lineWidthScale / 1000,
        });
    }
}
