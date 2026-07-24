/**
 * ChartCard component.
 *
 * Reusable wrapper that provides a consistent card container for
 * every chart visualization. Includes a header with title, subtitle,
 * and optional icon.
 */

import React from 'react';
import './ChartCard.css';

const ChartCard = ({ title, subtitle, icon, children, className = '' }) => {
  return (
    <div className={`chart-card ${className}`} id={`chart-${title?.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="chart-card-header">
        <div className="chart-card-title-group">
          {icon && <span className="chart-card-icon">{icon}</span>}
          <div>
            <h3 className="chart-card-title">{title}</h3>
            {subtitle && <p className="chart-card-subtitle">{subtitle}</p>}
          </div>
        </div>
      </div>
      <div className="chart-card-body">
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
