import {CollisionFilterExtension} from '@deck.gl/extensions';
import {TextLayer} from 'deck.gl';

export class LabelsLayer {
    createLayer(labels) {
        return new TextLayer({
            id: 'labels-layer',
            data: labels,
            sizeUnits: 'meters',
            getPosition: d => d.geometry.coordinates,
            getText: d => d.properties.text,
            getAlignmentBaseline: 'top',
            pickable: false,
            getSize: 15000,
            background: true,
            getColor: [255, 255, 255, 255],
            getBackgroundColor: [255, 255, 255, 0],
            characterSet: 'auto',
            fontFamily: '"Your Font Family", Arial, sans-serif', // Specify the font family here

            // extensions: [new CollisionFilterExtension()]
        });
    }
}
