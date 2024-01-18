import {Select, Box} from '@chakra-ui/react';
import React, {useEffect, useRef, useState} from 'react';
import DeckGL from 'deck.gl';
import {Map} from 'react-map-gl';
import {JsonFilePathsDictionary, Layouts} from "../../hooks/useJsonData.tsx";
import GeoNetLayer from "../../layers/GeoNetLayer.ts";
import GeoNetControls from "../controls/GeoNetControls.tsx";
import {INITIAL_VIEW_STATE, MAP_STYLE, MAPBOX_ACCESS_TOKEN} from "./MAP_STYLE.tsx";

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
        nodeBorderOpacity: 1,
        degreeBasedRadiusScale: false
    });
    const [selectedNodes, _setSelectedNodes] = useState([]);
    const selectedNodesRef = useRef(selectedNodes);
    const [mapStyle, setMapStyle] = useState('mapbox://styles/multilingual-graz/clr8ultym002701pd38o83d83')

    useEffect(() => {
        const geonetLayer = new GeoNetLayer({
            id: `${selectedLayer}`,
            data: layouts[selectedLayer],
            pickable: true,
            autoHighlight: true,
            ...settings,
            onClick: onClick,
            onHover: onHover
        });
        setCurrentGeoNetLayer(geonetLayer);
    }, [layouts, settings, selectedLayer]);

    function setSelectedNodes(selectedNodes) {
        selectedNodesRef.current = selectedNodes;
        _setSelectedNodes(selectedNodes);
    }

    function onHover(info) {
        if (info.object && info.object.geometry.type === 'Point') {
            const {neighbors, connecting_edges} = info.object.properties;
            const filteredData = layouts[selectedLayer].features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );

            if (selectedNodesRef.current.length > 0) {
                const newSelectedNodes = Array.from(new Set([...selectedNodesRef.current, ...filteredData]));
                updateLayer(selectedLayer, newSelectedNodes);
            } else {
                updateLayer(selectedLayer, filteredData)
            }

        } else if (selectedNodesRef.current.length === 0) {
            updateLayer(selectedLayer, layouts[selectedLayer]);
        }
    }

    const handleMapStyleChange = (event) => {
        setMapStyle(event.target.value);
    };

    function onClick(info) {
        if (info.object && info.object.geometry.type === 'Point') {
            const {neighbors, connecting_edges} = info.object.properties;
            const filteredData = layouts[selectedLayer].features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );

            const newSelectedNodes = Array.from(new Set([...selectedNodesRef.current, ...filteredData]));
            setSelectedNodes(newSelectedNodes);
            updateLayer(selectedLayer, selectedNodesRef.current);
        }
    }

    function handleSettingsChange(newSettings, layerIndex) {
        if (layerIndex !== undefined) {
            setSelectedLayer(layerIndex);
        }
        setSettings(prevSettings => ({...prevSettings, ...newSettings}));
    }

    function resetNodeSelection() {
        console.log('Resetting node selection to whole geoNetwork..')
        updateLayer(selectedLayer, layouts[selectedLayer]);
        setSelectedNodes([])
    }

    function updateLayer(selectedLayer, newFilteredData) {
        const filteredLayer = new GeoNetLayer({
            id: `${selectedLayer}`,
            data: newFilteredData,
            pickable: true,
            autoHighlight: true,
            ...settings,
            onClick: onClick,
            onHover: onHover
        });
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
                    mapStyle={mapStyle}
                />
            </DeckGL>
            <Box position="absolute" top={4} left={4} zIndex="1" color={'black'}>
                <Select
                    onChange={handleMapStyleChange}
                    size="sm"
                    variant="filled"
                    width="auto"
                    bgColor="rgb(45, 55, 72)"
                >
                    <option value="mapbox://styles/multilingual-graz/clr8ultym002701pd38o83d83">Default</option>
                    <option value='mapbox://styles/multilingual-graz/clrht8uk600kw01pdhmjc8u0g'>Distorted 50%</option>
                    <option value='mapbox://styles/multilingual-graz/clrirf57300m701pehf0t2aqd'>Distorted 100%</option>
                </Select>
            </Box>
            <GeoNetControls settings={settings} handleSettingsChange={handleSettingsChange} resetNodeSelection={resetNodeSelection}/>
        </>
    );
}

export default GeoNetMap;
