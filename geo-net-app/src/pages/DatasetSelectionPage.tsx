import {useEffect, useMemo, useState} from 'react';
import {Center, Flex, Grid, Text, useRadioGroup} from "@chakra-ui/react";
import usePublicJsonData, {JsonFilePathsDictionary, Layouts} from "../hooks/useJsonData.tsx";
import {useNavigate} from "react-router-dom";
import {RadioCard} from "../components/RadioCard.tsx";

export function DataSetSelectionPage() {
    const navigate = useNavigate();
    const [selectedDataSet, setSelectedDataSet] = useState('');
    const dataSetDirectories = useMemo(() => ['china', 'jucs', 'marieboucher', 'smith'], []);
    const [userSelected, setUserSelected] = useState(false);
    const [layouts, setLayouts] = useState(null);

    const layoutSetDict: JsonFilePathsDictionary = useMemo(() => {
        const baseLayouts = {
            [Layouts.Default]: 'default.geojson',
            [Layouts.CircularClustered]: 'circular-clustered.geojson',
            [Layouts.Circular]: 'circular.geojson',
            [Layouts.Stacked]: 'stacked.geojson',
            [Layouts.StackedClustered]: 'stacked-clustered.geojson'
        };
        const datasetLayouts = {};
        dataSetDirectories.forEach(dataset => {
            datasetLayouts[dataset] = {};
            Object.keys(baseLayouts).forEach(layout => {
                datasetLayouts[dataset][layout] = `${dataset}/${baseLayouts[layout]}`;
            });
        });
        return datasetLayouts;
    }, [dataSetDirectories]);


    const {isLoading, error} = usePublicJsonData(layoutSetDict[selectedDataSet], setLayouts);

    useEffect(() => {
        if (userSelected && !isLoading && layouts && !error) {
            console.log('Navigating with layouts:', layouts);
            navigate('/map', {state: {layouts: layouts}});
        }
    }, [layouts]);


    const handleDataSetChange = (dataSet) => {
        // Reset layouts to null to force navigation /map hook to wait for the newly selected dataset
        setLayouts(null)
        setSelectedDataSet(dataSet);
        setUserSelected(true)
    };
    const {getRootProps, getRadioProps} = useRadioGroup({
        name: 'dataSet',
        onChange: handleDataSetChange,
    });

    const group = getRootProps();
    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error loading data: {error.message}</div>;
    }

    return (
        <Center marginTop={10}>
            <Flex direction='column' align='center' justify='center'>
                <Grid templateColumns='repeat(2, 1fr)' gap={6} {...group}>
                    {dataSetDirectories.map((dataset) => {
                        const radio = getRadioProps({value: dataset});
                        return (
                            <RadioCard key={dataset} {...radio}>
                                <Text fontWeight='bold'>{dataset}</Text>
                                <Text fontSize='sm'>Description of {dataset}</Text>
                            </RadioCard>
                        );
                    })}
                </Grid>
            </Flex>
        </Center>
    );
}