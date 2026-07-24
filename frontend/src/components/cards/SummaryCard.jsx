/**
 * SummaryCard component.
 *
 * Displays a single KPI metric with an icon, title, value,
 * and optional trend indicator.
 */

import React from 'react';
import './SummaryCard.css';

const SummaryCard = ({ icon, title, value, subtitle, trend, trendDirection, accentColor }) => {
  const trendClass = trendDirection === 'up' ? 'trend--up' : 'trend--down';

  return (
    <div className="summary-card" style={{ '--card-accent': accentColor }}>
      <div className="summary-card-header">
        <div className="summary-card-icon" style={{ background: accentColor + '18', color: accentColor }}>
          {icon}
        </div>
        {trend !== undefined && trend !== null && (
          <span className={`summary-card-trend ${trendClass}`}>
            {trendDirection === 'up' ? '↑' : '↓'} {trend}
          </span>
        )}
      </div>
      <div className="summary-card-body">
        <p className="summary-card-title">{title}</p>
        <h2 className="summary-card-value">{value}</h2>
        {subtitle && <p className="summary-card-subtitle">{subtitle}</p>}
      </div>
      <div className="summary-card-accent-bar" style={{ background: accentColor }} />
    </div>
  );
};

export default SummaryCard;
