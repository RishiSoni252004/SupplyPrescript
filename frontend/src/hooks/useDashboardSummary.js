/**
 * Custom hook for fetching dashboard summary data.
 *
 * Manages loading, error, and data states for the
 * GET /dashboard/summary endpoint.
 */

import { useState, useEffect, useCallback } from 'react';
import { fetchDashboardSummary } from '../services/dashboardService';

const useDashboardSummary = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const summary = await fetchDashboardSummary();
      setData(summary);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.message ||
        'Failed to fetch dashboard summary.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  return { data, loading, error, refetch: loadSummary };
};

export default useDashboardSummary;
