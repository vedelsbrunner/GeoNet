import {useState, useEffect} from 'react';

export enum Layouts {
    Default = 'default',
    CircularClustered = 'circularClustered',
    Circular = 'circular',
    Stacked = 'stacked',
    StackedClustered = 'stackedClustered'
}

export interface JsonFilePathsDictionary {
    [Layouts.Default]?: string;
    [Layouts.CircularClustered]?: string;
    [Layouts.Circular]?: string;
    [Layouts.Stacked]?: string;
    [Layouts.StackedClustered]?: string;
}

interface DataSetsDictionary {
    [key: string]: any;
}

export interface UsePublicJsonDataReturn {
    dataSets: DataSetsDictionary;
    isLoading: boolean;
    error: Error | null;
}

const usePublicJsonData = (jsonFilePaths: JsonFilePathsDictionary): UsePublicJsonDataReturn => {
    const [dataSets, setDataSets] = useState<DataSetsDictionary>({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
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

                setDataSets(newDataSet);
            } catch (e) {
                setError(e instanceof Error ? e : new Error(e.toString()));
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [jsonFilePaths]);

    return {dataSets, isLoading, error};
};

export default usePublicJsonData;
