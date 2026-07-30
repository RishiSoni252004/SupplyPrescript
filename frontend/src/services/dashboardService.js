/**
 * Dashboard API service.
 *
 * Provides reusable functions to fetch dashboard-related data from
 * the FastAPI backend. Each function maps to a specific analytics
 * endpoint.
 */

import api from './api';

/**
 * Fetch high-level KPI summary from the dashboard endpoint.
 *
 * Expected response shape (from DashboardSummaryResponse):
 *   - total_shipments: number
 *   - on_time_shipments: number
 *   - delayed_shipments: number
 *   - on_time_percentage: number
 *   - average_shipping_cost: number
 *   - average_delay_days: number
 */
export const fetchDashboardSummary = async () => {
  const response = await api.get('/dashboard/summary');
  return response.data;
};

/**
 * Fetch transport mode analysis (shipment counts by transport mode).
 *
 * Expected response shape (from TransportAnalysisResponse):
 *   - total_shipments: number
 *   - breakdown: Array<{ transport_mode: string, count: number }>
 */
export const fetchTransportAnalysis = async () => {
  const response = await api.get('/dashboard/transport-analysis');
  return response.data;
};

/**
 * Fetch supplier analysis (shipment counts by carrier).
 *
 * Expected response shape (from SupplierAnalysisResponse):
 *   - total_suppliers: number
 *   - breakdown: Array<{ supplier: string, count: number }>
 */
export const fetchSupplierAnalysis = async () => {
  const response = await api.get('/dashboard/supplier-analysis');
  return response.data;
};

/**
 * Fetch all shipments (used for monthly trend aggregation).
 *
 * We request a large limit to get enough data for trend analysis.
 * The client-side hook will aggregate this into monthly buckets.
 *
 * @param {number} limit - Maximum records to return (default 500).
 */
export const fetchAllShipments = async (limit = 500) => {
  const response = await api.get('/shipments', {
    params: { skip: 0, limit },
  });
  return response.data;
};

export const fetchRecentShipments = async () => {
  const response = await api.get('/dashboard/recent-shipments');
  return response.data;
};
