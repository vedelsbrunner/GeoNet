import {useEffect, useState} from 'react';
import DeckGL from 'deck.gl';
import {MapContext, NavigationControl, StaticMap} from 'react-map-gl';
import {GeoJsonLayer} from '@deck.gl/layers';
import MapControls from './MapControls.tsx';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box
} from '@chakra-ui/react';

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json';
const NAV_CONTROL_STYLE = {
    position: 'absolute',
    top: 10,
    left: 10
};

function GeoNetMap({initialViewState, data}) {
    const [layers, setLayers] = useState([]);
    const [filteredData, setFilteredData] = useState(data);

    const [settings, setSettings] = useState({
        lineWidthScale: 80,
        pointRadius: 800,
        edgeWidth: 1,
        pointOpacity: 0.1,
        edgeOpacity: 1,
        degreeFilter: 0

    });

    useEffect(() => {
        const filteredData = {
            ...data,
            features: data.features.filter(feature => {
                // Apply the filter only if the feature is a point and it has a degree property
                return feature.geometry.type === 'Point'
                    ? settings.degreeFilter === 0 || feature.properties.degree === settings.degreeFilter
                    : true;
            })
        };
        const geoJsonLayer = new GeoJsonLayer({
            id: 'geojson-layer',
            data: filteredData,
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: [0, 0, 0, settings.pointOpacity * 250],
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],

        });
        setLayers([geoJsonLayer]);
    }, [filteredData, settings]);

    const handleSettingsChange = (newSettings) => {
        console.log("handleSettingsChange....")
        setSettings((prevSettings) => ({...prevSettings, ...newSettings}));

    };

    return (
        <>
            <DeckGL
                initialViewState={initialViewState}
                controller={true}
                layers={layers}
                ContextProvider={MapContext.Provider}
            >
                <StaticMap mapStyle={MAP_STYLE}/>
                <NavigationControl style={NAV_CONTROL_STYLE}></NavigationControl>
            </DeckGL>
            <Box position="absolute" top={1} right={1}>
                <Accordion allowToggle>
                    <AccordionItem>
                        <AccordionButton>
                            <Box flex="1" textAlign="left">
                                Map Controls
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                        <AccordionPanel>
                            <MapControls settings={settings} onChange={handleSettingsChange} />
                        </AccordionPanel>
                    </AccordionItem>
                </Accordion>
            </Box>
        </>
    );
}

export default GeoNetMap;
