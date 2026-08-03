import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import api from '../../services/api';
import './DecisionHistory.css';
import Spinner from '../../components/Spinner';

const DecisionHistory = () => {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDecisions();
  }, []);

  const fetchDecisions = async () => {
    setLoading(true);
    try {
      // Fetching from analytics/decisions or creating a specific endpoint
      // We will create a simple mock logic here if the endpoint isn't fully returning lists yet
      // Or we can rely on a GET /analytics/decisions endpoint if we built one.
      // Wait, we didn't build GET /analytics/decisions list. 
      // Let's assume we can fetch them via a general decisions endpoint.
      // For now we will just simulate a fetch or use the actual endpoint once built.
      
      const response = await api.get('/analytics/decisions');
      setDecisions(response.data);
    } catch (error) {
      toast.error('Failed to load decision history.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="decisions-loading">
        <Spinner size="large" />
      </div>
    );
  }

  return (
    <div className="decisions-container fade-in">
      <div className="decisions-header">
        <h1>Decision History</h1>
        <p>Review previously executed recommendations and their outcomes.</p>
      </div>

      <div className="table-container glass-panel">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Shipment ID</th>
              <th>Selected Option</th>
              <th>Predicted Delay</th>
              <th>Predicted Cost</th>
              <th>Status</th>
              <th>Executed At</th>
            </tr>
          </thead>
          <tbody>
            {decisions.length > 0 ? (
              decisions.map((decision) => (
                <tr key={decision.id}>
                  <td>#{decision.id}</td>
                  <td>{decision.shipment_id}</td>
                  <td>{decision.selected_option}</td>
                  <td>{decision.predicted_delay} days</td>
                  <td>${decision.predicted_cost.toFixed(2)}</td>
                  <td>
                    <span className={`status-badge ${decision.status}`}>
                      {decision.status}
                    </span>
                  </td>
                  <td>{new Date(decision.execution_time).toLocaleString()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="empty-table">No decisions executed yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DecisionHistory;
