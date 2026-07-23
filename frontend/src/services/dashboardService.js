/**
 * Dashboard API service.
 *
 * Provides functions to fetch dashboard-related data from
 * the FastAPI backend.
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
