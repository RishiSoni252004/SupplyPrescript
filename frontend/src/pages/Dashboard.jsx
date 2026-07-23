/**
 * Main Dashboard Page.
 *
 * Uses the useDashboardSummary hook to fetch KPI data and
 * displays it using SummaryCard components. Includes loading
 * and error states.
 */

import React from 'react';
import {
  HiOutlineCube,
  HiOutlineClock,
  HiOutlineCheckCircle,
  HiOutlineCurrencyDollar,
} from 'react-icons/hi';
import SummaryCard from '../components/SummaryCard';
import Spinner from '../components/Spinner';
import ErrorMessage from '../components/ErrorMessage';
import useDashboardSummary from '../hooks/useDashboardSummary';
import './Dashboard.css';

const Dashboard = () => {
  const { data, loading, error, refetch } = useDashboardSummary();

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

  return (
    <div className="dashboard-content">
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

      <div className="dashboard-extra">
        {/* Placeholder for future charts or tables */}
        <div className="placeholder-card">
          <p>More detailed analytics and visualizations coming soon.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
