import GeoNetLayer from "./GeoNetLayer.ts";

//TODO: Remove data param is unnoetig
export const CreateGeoNetLayer = (selectedLayer, data, settings, onClick, onHover) => {
// @ts-ignore
    return new GeoNetLayer({
        id: `${selectedLayer}`,
        data: data,
        pickable: true,
        autoHighlight: true,
        ...settings,
        onClick: onClick,
        onHover: onHover,

    });
}
