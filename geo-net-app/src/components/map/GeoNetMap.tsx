import {useEffect, useState} from 'react';
import DeckGL from 'deck.gl';
import {MapContext, NavigationControl, StaticMap} from 'react-map-gl';
import MapControls from '../controls/MapControls.tsx';
import {Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Box} from '@chakra-ui/react';
import {JsonFilePathsDictionary} from "../../hooks/useJsonData.tsx";
import GeoNetLayer from "../layers/GeoNetLayer.ts";

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
    const [layers, setLayers] = useState([]);
    const [settings, setSettings] = useState({
        lineWidthScale: 80,
        pointRadius: 1200,
        edgeWidth: 1,
        pointOpacity: 1,
        edgeOpacity: 0.2,
        degreeFilter: 0

    });

    useEffect(() => {
        const geonetLayers = Object.keys(dataSets).map(key => {
            const dataSet = dataSets[key];
            return new GeoNetLayer({
                id: `geonet-layer-${key}`,
                data: dataSet,
                ...settings,
            });
        });
        setLayers(geonetLayers);
    }, [dataSets]);

    const handleSettingsChange = (newSettings) => {
        console.log(newSettings)
        setSettings(prevSettings => ({...prevSettings, ...newSettings}));
    };

    return (
        <>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={layers}
                ContextProvider={MapContext.Provider}
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
