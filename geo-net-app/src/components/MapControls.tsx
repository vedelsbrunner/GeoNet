import {Box, Divider, FormLabel, HStack, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Text} from '@chakra-ui/react';
import React, {useState} from "react";

function MapControls({settings, onChange}) {
    const [lineWidthScale, setLineWidthScale] = useState(settings.lineWidthScale);
    const [pointOpacity, setPointOpacity] = useState(settings.pointOpacity);
    const [edgeOpacity, setEdgeOpacity] = useState(settings.edgeOpacity);
    const [pointRadius, setPointRadius] = useState(settings.pointRadius);
    const [edgeWidth, setEdgeWidth] = useState(settings.edgeWidth);
    const [degreeFilter, setDegreeFilter] = useState(settings.degreeFilter);

    const handleLineWidthChange = (value) => {
        setLineWidthScale(value);
        onChange({...settings, lineWidthScale: value});
    };

    const handlePointOpacityChange = (value) => {
        setPointOpacity(value);
        console.log(value)
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

    const handleEdgeWidthChange = (value) => {
        setEdgeWidth(value);
        onChange({...settings, edgeWidth: value});
    };

    const handleDegreeFilterChange = (value) => {
        setDegreeFilter(value);
        onChange({...settings, degreeFilter: value});
    };

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
                <Slider id='point-radius' value={pointRadius} min={0} max={5000} onChange={handlePointRadiusChange}>
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
                <Slider id='line-width-scale' value={lineWidthScale} min={0} max={2500} onChange={handleLineWidthChange}>
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
        </Box>
    );
}

export default MapControls;
