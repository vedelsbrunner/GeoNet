import {CompositeLayer} from 'deck.gl';
import {NodesLayer} from "./NodesLayer.ts";
import {EdgesLayer} from "./EdgesLayer.ts";
import {HullsLayer} from "./HullsLayer.ts";
import {ExtractDataLayers} from "./DataExtractor.ts";
import {LabelsLayer} from "./LabelsLayer.ts";

export default class GeoNetLayer extends CompositeLayer {

    renderLayers() {
        const {nodes, edges, hulls, location_labels} = ExtractDataLayers(this.props.data)
        console.log(location_labels)
        return [
            new LabelsLayer().createLayer(location_labels),
            new NodesLayer().createLayer(nodes),
            new EdgesLayer().createLayer(edges),
            new HullsLayer().createHullsLayer(hulls)
        ];
    }
}