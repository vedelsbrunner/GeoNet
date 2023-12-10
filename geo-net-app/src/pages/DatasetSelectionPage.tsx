import {useEffect, useMemo, useState} from 'react';
import {Box, Center, Radio, RadioGroup, Stack} from "@chakra-ui/react";
import usePublicJsonData, {JsonFilePathsDictionary, Layouts} from "../hooks/useJsonData.tsx";
import {useNavigate} from "react-router-dom";

export function DataSetSelectionPage() {
    const navigate = useNavigate();
    const [selectedDataSet, setSelectedDataSet] = useState('china');
    const dataSetDirectories = useMemo(() => ['china', 'jucs', 'marieboucher', 'smith'], []);
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

    const {layouts, isLoading, error} = usePublicJsonData(layoutSetDict[selectedDataSet]);

    const handleDataSetChange = (dataSet) => {
        setSelectedDataSet(dataSet);
        navigate('/map', {state: {layouts: layouts}});
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error loading data: {error.message}</div>;
    }

    return (
        <Center marginTop={150}>
            <Box>
                <RadioGroup onChange={handleDataSetChange} value={selectedDataSet}>
                    <Stack direction="column">
                        {dataSetDirectories.map(dataset => (
                            <Radio key={dataset} value={dataset}>{dataset}</Radio>
                        ))}
                    </Stack>
                </RadioGroup>
            </Box>
        </Center>

    );
}
