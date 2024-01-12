import {useEffect, useState} from 'react';
import DeckGL from 'deck.gl';
import {NavigationControl, Map} from 'react-map-gl';
import {JsonFilePathsDictionary, Layouts} from "../../hooks/useJsonData.tsx";
import {CreateGeoNetLayer} from "../../layers/GeoNetLayerCreator.ts";
import GeoNetControls from "../controls/GeoNetControls.tsx";
import {INITIAL_VIEW_STATE, MAP_STYLE, MAPBOX_ACCESS_TOKEN, NAV_CONTROL_STYLE} from "./MAP_STYLE.tsx";

interface GeoNetMapProps {
    layouts: JsonFilePathsDictionary;
}

function GeoNetMap({layouts}: GeoNetMapProps) {
    const [selectedLayer, setSelectedLayer] = useState(Layouts.Default);
    const [currentGeoNetLayer, setCurrentGeoNetLayer] = useState('');
    const [settings, setSettings] = useState({
        lineWidthScale: 600,
        pointRadius: 600,
        pointOpacity: 1,
        edgeOpacity: 0.4,
        nodeBorderWidth: 800,
        nodeBorderOpacity: 1
    });
    useEffect(() => {
        const selectedDataSet = layouts[selectedLayer];
        const geonetLayer = CreateGeoNetLayer(selectedLayer, selectedDataSet, settings, updateLayer, layouts);
        setCurrentGeoNetLayer(geonetLayer);
    }, [layouts, settings, selectedLayer]);

    const handleSettingsChange = (newSettings, layerIndex) => {
        console.log('handleSettingsChange', newSettings, layerIndex)
        if (layerIndex !== undefined) {
            setSelectedLayer(layerIndex);
        }
        setSettings(prevSettings => ({...prevSettings, ...newSettings}));
    };

    function updateLayer(selectedLayer, newFilteredData) {
        const filteredLayer = CreateGeoNetLayer(selectedLayer, newFilteredData, settings, updateLayer, layouts);
        setCurrentGeoNetLayer(filteredLayer);
    }


    return (
        <>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={currentGeoNetLayer}
            >
                <Map
                    mapboxAccessToken={MAPBOX_ACCESS_TOKEN}
                    mapStyle={MAP_STYLE}
                />
                {/*<NavigationControl style={NAV_CONTROL_STYLE}/>*/}
            </DeckGL>
            <GeoNetControls settings={settings} handleSettingsChange={handleSettingsChange}></GeoNetControls>
        </>
    );
}

export default GeoNetMap;
