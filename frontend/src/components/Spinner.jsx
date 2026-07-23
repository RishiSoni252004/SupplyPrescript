/**
 * Loading spinner component.
 *
 * Displays a pulsing animation with a status message
 * while data is being fetched.
 */

import React from 'react';
import './Spinner.css';

const Spinner = ({ message = 'Loading dashboard data…' }) => {
  return (
    <div className="spinner-container" id="loading-spinner">
      <div className="spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      <p className="spinner-message">{message}</p>
    </div>
  );
};

export default Spinner;
