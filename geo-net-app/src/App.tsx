import {HashRouter as Router, Route, Routes} from "react-router-dom";
import {ChakraProvider} from "@chakra-ui/react";
import {DataSetSelectionPage} from "./pages/DatasetSelectionPage.tsx";
import {GeoNetMapPage} from "./pages/GeoNetMapPage.tsx";
import 'mapbox-gl/dist/mapbox-gl.css';

function App() {


    return (
        <ChakraProvider>
            <Router>
                <Routes>
                    <Route index element={<DataSetSelectionPage/>}/>
                    <Route path="map" element={<GeoNetMapPage/>}/>
                </Routes>
            </Router>
        </ChakraProvider>
    )
}

export default App;
