import {GeoJsonLayer} from '@deck.gl/layers';
import {getFillColor} from "./GetFillColor.ts";
import {getLineColor} from "./GetLineColor.ts";
import {getLineWidth} from "./GetLineWidth.ts";


export const createGeoNetLayer = (id, data, settings, updateLayer) => {
    const onClick = (info) => {
        console.log('clicked')
        console.log(info)
        if (info.object) {
            const neighbors = info.object.properties.neighbors;
            const connectingEdges = info.object.properties.connecting_edges;
            const filteredData = data.features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connectingEdges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );

            // Call the updateLayer function passed in props with the new filtered data
            updateLayer(id, filteredData);
        }
    };


    const layer = new GeoJsonLayer({
        id: id,
        data: data,
        autoHighlight: true,
        pickable: true,
        highlightColor: [255, 255, 255, 155],
        getLineColor: getLineColor,
        getFillColor: getFillColor,
        lineWidthScale: 2,
        pointType: 'circle',
        lineWidthMinPixels: 2,
        extruded: true,
        pointRadiusScale: 10,
        pointRadiusMinPixels: 1,
        pointRadiusMaxPixels: 150,
        getPointRadius: d => 150,
        getLineWidth: getLineWidth,
        onClick: onClick
    });

    return layer;
}
