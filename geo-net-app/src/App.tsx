import React, {useState} from 'react';
import usePublicJsonData from './hooks/useJsonData.tsx';
import GeoNetMap from "./components/GeoNetMap.tsx"
import {ChakraProvider} from '@chakra-ui/react';

function App() {

    const {data, isLoading, error} = usePublicJsonData('mb-circular.geojson');
    const [initialViewState] = useState({
        latitude: 51.47,
        longitude: 0.45,
        zoom: 4,
        bearing: 1,
        pitch: 0
    });

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error loading data: {error.message}</div>;
    }

    return (
        <ChakraProvider>
            <GeoNetMap initialViewState={initialViewState} data={data}/>;
        </ChakraProvider>
    )
}

export default App;
