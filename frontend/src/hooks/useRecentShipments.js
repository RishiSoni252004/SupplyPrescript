import { useState, useEffect, useCallback } from 'react';
import { fetchRecentShipments } from '../services/dashboardService';

const useRecentShipments = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchRecentShipments();
      setData(response.shipments || []);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.message ||
        'Failed to fetch recent shipments.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return { data, loading, error, refetch: loadData };
};

export default useRecentShipments;
