import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { HiOutlinePlus, HiOutlinePencilAlt, HiOutlineTrash, HiOutlineSearch } from 'react-icons/hi';
import { getShipments, deleteShipment } from '../../services/shipmentService';
import Spinner from '../../components/Spinner';
import ErrorMessage from '../../components/ErrorMessage';
import './ShipmentList.css';

const ShipmentList = () => {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Pagination and Search
  const [skip, setSkip] = useState(0);
  const [limit] = useState(10);
  const [search, setSearch] = useState('');

  const loadShipments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getShipments(skip, limit);
      setShipments(data || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch shipments');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadShipments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skip]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this shipment?')) return;
    
    try {
      await deleteShipment(id);
      toast.success('Shipment deleted successfully');
      loadShipments();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete shipment');
    }
  };

  const filteredShipments = shipments.filter(s => 
    s.shipment_id.toLowerCase().includes(search.toLowerCase()) ||
    s.origin.toLowerCase().includes(search.toLowerCase()) ||
    s.destination.toLowerCase().includes(search.toLowerCase())
  );

  if (loading && shipments.length === 0) return <div className="page-content"><Spinner message="Loading shipments..." /></div>;
  if (error) return <div className="page-content"><ErrorMessage message={error} onRetry={loadShipments} /></div>;

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2 className="page-title">Shipments</h2>
          <p className="page-subtitle">Manage all your supply chain shipments</p>
        </div>
        <Link to="/shipments/add" className="btn btn-primary">
          <HiOutlinePlus className="btn-icon" /> Add Shipment
        </Link>
      </div>

      <div className="list-container">
        <div className="list-toolbar">
          <div className="search-box">
            <HiOutlineSearch className="search-icon" />
            <input 
              type="text" 
              placeholder="Search by ID, Origin, Destination..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Origin</th>
                <th>Destination</th>
                <th>Date</th>
                <th>Carrier</th>
                <th>Mode</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredShipments.length === 0 ? (
                <tr>
                  <td colSpan="8" className="empty-row">No shipments found.</td>
                </tr>
              ) : (
                filteredShipments.map(s => (
                  <tr key={s.id}>
                    <td>{s.shipment_id}</td>
                    <td>{s.origin}</td>
                    <td>{s.destination}</td>
                    <td>{new Date(s.shipment_date).toLocaleDateString()}</td>
                    <td>{s.carrier}</td>
                    <td>{s.transport_mode}</td>
                    <td>
                      <span className={`status-badge ${s.is_delayed ? 'status-delayed' : 'status-ontime'}`}>
                        {s.is_delayed ? 'Delayed' : 'On Time'}
                      </span>
                    </td>
                    <td className="actions-cell">
                      <Link to={`/shipments/edit/${s.id}`} className="btn-icon-only text-blue" title="Edit">
                        <HiOutlinePencilAlt />
                      </Link>
                      <button onClick={() => handleDelete(s.id)} className="btn-icon-only text-red" title="Delete">
                        <HiOutlineTrash />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="pagination">
          <button 
            className="btn btn-outline" 
            disabled={skip === 0} 
            onClick={() => setSkip(skip - limit)}
          >
            Previous
          </button>
          <span className="pagination-info">Showing {skip + 1} to {skip + shipments.length}</span>
          <button 
            className="btn btn-outline" 
            disabled={shipments.length < limit}
            onClick={() => setSkip(skip + limit)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default ShipmentList;
