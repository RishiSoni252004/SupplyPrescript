/**
 * MonthlyTrendChart component.
 *
 * Renders a Line Chart with gradient area fill showing the
 * monthly shipment volume trend using Recharts.
 *
 * Props:
 *   data - Array of { month: string, count: number }
 *          e.g. [{ month: "Jan 2025", count: 42 }, ...]
 */

import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { HiOutlineTrendingUp } from 'react-icons/hi';
import ChartCard from './ChartCard';

/**
 * Custom tooltip for the trend chart.
 */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="chart-tooltip">
      <span className="chart-tooltip-dot" style={{ background: '#6366f1' }} />
      <span className="chart-tooltip-label">{label}</span>
      <span className="chart-tooltip-value">
        {payload[0].value.toLocaleString()} shipments
      </span>
    </div>
  );
};

const MonthlyTrendChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <ChartCard
      title="Monthly Shipment Trend"
      subtitle="Volume over time"
      icon={<HiOutlineTrendingUp />}
      className="chart-card--full-width"
    >
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart
          data={data}
          margin={{ top: 8, right: 24, left: -8, bottom: 0 }}
        >
          <defs>
            <linearGradient id="trendGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-color)"
            vertical={false}
          />
          <XAxis
            dataKey="month"
            tick={{ fill: 'var(--text-muted)', fontSize: 12, fontWeight: 500 }}
            axisLine={{ stroke: 'var(--border-color)' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: 'var(--text-muted)', fontSize: 12, fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
            allowDecimals={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#6366f1"
            strokeWidth={2.5}
            fill="url(#trendGradient)"
            dot={{
              r: 4,
              fill: '#6366f1',
              stroke: '#fff',
              strokeWidth: 2,
            }}
            activeDot={{
              r: 6,
              fill: '#6366f1',
              stroke: '#fff',
              strokeWidth: 2,
            }}
            animationBegin={0}
            animationDuration={1000}
            animationEasing="ease-out"
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};

export default MonthlyTrendChart;
