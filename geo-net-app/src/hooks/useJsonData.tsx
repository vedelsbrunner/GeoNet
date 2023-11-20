import { useState, useEffect } from 'react';

// A custom hook that loads JSON data from the public directory
const usePublicJsonData = (jsonFileName) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Define an async function to fetch the data
    const fetchData = async () => {
      try {
        const response = await fetch(jsonFileName);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        setData(jsonData); // Set the data in state
      } catch (e) {
        setError(e); // Set any error that occurs in state
      } finally {
        setIsLoading(false); // Set loading to false once the fetch is complete
      }
    };

    fetchData();
  }, [jsonFileName]); // This effect runs only when jsonFileName changes

  return { data, isLoading, error };
};

export default usePublicJsonData;
