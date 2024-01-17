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

    function setSelectedNodes(selectedNodes) {
        selectedNodesRef.current = selectedNodes;
        _setSelectedNodes(selectedNodes);
    }

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

    function onHover(info) {
        if (info.object && info.object.geometry.type === 'Point') {
            const {neighbors, connecting_edges} = info.object.properties;
            const filteredData = layouts[selectedLayer].features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );
            updateLayer(selectedLayer, filteredData);
        } else if (selectedNodesRef.current.length === 0) {
            updateLayer(selectedLayer, layouts[selectedLayer]);
        }
    }

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
                    mapStyle={MAP_STYLE}
                />
            </DeckGL>
            <GeoNetControls settings={settings} handleSettingsChange={handleSettingsChange} resetNodeSelection={resetNodeSelection}/>
        </>
    );
}

export default GeoNetMap;
