/**
 * TransportModeChart component.
 *
 * Renders a vertical Bar Chart showing shipment counts by
 * transport mode (Air, Sea, Road, Rail) using Recharts.
 *
 * Props:
 *   data - Array of { transport_mode: string, count: number }
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { HiOutlineTruck } from 'react-icons/hi';
import ChartCard from './ChartCard';

const MODE_COLORS = {
  Air: '#6366f1',
  Sea: '#0ea5e9',
  Road: '#f59e0b',
  Rail: '#10b981',
};

const DEFAULT_COLOR = '#8b5cf6';

/**
 * Custom tooltip for the Bar Chart.
 */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="chart-tooltip">
      <span
        className="chart-tooltip-dot"
        style={{ background: payload[0].payload.fill || payload[0].fill }}
      />
      <span className="chart-tooltip-label">{label}</span>
      <span className="chart-tooltip-value">{payload[0].value.toLocaleString()}</span>
    </div>
  );
};

const TransportModeChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.map((item) => ({
    ...item,
    fill: MODE_COLORS[item.transport_mode] || DEFAULT_COLOR,
  }));

  return (
    <ChartCard
      title="Transport Mode"
      subtitle="Shipments by mode"
      icon={<HiOutlineTruck />}
    >
      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={chartData}
          margin={{ top: 8, right: 16, left: -8, bottom: 0 }}
          barCategoryGap="25%"
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-color)"
            vertical={false}
          />
          <XAxis
            dataKey="transport_mode"
            tick={{ fill: 'var(--text-muted)', fontSize: 12.5, fontWeight: 500 }}
            axisLine={{ stroke: 'var(--border-color)' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: 'var(--text-muted)', fontSize: 12, fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
            allowDecimals={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--hover-bg)' }} />
          <Bar
            dataKey="count"
            radius={[8, 8, 0, 0]}
            animationBegin={0}
            animationDuration={800}
            animationEasing="ease-out"
          >
            {chartData.map((entry) => (
              <Cell key={entry.transport_mode} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};

export default TransportModeChart;
