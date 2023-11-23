import {CompositeLayer, GeoJsonLayer, TextLayer} from 'deck.gl';
import {NodesLayer} from "./NodesLayer.ts";
import {EdgesLayer} from "./EdgesLayer.ts";

export default class GeoNetLayer extends CompositeLayer {


    _createHullsLayer(hulls) {
        console.log('Creating hulls layer with data: ', hulls);
        return new GeoJsonLayer({
            id: 'hulls-layer',
            data: hulls,
        });
    }

    _createLabelsLayer(labels) {
    console.log('Creating labels layer with data: ', labels);
        return new TextLayer({
            id: 'text-layer',
            data: labels,
        });
    }

    _extractDataLayers(geoJson) {
        let nodes = [];
        let edges = [];
        let hulls = {type: 'FeatureCollection', features: []};
        let labels = [];

        geoJson.features.forEach(feature => {
            switch (feature.geometry.type) {
                case 'Point':
                    nodes.push(feature);
                    break;
                case 'LineString':
                    edges.push(feature);
                    break;
                case 'Polygon':
                case 'MultiPolygon':
                    hulls.features.push(feature);
                    break;
                case 'Point' && feature.properties.label:
                    labels.push(feature);
                    break;
            }
        });

        return {nodes, edges, hulls, labels};
    }

    renderLayers() {
        const {nodes, edges, hulls, labels} = this._extractDataLayers(this.props.data)

        return [
            new NodesLayer().createLayer(nodes),
            new EdgesLayer().createLayer(edges),
            // this._createHullsLayer(hulls),
            // this._createLabelsLayer(labels)
        ];
    }
}