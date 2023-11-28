import GeoNetLayer from "./GeoNetLayer.ts";

export const CreateGeoNetLayer = (id, data, settings, updateLayer) => {
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

            console.log('Newly filtered data:', filteredData)
            updateLayer(id, filteredData);
        }
    };

    // @ts-ignore
    return new GeoNetLayer({
        id: `${id}`,
        data: data,
        pickable: true,
        autoHighlight: true,
        ...settings,
        // onHover: info => console.log('hovered:', info),
        onClick: onClick,
    });
}