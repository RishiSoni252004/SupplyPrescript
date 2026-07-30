import React from 'react';
import useRecentShipments from '../../hooks/useRecentShipments';
import Spinner from '../Spinner';
import ErrorMessage from '../ErrorMessage';
import './RecentShipmentsTable.css';

const RecentShipmentsTable = () => {
  const { data: shipments, loading, error, refetch } = useRecentShipments();

  if (loading) return <Spinner message="Loading recent shipments..." />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;
  if (!shipments || shipments.length === 0) return <div className="recent-empty">No recent shipments.</div>;

  return (
    <div className="recent-shipments-container">
      <h3 className="recent-shipments-title">Recent Shipments</h3>
      <div className="table-responsive">
        <table className="recent-shipments-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Origin</th>
              <th>Destination</th>
              <th>Date</th>
              <th>Carrier</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {shipments.map((s) => (
              <tr key={s.id}>
                <td>{s.shipment_id}</td>
                <td>{s.origin}</td>
                <td>{s.destination}</td>
                <td>{new Date(s.shipment_date).toLocaleDateString()}</td>
                <td>{s.carrier}</td>
                <td>
                  <span className={`status-badge ${s.is_delayed ? 'status-delayed' : 'status-ontime'}`}>
                    {s.is_delayed ? 'Delayed' : 'On Time'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecentShipmentsTable;
