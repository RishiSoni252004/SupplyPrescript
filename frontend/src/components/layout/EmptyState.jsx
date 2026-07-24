/**
 * EmptyState component.
 *
 * Displays a centered message when no data is available for
 * the analytics charts. Used when the backend returns empty datasets.
 */

import React from 'react';
import { HiOutlineChartBar } from 'react-icons/hi';
import './EmptyState.css';

const EmptyState = ({
  icon,
  title = 'No data available',
  description = 'There are no shipment records to visualize yet. Start by adding shipments to see analytics here.',
}) => {
  return (
    <div className="empty-state" id="empty-state">
      <div className="empty-state-card">
        <div className="empty-state-icon-wrapper">
          {icon || <HiOutlineChartBar className="empty-state-icon" />}
        </div>
        <h3 className="empty-state-title">{title}</h3>
        <p className="empty-state-description">{description}</p>
      </div>
    </div>
  );
};

export default EmptyState;
