import {CompositeLayer} from 'deck.gl';
import {NodesLayer} from "./NodesLayer.ts";
import {EdgesLayer} from "./EdgesLayer.ts";
import {HullsLayer} from "./HullsLayer.ts";
import {ExtractDataLayers} from "./DataExtractor.ts";
import {LabelsLayer} from "./LabelsLayer.ts";
import {CircularHullLayer} from "./CircularHullLayer.ts";

export default class GeoNetLayer extends CompositeLayer {

    renderLayers() {
        const {nodes, edges, hulls, location_labels, circluar_hulls} = ExtractDataLayers(this.props.data)

        const {lineWidthScale, pointRadius, pointOpacity, edgeOpacity, nodeBorderWidth, nodeBorderOpacity, degreeBasedRadiusScale} = this.props;
        const layerSettings = {lineWidthScale, pointRadius, pointOpacity, edgeOpacity, nodeBorderWidth, nodeBorderOpacity, degreeBasedRadiusScale};
        return [
            new LabelsLayer().createLayer(location_labels),
            // new HullsLayer().createHullsLayer(hulls),
            new EdgesLayer().createLayer(edges, layerSettings),
            new NodesLayer().createLayer(nodes, layerSettings),
            new CircularHullLayer().createLayer(circluar_hulls, layerSettings)
        ];
    }
}