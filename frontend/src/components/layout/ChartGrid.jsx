/**
 * ChartGrid component.
 *
 * Responsive CSS Grid layout for chart cards.
 * 2 columns on desktop, 1 column on mobile.
 */

import React from 'react';
import './ChartGrid.css';

const ChartGrid = ({ children }) => {
  return (
    <div className="chart-grid" id="analytics-charts-grid">
      {children}
    </div>
  );
};

export default ChartGrid;
