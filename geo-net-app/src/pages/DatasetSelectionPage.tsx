import {useEffect, useMemo, useState} from 'react';
import {Center, Flex, Grid, Text, useRadioGroup} from "@chakra-ui/react";
import usePublicJsonData, {JsonFilePathsDictionary, Layouts} from "../hooks/useJsonData.tsx";
import {useNavigate} from "react-router-dom";
import {RadioCard} from "../components/RadioCard.tsx";

export function DataSetSelectionPage() {
    const navigate = useNavigate();
    const [selectedDataSet, setSelectedDataSet] = useState('');
    const dataSetDirectories = useMemo(() => ['china', 'jucs', 'jucs_europe', 'marieboucher', 'smith', 'russia', 'russia_europe', 'russia_middle_east',
        // 'user_study_task1_1', 'user_study_task1_2', 'user_study_task1_3', 'user_study_task1_4', 'user_study_task1_5', 'user_study_task1_6',
        // 'user_study_task2_1', 'user_study_task2_2', 'user_study_task2_3', 'user_study_task2_4', 'user_study_task2_5', 'user_study_task2_6',
        // 'user_study_task3_1', 'user_study_task3_2', 'user_study_task3_3', 'user_study_task3_4', 'user_study_task3_5', 'user_study_task3_6'
        'user_study_task4_1', 'user_study_task4_2', 'user_study_task4_3', 'user_study_task4_4', 'user_study_task4_5', 'user_study_task4_6'
    ], []);
    const [userSelected, setUserSelected] = useState(false);
    const [layouts, setLayouts] = useState(null);

    const layoutSetDict: JsonFilePathsDictionary = useMemo(() => {
        const baseLayouts = {
            [Layouts.Default]: 'default.geojson',
            [Layouts.SingleCircularClustered]: 'single_circle-circular-clustered.geojson',
            [Layouts.NoOverlapSingleCircularClustered]: 'no-overlap-single_circle-circular-clustered.geojson',
            [Layouts.SingleCircular]: 'single_circle-circular.geojson',
            [Layouts.NoOverlapSingleCircular]: 'no-overlap-single_circle-circular.geojson',
            [Layouts.DoubleCircularClustered]: 'double_circle-circular-clustered.geojson',
            [Layouts.NoOverlapDoubleCircularClustered]: 'no-overlap-double_circle-circular-clustered.geojson',
            [Layouts.DoubleCircular]: 'double_circle-circular.geojson',
            [Layouts.NoOverlapDoubleCircular]: 'no-overlap-double_circle-circular.geojson',
            [Layouts.Stacked]: 'stacked.geojson',
            [Layouts.NoOverlapStacked]: 'no-overlap-stacked.geojson',
            [Layouts.StackedClustered]: 'stacked-clustered.geojson',
            [Layouts.NoOverlapStackedClustered]: 'no-overlap-stacked-clustered.geojson',
            [Layouts.Sunflower]: 'sunflower.geojson',
            [Layouts.NoOverlapSunflower]: 'no-overlap-sunflower.geojson',
            [Layouts.Grid]: 'grid.geojson',
            [Layouts.NoOverlapGrid]: 'no-overlap-grid.geojson',
            [Layouts.SunflowerClustered]: 'sunflower-clustered.geojson',
            [Layouts.NoOverlapSunflowerClustered]: 'no-overlap-sunflower-clustered.geojson',
            [Layouts.GridClustered]: 'grid-clustered.geojson',
            [Layouts.NoOverlapGridClustered]: 'no-overlap-grid-clustered.geojson'

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
