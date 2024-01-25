import {CollisionFilterExtension} from '@deck.gl/extensions';
import {TextLayer} from 'deck.gl';

export class LabelsLayer {
    createLayer(labels) {
        return new TextLayer({
            id: 'nodes-layer',
            data: labels,
            sizeUnits: 'meters',
            getPosition: d => d.geometry.coordinates,
            getText: d => d.properties.text,
            getAlignmentBaseline : 'top',
            pickable: false,
            getSize: 1500,
            background: true,
            getColor: [255,255,255,255],
            getBackgroundColor: [255, 255, 255, 80],
            // extensions: [new CollisionFilterExtension()]
        });
    }
}
