/**
 * ChartSkeleton component.
 *
 * Animated loading skeleton that mimics chart card shapes.
 * Displays 4 pulsing placeholders while analytics data is loading.
 */

import React from 'react';
import './ChartSkeleton.css';

const SkeletonCard = ({ className = '' }) => (
  <div className={`skeleton-card ${className}`}>
    <div className="skeleton-header">
      <div className="skeleton-icon" />
      <div className="skeleton-title-group">
        <div className="skeleton-title" />
        <div className="skeleton-subtitle" />
      </div>
    </div>
    <div className="skeleton-body">
      <div className="skeleton-chart" />
    </div>
  </div>
);

const ChartSkeleton = () => {
  return (
    <div className="chart-skeleton-grid" id="chart-loading-skeleton">
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard />
      <SkeletonCard className="skeleton-card--full-width" />
    </div>
  );
};

export default ChartSkeleton;
