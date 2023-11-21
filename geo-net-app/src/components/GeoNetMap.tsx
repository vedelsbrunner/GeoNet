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
    const [selectedLayerIndex, setSelectedLayerIndex] = useState(1);
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

        const mbDefault = new GeoJsonLayer({
            id: 'geojson-layer',
            data: data[0],
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: (feature) => {
                if (feature.geometry.type === 'Point') {
                    return [0, 0, 0, settings.pointOpacity * 255];
                } else if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                    return [149, 200, 216, 50];
                }
                // Default color, if needed
                return [255, 255, 255, 255];
            },
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],
        });

        const mbCircular = new GeoJsonLayer({
            id: 'geojson-layer',
            data: data[2],
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: (feature) => {
                if (feature.geometry.type === 'Point') {
                    return [0, 0, 0, settings.pointOpacity * 255];
                } else if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                    return [149, 200, 216, 50];
                }
                // Default color, if needed
                return [255, 255, 255, 255];
            },
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],
        });

        const mbCircularClustered = new GeoJsonLayer({
            id: 'geojson-layer',
            data: data[1],
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: (feature) => {
                if (feature.geometry.type === 'Point') {
                    return [0, 0, 0, settings.pointOpacity * 255];
                } else if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                    return [149, 200, 216, 50];
                }
                // Default color, if needed
                return [255, 255, 255, 255];
            },
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],
        });

        const mbStacked = new GeoJsonLayer({
            id: 'geojson-layer',
            data: data[3],
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: (feature) => {
                if (feature.geometry.type === 'Point') {
                    return [0, 0, 0, settings.pointOpacity * 255];
                } else if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                    return [149, 200, 216, 50];
                }
                // Default color, if needed
                return [255, 255, 255, 255];
            },
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],
        });

        const mbStackedClustered = new GeoJsonLayer({
            id: 'geojson-layer',
            data: data[4],
            filled: true,
            getPointRadius: settings.pointRadius,
            pickable: true,
            autoHighlight: true,
            extruded: true,
            lineWidthScale: settings.lineWidthScale,
            lineWidthMinPixels: 1,
            getFillColor: (feature) => {
                if (feature.geometry.type === 'Point') {
                    return [0, 0, 0, settings.pointOpacity * 255];
                } else if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                    return [149, 200, 216, 50];
                }
                // Default color, if needed
                return [255, 255, 255, 255];
            },
            getLineColor: [0, 0, 0, settings.edgeOpacity * 250],
        });

        setLayers([mbDefault, mbCircular, mbCircularClustered, mbStacked, mbStackedClustered].filter((_, index) => index === selectedLayerIndex));
    }, [data, settings, selectedLayerIndex]);

    const handleSettingsChange = (newSettings, layerIndex) => {
        if (layerIndex !== undefined) {
            setSelectedLayerIndex(layerIndex);
        }
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
