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
    const [selectedLayer, _setSelectedLayer] = useState(Layouts.Default);
    const selectedLayerRef = useRef(selectedLayer);
    const [hoverInfo, setHoverInfo] = useState(null);

    const [currentGeoNetLayer, setCurrentGeoNetLayer] = useState('');


    const [selectedNodes, _setSelectedNodes] = useState([]);
    const selectedNodesRef = useRef(selectedNodes);


    const [settings, setSettings] = useState({
        lineWidthScale: 500,
        pointRadius: 1500,
        pointOpacity: 1,
        edgeOpacity: 0.1,
        nodeBorderWidth: 800,
        nodeBorderOpacity: 1,
        degreeBasedRadiusScale: false,
        hullOverlapRemoval: false,
        showLabels: false,
        nodeSelectionActive: nodeSelectionActive
    });
    const [mapStyle, setMapStyle] = useState('mapbox://styles/multilingual-graz/clr8ultym002701pd38o83d83')

    useEffect(() => {
        const dataSource = selectedNodesRef.current.length > 0 ? selectedNodesRef.current : layouts[selectedLayer];
        console.log('Current datasource:')
        console.log(dataSource)
        // @ts-ignore
        const geonetLayer = new GeoNetLayer({
            id: `${selectedLayer}`,
            data: dataSource,
            pickable: true,
            autoHighlight: true,
            ...settings,
            onClick: onClick,
            onHover: onHover
        });
        setCurrentGeoNetLayer(geonetLayer);
    }, [layouts, settings, selectedLayer]);

    function setSelectedLayer(selectedLayer) {
        selectedLayerRef.current = selectedLayer;
        _setSelectedLayer(selectedLayer);
    }

    function setSelectedNodes(selectedNodes) {
        selectedNodesRef.current = selectedNodes;
        _setSelectedNodes(selectedNodes);
    }

    function onHover(info) {
        if (info.object) {
            console.log(info.object)
            setHoverInfo({
                x: info.x,
                y: info.y,
                properties: info.object.properties
            });
        } else {
            setHoverInfo(null);
        }
        if (info.object && info.object.geometry.type === 'Point') {
            const {neighbors, connecting_edges} = info.object.properties;
            const filteredData = layouts[selectedLayerRef.current].features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );

            if (selectedNodesRef.current.length > 0) {
                const newSelectedNodes = Array.from(new Set([...selectedNodesRef.current, ...filteredData]));
                updateLayer(selectedLayerRef.current, newSelectedNodes);
            } else {
                updateLayer(selectedLayerRef.current, filteredData)
            }

        } else if (selectedNodesRef.current.length === 0) {
            updateLayer(selectedLayerRef.current, layouts[selectedLayerRef.current]);
        }
    }

    function nodeSelectionActive()
    {
        return selectedNodesRef.current.length > 0
    }

    const handleMapStyleChange = (event) => {
        setMapStyle(event.target.value);
    };

    function onClick(info) {
        if (info.object && info.object.geometry.type === 'Point') {
            const {neighbors, connecting_edges} = info.object.properties;
            const filteredData = layouts[selectedLayerRef.current].features.filter(feature =>
                neighbors.includes(feature.properties.id) ||
                connecting_edges.includes(feature.properties.id) ||
                feature.properties.id === info.object.properties.id
            );

            const newSelectedNodes = Array.from(new Set([...selectedNodesRef.current, ...filteredData]));
            setSelectedNodes(newSelectedNodes);
            updateLayer(selectedLayerRef.current, selectedNodesRef.current);
        }
    }

    function handleSettingsChange(newSettings, layerIndex) {
        console.log(layerIndex)
        if (layerIndex !== undefined) {
            resetNodeSelection()
            setSelectedLayer(layerIndex);
        }
        setSettings(prevSettings => ({...prevSettings, ...newSettings}));
    }

    function resetNodeSelection() {
        updateLayer(selectedLayerRef.current, layouts[selectedLayerRef.current]);
        setSelectedNodes([])
    }

    function removeHullOverlap(removeOverlap: boolean) { //TODO: Move into own file..

        let newLayout;
        switch (selectedLayerRef.current) {
            case Layouts.SingleCircularClustered:
            case Layouts.NoOverlapSingleCircularClustered:
                newLayout = removeOverlap ? Layouts.NoOverlapSingleCircularClustered : Layouts.SingleCircularClustered;
                break;
            case Layouts.SingleCircular:
            case Layouts.NoOverlapSingleCircular:
                newLayout = removeOverlap ? Layouts.NoOverlapSingleCircular : Layouts.SingleCircular;
                break;
            case Layouts.DoubleCircularClustered:
            case Layouts.NoOverlapDoubleCircularClustered:
                newLayout = removeOverlap ? Layouts.NoOverlapDoubleCircularClustered : Layouts.DoubleCircularClustered;
                break;
            case Layouts.DoubleCircular:
            case Layouts.NoOverlapDoubleCircular:
                newLayout = removeOverlap ? Layouts.NoOverlapDoubleCircular : Layouts.DoubleCircular;
                break;
            case Layouts.Stacked:
            case Layouts.NoOverlapStacked:
                newLayout = removeOverlap ? Layouts.NoOverlapStacked : Layouts.Stacked;
                break;
            case Layouts.StackedClustered:
            case Layouts.NoOverlapStackedClustered:
                newLayout = removeOverlap ? Layouts.NoOverlapStackedClustered : Layouts.StackedClustered;
                break;
            case Layouts.Sunflower:
            case Layouts.NoOverlapSunflower:
                newLayout = removeOverlap ? Layouts.NoOverlapSunflower : Layouts.Sunflower;
                break;
            case Layouts.Grid:
            case Layouts.NoOverlapGrid:
                newLayout = removeOverlap ? Layouts.NoOverlapGrid : Layouts.Grid;
                break;
            case Layouts.SunflowerClustered:
            case Layouts.NoOverlapSunflowerClustered:
                newLayout = removeOverlap ? Layouts.NoOverlapSunflowerClustered : Layouts.SunflowerClustered;
                break;
            case Layouts.GridClustered:
            case Layouts.NoOverlapGridClustered:
                newLayout = removeOverlap ? Layouts.NoOverlapGridClustered : Layouts.GridClustered;
                break;
            default:
                newLayout = Layouts.Default;
                break;
        }

        updateLayer(newLayout, layouts[newLayout])
        setSelectedLayer(newLayout);
    }

    function updateLayer(layer, newFilteredData) {
        // @ts-ignore
        const filteredLayer = new GeoNetLayer({
            id: `${layer}`,
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
                {/*{*/}
                {/*    hoverInfo != null && hoverInfo.x != null && hoverInfo.y != null &&*/}

                {/*    <div style={{*/}
                {/*        position: 'absolute',*/}
                {/*        zIndex: 1,*/}
                {/*        pointerEvents: 'none',*/}
                {/*        padding: '10px',*/}
                {/*        background: 'rgba(255, 255, 255, 0.8)',*/}
                {/*        color: 'black',*/}
                {/*        maxWidth: '200px',*/}
                {/*        fontSize: '14px',*/}
                {/*        borderRadius: '4px',*/}
                {/*        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',*/}
                {/*        left: hoverInfo.x, top: hoverInfo.y*/}
                {/*    }}>*/}

                {/*        {Object.entries(hoverInfo.properties).map(([key, value]) => (*/}
                {/*            <div key={key}><strong>{key}</strong>: {value}</div>*/}
                {/*        ))}*/}
                {/*    </div>*/}
                {/*}*/}

                {
                    hoverInfo != null && hoverInfo.x != null && hoverInfo.y != null &&
                    (hoverInfo.properties.node_info || hoverInfo.properties.edge_info) &&
                    <div style={{
                        position: 'absolute',
                        zIndex: 1,
                        pointerEvents: 'none',
                        padding: '10px',
                        background: 'rgba(255, 255, 255, 0.8)',
                        color: 'black',
                        maxWidth: '200px',
                        fontSize: '14px',
                        borderRadius: '4px',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
                        left: hoverInfo.x, top: hoverInfo.y
                    }}>

                        {
                            hoverInfo.properties && hoverInfo.properties.node_info &&
                            <div key="node_info">{hoverInfo.properties.node_info}</div>
                        }

                        {
                            hoverInfo.properties && hoverInfo.properties.edge_info &&
                            <div key="edge_info">{hoverInfo.properties.edge_info}</div>
                        }
                    </div>
                }
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
            <GeoNetControls settings={settings} handleSettingsChange={handleSettingsChange} resetNodeSelection={resetNodeSelection} removeHullOverlap={removeHullOverlap}/>
        </>
    );
}

export default GeoNetMap;
