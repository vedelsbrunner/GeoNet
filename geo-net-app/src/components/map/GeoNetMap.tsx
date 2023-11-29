import {useEffect, useState} from 'react';
import DeckGL from 'deck.gl';
import {MapContext, NavigationControl, StaticMap} from 'react-map-gl';
import MapControls from '../controls/MapControls.tsx';
import {Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Box} from '@chakra-ui/react';
import {JsonFilePathsDictionary, Layouts} from "../../hooks/useJsonData.tsx";
import GeoNetLayer from "../../layers/GeoNetLayer.ts";
import {CreateGeoNetLayer} from "../../layers/GeoNetLayerCreator.ts";

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json';
const NAV_CONTROL_STYLE = {
    position: 'absolute',
    top: 10,
    left: 10
};
const INITIAL_VIEW_STATE = {
    latitude: 51.47,
    longitude: 0.45,
    zoom: 4,
    bearing: 1,
    pitch: 0
};

interface GeoNetMapProps {
    initialViewState: any;
    dataSets: JsonFilePathsDictionary;
}

function GeoNetMap({initialViewState, dataSets}: GeoNetMapProps) {
    const [selectedLayer, setSelectedLayer] = useState(Layouts.Default);
    const [layers, setLayers] = useState([]); //TODO: Always a single value never a list...!
    const [settings, setSettings] = useState({
        lineWidthScale: 600,
        pointRadius: 300,
        pointOpacity: 0.6,
        edgeOpacity: 0.2,
        degreeFilter: 0
    });

    // Reset dataset from all filters
    const handleMapClick = (info) => {
        if (!info.object) {
            const selectedDataSet = dataSets[selectedLayer];
            const geonetLayer = CreateGeoNetLayer(selectedLayer, selectedDataSet, settings, updateLayer);
            setLayers(geonetLayer);
        }
    };

    function updateLayer(id, newFilteredData) {
        console.log(id)
        console.log(newFilteredData)
        const filteredLayer = CreateGeoNetLayer(id, newFilteredData, settings, updateLayer);
        setLayers(filteredLayer);
    }

    useEffect(() => {
        const selectedDataSet = dataSets[selectedLayer];
        const geonetLayer = CreateGeoNetLayer(selectedLayer, selectedDataSet, settings, updateLayer);
        setLayers(geonetLayer);
    }, [dataSets, settings, selectedLayer]);

    const handleSettingsChange = (newSettings, layerIndex) => {
        console.log('handleSettingsChange', newSettings, layerIndex)
        if (layerIndex !== undefined) {
            setSelectedLayer(layerIndex);
        }
        setSettings(prevSettings => ({...prevSettings, ...newSettings}));
    };

    return (
        <>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={layers}
                ContextProvider={MapContext.Provider}
                onClick={handleMapClick}

            >
                <StaticMap mapStyle={MAP_STYLE}/>
                <NavigationControl style={NAV_CONTROL_STYLE}/>
            </DeckGL>
            <Box position="absolute" top={1} right={1}>
                <Accordion allowToggle>
                    <AccordionItem>
                        <AccordionButton>
                            <Box flex="1" textAlign="left">
                                Map Controls
                            </Box>
                            <AccordionIcon/>
                        </AccordionButton>
                        <AccordionPanel>
                            <MapControls settings={settings} onChange={handleSettingsChange}/>
                        </AccordionPanel>
                    </AccordionItem>
                </Accordion>
            </Box>
        </>
    );
}

export default GeoNetMap;
