import { useState, useEffect } from 'react';

const usePublicJsonData = (jsonFileNames) => {
  const [dataSets, setDataSets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const loadedDataSets = await Promise.all(
          jsonFileNames.map(async (fileName) => {
            const response = await fetch(fileName);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
        );
        setDataSets(loadedDataSets);
      } catch (e) {
        setError(e);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [jsonFileNames]);

  return { dataSets, isLoading, error };
};

export default usePublicJsonData;
