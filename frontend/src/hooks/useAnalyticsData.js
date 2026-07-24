/**
 * Custom hook for fetching all analytics dashboard data.
 *
 * Fetches 4 datasets in parallel using Promise.all:
 *   1. Dashboard summary (for shipment status pie chart)
 *   2. Transport mode analysis (bar chart)
 *   3. Supplier distribution (horizontal bar chart)
 *   4. All shipments (aggregated into monthly trend)
 *
 * Returns { data, loading, error, refetch } — consistent
 * with the existing useDashboardSummary pattern.
 */

import { useState, useEffect, useCallback } from 'react';
import {
  fetchDashboardSummary,
  fetchTransportAnalysis,
  fetchSupplierAnalysis,
  fetchAllShipments,
} from '../services/dashboardService';

/**
 * Aggregate raw shipment records into monthly counts.
 *
 * Groups shipments by YYYY-MM from shipment_date and returns
 * sorted array of { month: "Jan 2025", count: 42 }.
 */
const aggregateMonthlyTrend = (shipments) => {
  if (!shipments || shipments.length === 0) return [];

  const monthMap = {};

  shipments.forEach((s) => {
    const date = new Date(s.shipment_date);
    // Build a sortable key (YYYY-MM) and a display label
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    monthMap[key] = (monthMap[key] || 0) + 1;
  });

  const MONTH_NAMES = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
  ];

  return Object.keys(monthMap)
    .sort()
    .map((key) => {
      const [year, monthNum] = key.split('-');
      return {
        month: `${MONTH_NAMES[parseInt(monthNum, 10) - 1]} ${year}`,
        count: monthMap[key],
      };
    });
};

const useAnalyticsData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const [summary, transport, supplier, shipments] = await Promise.all([
        fetchDashboardSummary(),
        fetchTransportAnalysis(),
        fetchSupplierAnalysis(),
        fetchAllShipments(),
      ]);

      // Build shipment status data for Pie Chart
      const shipmentStatus = [
        { name: 'On Time', value: summary.on_time_shipments },
        { name: 'Delayed', value: summary.delayed_shipments },
      ];

      // Transport mode breakdown for Bar Chart
      const transportMode = transport.breakdown || [];

      // Supplier distribution for Horizontal Bar Chart
      const supplierDistribution = supplier.breakdown || [];

      // Monthly trend from raw shipments for Line Chart
      const monthlyTrend = aggregateMonthlyTrend(shipments);

      setData({
        shipmentStatus,
        transportMode,
        supplierDistribution,
        monthlyTrend,
      });
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.message ||
        'Failed to fetch analytics data.';
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

export default useAnalyticsData;
