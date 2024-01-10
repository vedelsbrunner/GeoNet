import GeoNetLayer from "./GeoNetLayer.ts";

export const CreateGeoNetLayer = (selectedLayer, data, settings, updateLayer, layouts) => {
    const onHover = (info) => {
        if (info.object) {
            const {neighbors, connecting_edges} = info.object.properties;
            if (!neighbors || !connecting_edges) {
                console.log("Null or undefined data encountered", {neighbors, connecting_edges});

                return;
            }
            const filteredData = data.features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );
            updateLayer(selectedLayer, filteredData);
        } else {
            console.log('OnHove ended')
            console.log(selectedLayer, layouts[selectedLayer])
            updateLayer(selectedLayer, layouts[selectedLayer]);
        }
    };


    // @ts-ignore
    return new GeoNetLayer({
        id: `${selectedLayer}`,
        data: data,
        pickable: true,
        autoHighlight: true,
        ...settings,
        onHover: onHover
    });
}