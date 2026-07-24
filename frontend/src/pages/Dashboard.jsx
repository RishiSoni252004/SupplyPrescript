/**
 * Main Dashboard Page.
 *
 * Uses the useDashboardSummary hook to fetch KPI data and
 * displays it using SummaryCard components. Includes loading
 * and error states.
 *
 * The analytics section uses useAnalyticsData to fetch chart data
 * and renders 4 Recharts visualizations in a responsive grid.
 */

import React from 'react';
import {
  HiOutlineCube,
  HiOutlineClock,
  HiOutlineCheckCircle,
  HiOutlineCurrencyDollar,
} from 'react-icons/hi';
import SummaryCard from '../components/cards/SummaryCard';
import Spinner from '../components/Spinner';
import ErrorMessage from '../components/ErrorMessage';
import useDashboardSummary from '../hooks/useDashboardSummary';
import useAnalyticsData from '../hooks/useAnalyticsData';
import {
  ShipmentStatusChart,
  TransportModeChart,
  SupplierDistributionChart,
  MonthlyTrendChart,
} from '../components/charts';
import ChartGrid from '../components/layout/ChartGrid';
import ChartSkeleton from '../components/layout/ChartSkeleton';
import EmptyState from '../components/layout/EmptyState';
import './Dashboard.css';

const Dashboard = () => {
  const { data, loading, error, refetch } = useDashboardSummary();
  const {
    data: analyticsData,
    loading: analyticsLoading,
    error: analyticsError,
    refetch: analyticsRefetch,
  } = useAnalyticsData();

  if (loading) {
    return (
      <div className="dashboard-content">
        <Spinner message="Loading dashboard summary..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-content">
        <ErrorMessage message={error} onRetry={refetch} />
      </div>
    );
  }

  if (!data) return null;

  /**
   * Check if all analytics datasets are empty.
   */
  const isAnalyticsEmpty =
    analyticsData &&
    analyticsData.shipmentStatus.every((s) => s.value === 0) &&
    analyticsData.transportMode.length === 0 &&
    analyticsData.supplierDistribution.length === 0 &&
    analyticsData.monthlyTrend.length === 0;

  return (
    <div className="dashboard-content">
      {/* --- KPI Section --- */}
      <div className="dashboard-header">
        <h2 className="dashboard-title">Overview</h2>
        <p className="dashboard-subtitle">Key Performance Indicators</p>
      </div>

      <div className="kpi-grid">
        <SummaryCard
          title="Total Shipments"
          value={data.total_shipments.toLocaleString()}
          icon={<HiOutlineCube />}
          accentColor="#6366f1"
          trend="12%"
          trendDirection="up"
          subtitle="vs last month"
        />
        
        <SummaryCard
          title="Delayed Shipments"
          value={data.delayed_shipments.toLocaleString()}
          icon={<HiOutlineClock />}
          accentColor="#ef4444"
          trend="3%"
          trendDirection="up"
          subtitle="Action required"
        />
        
        <SummaryCard
          title="On-Time Shipments"
          value={data.on_time_shipments.toLocaleString()}
          icon={<HiOutlineCheckCircle />}
          accentColor="#10b981"
          subtitle={`${data.on_time_percentage.toFixed(1)}% success rate`}
        />
        
        <SummaryCard
          title="Avg Shipping Cost"
          value={`$${data.average_shipping_cost.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
          icon={<HiOutlineCurrencyDollar />}
          accentColor="#f59e0b"
          trend="5%"
          trendDirection="down"
          subtitle="vs last month"
        />
      </div>

      {/* --- Analytics Charts Section --- */}
      <div className="analytics-section">
        <div className="dashboard-header">
          <h2 className="dashboard-title">Analytics</h2>
          <p className="dashboard-subtitle">Visual insights from your supply chain data</p>
        </div>

        {analyticsLoading && <ChartSkeleton />}

        {analyticsError && !analyticsLoading && (
          <ErrorMessage message={analyticsError} onRetry={analyticsRefetch} />
        )}

        {isAnalyticsEmpty && !analyticsLoading && !analyticsError && (
          <EmptyState />
        )}

        {analyticsData && !isAnalyticsEmpty && !analyticsLoading && !analyticsError && (
          <ChartGrid>
            <ShipmentStatusChart data={analyticsData.shipmentStatus} />
            <TransportModeChart data={analyticsData.transportMode} />
            <SupplierDistributionChart data={analyticsData.supplierDistribution} />
            <MonthlyTrendChart data={analyticsData.monthlyTrend} />
          </ChartGrid>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
