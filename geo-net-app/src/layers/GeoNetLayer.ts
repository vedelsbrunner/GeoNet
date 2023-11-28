import {CompositeLayer, GeoJsonLayer, TextLayer} from 'deck.gl';
import {NodesLayer} from "./NodesLayer.ts";
import {EdgesLayer} from "./EdgesLayer.ts";
import {HullsLayer} from "./HullsLayer.ts";
import {ExtractDataLayers} from "./DataExtractor.ts";

export default class GeoNetLayer extends CompositeLayer {

    renderLayers() {
        const {nodes, edges, hulls, labels} = ExtractDataLayers(this.props.data)
        console.log(hulls)
        return [
            new NodesLayer().createLayer(nodes),
            new EdgesLayer().createLayer(edges),
            new HullsLayer().createHullsLayer(hulls),
        ];
    }
}