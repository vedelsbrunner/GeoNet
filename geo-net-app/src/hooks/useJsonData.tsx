import {useState, useEffect} from 'react';

export enum Layouts {
    Default = 'default',
    SingleCircularClustered = 'singleCircularClustered',
    NoOverlapSingleCircularClustered = 'noOverlapSingleCircularClustered',
    SingleCircular = 'singleCircular',
    NoOverlapSingleCircular = 'noOverlapSingleCircular',
    DoubleCircularClustered = 'doubleCircularClustered',
    NoOverlapDoubleCircularClustered = 'noOverlapDoubleCircularClustered',
    DoubleCircular = 'doubleCircular',
    NoOverlapDoubleCircular = 'noOverlapDoubleCircular',
    Stacked = 'stacked',
    NoOverlapStacked = 'noOverlapStacked',
    StackedClustered = 'stackedClustered',
    NoOverlapStackedClustered = 'noOverlapStackedClustered',
    Sunflower = 'sunflower',
    NoOverlapSunflower = 'noOverlapSunflower',
    SunflowerClustered = 'sunflowerClustered',
    NoOverlapSunflowerClustered = 'noOverlapSunflowerClustered',
    Grid = 'grid',
    NoOverlapGrid = 'noOverlapGrid',
    GridClustered = 'gridClustered',
    NoOverlapGridClustered = 'noOverlapGridClustered'
}

export interface JsonFilePathsDictionary {
    [Layouts.Default]?: string;
    [Layouts.SingleCircularClustered]?: string;
    [Layouts.NoOverlapSingleCircularClustered]?: string;
    [Layouts.SingleCircular]?: string;
    [Layouts.NoOverlapSingleCircular]?: string;
    [Layouts.DoubleCircularClustered]?: string;
    [Layouts.NoOverlapDoubleCircularClustered]?: string;
    [Layouts.DoubleCircular]?: string;
    [Layouts.NoOverlapDoubleCircular]?: string;
    [Layouts.Stacked]?: string;
    [Layouts.NoOverlapStacked]?: string;
    [Layouts.StackedClustered]?: string;
    [Layouts.NoOverlapStackedClustered]?: string;
    [Layouts.Sunflower]?: string;
    [Layouts.NoOverlapSunflower]?: string;
    [Layouts.SunflowerClustered]?: string;
    [Layouts.NoOverlapSunflowerClustered]?: string;
    [Layouts.Grid]?: string;
    [Layouts.NoOverlapGrid]?: string;
    [Layouts.GridClustered]?: string;
    [Layouts.NoOverlapGridClustered]?: string;
}

interface DataSetsDictionary {
    [key: string]: any;
}

export interface UsePublicJsonDataReturn {
    isLoading: boolean;
    error: Error | null;
}

const usePublicJsonData = (jsonFilePaths: JsonFilePathsDictionary, setExternalLayouts: (layouts: DataSetsDictionary | null) => void): UsePublicJsonDataReturn => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        setExternalLayouts(null); // Reset layouts to null before fetching new data

        if (!jsonFilePaths || Object.keys(jsonFilePaths).length === 0) {
            setIsLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                const dataSetsPromises = Object.entries(jsonFilePaths).map(async ([name, path]) => {
                    const response = await fetch(path);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const jsonData = await response.json();
                    return {name, data: jsonData};
                });

                const loadedDataSets = await Promise.all(dataSetsPromises);
                const newDataSet = loadedDataSets.reduce((acc, {name, data}) => {
                    acc[name] = data;
                    return acc;
                }, {});

                setExternalLayouts(newDataSet);

            } catch (e) {
                setError(e instanceof Error ? e : new Error(e.toString()));
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [jsonFilePaths, setExternalLayouts]);

    return {isLoading, error};
};

export default usePublicJsonData;
