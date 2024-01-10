import {useLocation} from "react-router-dom";
import GeoNetMap from "../components/map/GeoNetMap.tsx";

export function GeoNetMapPage() {
    const location = useLocation();
    const layouts = location.state.layouts;
    return (
        <GeoNetMap layouts={layouts}/>
    )
}