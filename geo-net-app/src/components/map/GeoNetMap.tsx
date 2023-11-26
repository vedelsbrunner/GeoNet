import {useEffect, useState} from 'react';
import DeckGL from 'deck.gl';
import {MapContext, NavigationControl, StaticMap} from 'react-map-gl';
import MapControls from '../controls/MapControls.tsx';
import {Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Box} from '@chakra-ui/react';
import {JsonFilePathsDictionary} from "../../hooks/useJsonData.tsx";
import {createGeoNetLayer} from "../layers/GeoNetLayer.ts";
import {INITIAL_VIEW_STATE, MAP_STYLE, NAV_CONTROL_STYLE} from "./consts.tsx";

interface GeoNetMapProps {
    dataSets: JsonFilePathsDictionary;
}

function GeoNetMap({dataSets}: GeoNetMapProps) {
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
            console.log('Creating layer for ' + key)
            const layer = createGeoNetLayer(key, dataSets[key], settings)
            return layer;
        });
        setLayers(geonetLayers);
    }, [dataSets, settings]);

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
