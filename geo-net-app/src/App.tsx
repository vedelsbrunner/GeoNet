import React, {useMemo, useState} from 'react';
import usePublicJsonData, {Layouts, JsonFilePathsDictionary} from './hooks/useJsonData.tsx';
import GeoNetMap from "./components/map/GeoNetMap.tsx"
import {ChakraProvider, useMenu} from "@chakra-ui/react";

function App() {

    const dataSetsDictionary: JsonFilePathsDictionary = useMemo(() => ({
        [Layouts.Default]: 'mb-default.geojson',
        [Layouts.CircularClustered]: 'mb-circular-clustered.geojson',
        [Layouts.Circular]: 'mb-circular.geojson',
        [Layouts.Stacked]: 'mb-stacked.geojson',
        [Layouts.StackedClustered]: 'mb-stacked-clustered.geojson'
    }), []);

    const {dataSets, isLoading, error} = usePublicJsonData(dataSetsDictionary);


    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error loading data: {error.message}</div>;
    }

    return (
        <ChakraProvider>
            <GeoNetMap dataSets={dataSets}/>;
        </ChakraProvider>
    )
}

export default App;
