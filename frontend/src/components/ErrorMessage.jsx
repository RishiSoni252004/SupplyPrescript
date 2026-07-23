/**
 * ErrorMessage component.
 *
 * Displays an error alert with a retry button when
 * an API request fails.
 */

import React from 'react';
import { HiOutlineExclamationTriangle } from 'react-icons/hi2';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-container" id="error-message">
      <div className="error-card">
        <div className="error-icon-wrapper">
          <HiOutlineExclamationTriangle className="error-icon" />
        </div>
        <h3 className="error-title">Something went wrong</h3>
        <p className="error-text">{message}</p>
        {onRetry && (
          <button className="error-retry-btn" onClick={onRetry} id="retry-btn">
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;
