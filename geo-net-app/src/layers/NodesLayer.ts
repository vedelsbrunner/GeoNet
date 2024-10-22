import {ScatterplotLayer} from 'deck.gl';

export class NodesLayer {
    createLayer(nodes, settings) {
        return new ScatterplotLayer({
            id: 'nodes-layer',
            data: nodes,
            getPosition: d => d.geometry.coordinates,

            // Picking & AutoHighlight
            pickable: true,
            autoHighlight: true,
            highlightColor: [255, 255, 255, 255],

            // Node settings
            radiusUnits: 'meters',
            radiusScale: 3,
            radiusMinPixels: 1.5,
            getFillColor: d => [255, 255, 255, 255 * settings.pointOpacity],
            getRadius: d => settings.degreeBasedRadiusScale
                ? settings.pointRadius * Math.log(1 + d.properties.degree)
                : settings.pointRadius,

            // Node Border settings
            stroked: true,
            lineWidthUnits: 'meters',
            getLineWidth: d => settings.nodeBorderWidth,
            getLineColor: d => [0, 0, 0, 255 * settings.nodeBorderOpacity],


        });
    }
}
