import {Box, Divider, FormLabel, HStack, Button, Select, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Text, Checkbox} from '@chakra-ui/react';
import {useRef, useState} from "react";
import {Layouts} from "../../hooks/useJsonData.tsx";

function MapControls({settings, onChange, onResetNodeSelection, removeHullOverlap}) {
    const [lineWidthScale, setLineWidthScale] = useState(settings.lineWidthScale);
    const [pointOpacity, setPointOpacity] = useState(settings.pointOpacity);
    const [edgeOpacity, setEdgeOpacity] = useState(settings.edgeOpacity);
    const [pointRadius, setPointRadius] = useState(settings.pointRadius);
    const [nodeBorderWidth, setNodeBorderWidth] = useState(settings.nodeBorderWidth);
    const [nodeBorderOpacity, setNodeBorderOpacity] = useState(settings.nodeBorderOpacity);
    const [edgeWidth, setEdgeWidth] = useState(settings.edgeWidth);
    const [degreeFilter, setDegreeFilter] = useState(settings.degreeFilter);
    const [degreeBasedRadiusScale, setDegreeBasedRadiusScale] = useState(settings.degreeBasedRadiusScale);

    const [hullOverlapRemoval, _setHullOverlapRemoval] = useState(settings.hullOverlapRemoval)
    const hullOverlapRemovalRef = useRef(hullOverlapRemoval);
    const setHullOverlapRemoval= (removeOverlap: boolean) => {
        hullOverlapRemovalRef.current = removeOverlap;
        _setHullOverlapRemoval(removeOverlap);
    }

    const handleLineWidthChange = (value) => {
        setLineWidthScale(value);
        onChange({...settings, lineWidthScale: value});
    };
    const handleLayerSelectionChange = (event) => {
        const layerIndex = event.target.value;
        onChange(settings, layerIndex);
        console.log('Hull removal?')
        console.log(hullOverlapRemovalRef.current)
        removeHullOverlap(hullOverlapRemovalRef.current);
    };

    const handleHullOverlapRemoval = (value) => {
        console.log('Hull overlap remove..')
        const isChecked = value.target.checked;
        setHullOverlapRemoval(isChecked)
        removeHullOverlap(isChecked)
    }

    const handlePointOpacityChange = (value) => {
        setPointOpacity(value);
        onChange({...settings, pointOpacity: value});
    };

    const handleEdgeOpacityChange = (value) => {
        setEdgeOpacity(value);
        onChange({...settings, edgeOpacity: value});
    };

    const handlePointRadiusChange = (value) => {
        setPointRadius(value);
        onChange({...settings, pointRadius: value});
    };

    const handleNodeBorderWidthChange = (value) => {
        setNodeBorderWidth(value);
        onChange({...settings, nodeBorderWidth: value})
    }

    const handleNodeBorderOpacityChange = (value) => {
        setNodeBorderOpacity(value);
        onChange({...settings, nodeBorderOpacity: value})
    }

    const handleDegreeBasedRadiusScale = (value) => {
        const isChecked = value.target.checked;
        setDegreeBasedRadiusScale(isChecked);
        onChange({...settings, degreeBasedRadiusScale: isChecked})
    }

    const handleResetNodeSelection = () => {
        onResetNodeSelection();
    }


    return (
        <Box position="absolute" width={250} color="white" bg="gray.700" boxShadow="base" right={10} p={4} fontSize="sm">
            <Select onChange={handleLayerSelectionChange} bg={"gray"} color={"black"}>
                <optgroup label="Standard Layouts">
                    <option value={Layouts.Default}>Default</option>
                    <option value={Layouts.Stacked}>Stacked</option>
                    <option value={Layouts.SingleCircular}>Single Circular</option>
                    <option value={Layouts.DoubleCircular}>Double Circular</option>
                    <option value={Layouts.Sunflower}>Sunflower</option>
                    <option value={Layouts.Grid}>Grid</option>
                </optgroup>
                <optgroup label="Clustered Layouts">
                    <option value={Layouts.StackedClustered}>Stacked Clustered</option>
                    <option value={Layouts.SingleCircularClustered}>Single Circular Clustered</option>
                    <option value={Layouts.DoubleCircularClustered}>Double Circular Clustered</option>
                    <option value={Layouts.SunflowerClustered}>Sunflower Clustered</option>
                    <option value={Layouts.GridClustered}>Grid Clustered</option>
                </optgroup>
            </Select>
            <Divider
                mt={4}
                mb={2}
            />
            <Text
                fontWeight={300}
                fontSize={18}
            >
                Nodes
            </Text>
            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='point-radius'>Radius</FormLabel>
                <Slider id='point-radius' value={pointRadius} min={1} max={1500} onChange={handlePointRadiusChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>
            <HStack justifyContent="space-between" mt={1}>
                <Checkbox
                    id='enable-degree-based-radius-scale'
                    onChange={handleDegreeBasedRadiusScale}>
                    Degree-scaled radius
                </Checkbox>
            </HStack>

            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='point-opacity'>Opacity</FormLabel>
                <Slider id='point-opacity' value={pointOpacity} min={0} max={1} step={0.01} onChange={handlePointOpacityChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>
            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='node-border-width'>Border width</FormLabel>
                <Slider id='node-border-width' value={nodeBorderWidth} min={0} max={2000} step={10} onChange={handleNodeBorderWidthChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>
            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='node-border-opacity'>Border opacity</FormLabel>
                <Slider id='node-border-opacity' value={nodeBorderOpacity} min={0} max={1} step={0.1} onChange={handleNodeBorderOpacityChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>

            <Divider
                mt={2}
                mb={2}
            />

            <Text
                fontWeight={300}
                fontSize={18}
            >
                Edges
            </Text>
            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='line-width-scale'>Width</FormLabel>
                <Slider id='line-width-scale' value={lineWidthScale} min={0} max={3000} onChange={handleLineWidthChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>

            <HStack justifyContent="space-between" mt={1}>
                <FormLabel htmlFor='edge-opacity'>Opacity</FormLabel>
                <Slider id='edge-opacity' value={edgeOpacity} min={0} max={1} step={0.01} onChange={handleEdgeOpacityChange}>
                    <SliderTrack>
                        <SliderFilledTrack/>
                    </SliderTrack>
                    <SliderThumb/>
                </Slider>
            </HStack>

            <Divider
                mt={2}
                mb={2}
            />

            <Text
                fontWeight={300}
                fontSize={18}
            >
                Layouts
            </Text>

            <HStack justifyContent="space-between" mt={1}>
                <Checkbox
                    id='enable-hull-overlap-removal'
                    onChange={handleHullOverlapRemoval}>
                    Overlapping clusters removal
                </Checkbox>
            </HStack>

            <Divider
                mt={2}
                mb={2}
            />

            <HStack justifyContent="space-between" mt={1}>
                <Button
                    id='reset-node-selection'
                    onClick={handleResetNodeSelection}
                    size="sm"
                    colorScheme="blue"
                >
                    Reset Node Selection
                </Button>
            </HStack>


        </Box>
    );
}

export default MapControls;
