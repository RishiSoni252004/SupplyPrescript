/**
 * ShipmentStatusChart component.
 *
 * Renders a Pie Chart showing the split between on-time and
 * delayed shipments using Recharts.
 *
 * Props:
 *   data - Array of { name: string, value: number }
 *          e.g. [{ name: "On Time", value: 95 }, { name: "Delayed", value: 25 }]
 */

import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { HiOutlineChartPie } from 'react-icons/hi2';
import ChartCard from './ChartCard';

const COLORS = ['#10b981', '#ef4444'];

const RADIAN = Math.PI / 180;

/**
 * Custom label renderer that displays the percentage inside each slice.
 */
const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  if (percent < 0.05) return null;

  return (
    <text
      x={x}
      y={y}
      fill="#fff"
      textAnchor="middle"
      dominantBaseline="central"
      fontSize={13}
      fontWeight={700}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

/**
 * Custom tooltip for the Pie Chart.
 */
const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;

  const { name, value } = payload[0];
  return (
    <div className="chart-tooltip">
      <span
        className="chart-tooltip-dot"
        style={{ background: payload[0].payload.fill }}
      />
      <span className="chart-tooltip-label">{name}</span>
      <span className="chart-tooltip-value">{value.toLocaleString()}</span>
    </div>
  );
};

const ShipmentStatusChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <ChartCard
      title="Shipment Status"
      subtitle="On-time vs delayed"
      icon={<HiOutlineChartPie />}
    >
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={4}
            dataKey="value"
            labelLine={false}
            label={renderCustomLabel}
            animationBegin={0}
            animationDuration={800}
            animationEasing="ease-out"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${entry.name}`}
                fill={COLORS[index % COLORS.length]}
                stroke="none"
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="bottom"
            height={36}
            iconType="circle"
            iconSize={10}
            formatter={(value) => (
              <span style={{ color: 'var(--text-secondary)', fontSize: '13px', fontWeight: 500 }}>
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};

export default ShipmentStatusChart;
