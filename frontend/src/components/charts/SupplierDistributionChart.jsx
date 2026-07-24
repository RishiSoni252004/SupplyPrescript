/**
 * SupplierDistributionChart component.
 *
 * Renders a horizontal Bar Chart showing shipment counts
 * grouped by supplier/carrier using Recharts.
 *
 * Props:
 *   data - Array of { supplier: string, count: number }
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
} from 'recharts';
import { HiOutlineUserGroup } from 'react-icons/hi';
import ChartCard from './ChartCard';

/**
 * Truncate long supplier names for axis readability.
 */
const truncate = (str, maxLen = 12) =>
  str.length > maxLen ? str.slice(0, maxLen) + '…' : str;

/**
 * Custom tooltip for the horizontal Bar Chart.
 */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="chart-tooltip">
      <span className="chart-tooltip-dot" style={{ background: '#8b5cf6' }} />
      <span className="chart-tooltip-label">{label}</span>
      <span className="chart-tooltip-value">{payload[0].value.toLocaleString()}</span>
    </div>
  );
};

const SupplierDistributionChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <ChartCard
      title="Supplier Distribution"
      subtitle="Shipments by carrier"
      icon={<HiOutlineUserGroup />}
    >
      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 8, right: 24, left: 8, bottom: 0 }}
          barCategoryGap="20%"
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border-color)"
            horizontal={false}
          />
          <XAxis
            type="number"
            tick={{ fill: 'var(--text-muted)', fontSize: 12, fontWeight: 500 }}
            axisLine={{ stroke: 'var(--border-color)' }}
            tickLine={false}
            allowDecimals={false}
          />
          <YAxis
            dataKey="supplier"
            type="category"
            width={90}
            tick={{ fill: 'var(--text-muted)', fontSize: 12, fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={truncate}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--hover-bg)' }} />
          <Bar
            dataKey="count"
            fill="#8b5cf6"
            radius={[0, 8, 8, 0]}
            animationBegin={0}
            animationDuration={800}
            animationEasing="ease-out"
          />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};

export default SupplierDistributionChart;
