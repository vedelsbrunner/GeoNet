import {Box, Divider, FormLabel, HStack, Select, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Text} from '@chakra-ui/react';
import {useState} from "react";
import {Layouts} from "../../hooks/useJsonData.tsx";

function MapControls({settings, onChange}) {
    const [lineWidthScale, setLineWidthScale] = useState(settings.lineWidthScale);
    const [pointOpacity, setPointOpacity] = useState(settings.pointOpacity);
    const [edgeOpacity, setEdgeOpacity] = useState(settings.edgeOpacity);
    const [pointRadius, setPointRadius] = useState(settings.pointRadius);
    const [nodeBorderWidth, setNodeBorderWidth] = useState(settings.nodeBorderWidth);
    const [nodeBorderOpacity, setNodeBorderOpacity] = useState(settings.nodeBorderOpacity);
    const [edgeWidth, setEdgeWidth] = useState(settings.edgeWidth);
    const [degreeFilter, setDegreeFilter] = useState(settings.degreeFilter);

    const handleLineWidthChange = (value) => {
        setLineWidthScale(value);
        onChange({...settings, lineWidthScale: value});
    };
    const handleLayerSelectionChange = (event) => {
        const layerIndex = event.target.value;
        console.log('layerIndex', layerIndex);
        onChange(settings, layerIndex);
    };

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

    return (
        <Box position="absolute" width={250} color="white" bg="gray.700" boxShadow="base" right={10} p={4} fontSize="sm">
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
            ></Divider>
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

            <Text fontSize={18} mt={4}>Layers</Text>
            <Select onChange={handleLayerSelectionChange} bg={"gray"} color={"black"}>
                <option value={Layouts.Default}>Default Layout</option>
                <option value={Layouts.Stacked}>Stacked Layout</option>
                <option value={Layouts.Circular}>Circular Layout</option>
                <option value={Layouts.Sunflower}>Sunflower Layout</option>
                <option value={Layouts.Grid}>Grid Layout</option>
                <option value={Layouts.StackedClustered}>Stacked Clustered Layout</option>
                <option value={Layouts.CircularClustered}>Circular Clustered Layout</option>
                <option value={Layouts.SunflowerClustered}>Sunflower Clustered Layout</option>
                <option value={Layouts.GridClustered}>Grid Clustered Layout</option>
            </Select>
        </Box>
    );
}

export default MapControls;
