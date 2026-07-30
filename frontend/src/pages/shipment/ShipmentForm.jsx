import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { getShipment, createShipment, updateShipment } from '../../services/shipmentService';
import Spinner from '../../components/Spinner';
import './ShipmentForm.css';

const initialFormState = {
  shipment_id: '',
  origin: '',
  destination: '',
  shipment_date: new Date().toISOString().slice(0, 16),
  delivery_date: '',
  carrier: '',
  weight_kg: '',
  shipping_cost: '',
  transport_mode: 'Road',
  is_delayed: false,
  delay_days: 0,
  notes: ''
};

const ShipmentForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = !!id;

  const [formData, setFormData] = useState(initialFormState);
  const [loading, setLoading] = useState(isEditMode);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isEditMode) {
      const fetchShipment = async () => {
        try {
          const data = await getShipment(id);
          setFormData({
            ...data,
            shipment_date: data.shipment_date ? new Date(data.shipment_date).toISOString().slice(0, 16) : '',
            delivery_date: data.delivery_date ? new Date(data.delivery_date).toISOString().slice(0, 16) : ''
          });
        } catch {
          toast.error('Failed to load shipment data');
          navigate('/shipments');
        } finally {
          setLoading(false);
        }
      };
      fetchShipment();
    }
  }, [id, navigate, isEditMode]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    // Formatting data for API
    const payload = {
      ...formData,
      weight_kg: parseFloat(formData.weight_kg),
      shipping_cost: parseFloat(formData.shipping_cost),
      delay_days: parseInt(formData.delay_days || 0, 10),
      delivery_date: formData.delivery_date ? new Date(formData.delivery_date).toISOString() : null,
      shipment_date: new Date(formData.shipment_date).toISOString()
    };

    if (!payload.is_delayed) {
      payload.delay_days = 0;
    }

    try {
      if (isEditMode) {
        await updateShipment(id, payload);
        toast.success('Shipment updated successfully');
      } else {
        await createShipment(payload);
        toast.success('Shipment created successfully');
      }
      navigate('/shipments');
    } catch (err) {
      const detail = err.response?.data?.detail || 'An error occurred';
      toast.error(typeof detail === 'string' ? detail : JSON.stringify(detail));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="page-content"><Spinner message="Loading..." /></div>;

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2 className="page-title">{isEditMode ? 'Edit Shipment' : 'Add Shipment'}</h2>
          <p className="page-subtitle">
            {isEditMode ? 'Update existing shipment details' : 'Create a new shipment record'}
          </p>
        </div>
        <Link to="/shipments" className="btn btn-outline">Back to List</Link>
      </div>

      <div className="form-container">
        <form onSubmit={handleSubmit} className="shipment-form">
          <div className="form-grid">
            
            <div className="form-group">
              <label>Shipment ID *</label>
              <input type="text" name="shipment_id" value={formData.shipment_id} onChange={handleChange} required className="form-input" placeholder="e.g. SHP-1001" disabled={isEditMode} />
            </div>

            <div className="form-group">
              <label>Carrier *</label>
              <input type="text" name="carrier" value={formData.carrier} onChange={handleChange} required className="form-input" placeholder="e.g. DHL, FedEx" />
            </div>

            <div className="form-group">
              <label>Origin *</label>
              <input type="text" name="origin" value={formData.origin} onChange={handleChange} required className="form-input" placeholder="City or Warehouse" />
            </div>

            <div className="form-group">
              <label>Destination *</label>
              <input type="text" name="destination" value={formData.destination} onChange={handleChange} required className="form-input" placeholder="City or Warehouse" />
            </div>

            <div className="form-group">
              <label>Shipment Date *</label>
              <input type="datetime-local" name="shipment_date" value={formData.shipment_date} onChange={handleChange} required className="form-input" />
            </div>

            <div className="form-group">
              <label>Delivery Date</label>
              <input type="datetime-local" name="delivery_date" value={formData.delivery_date} onChange={handleChange} className="form-input" />
            </div>

            <div className="form-group">
              <label>Weight (kg) *</label>
              <input type="number" step="0.1" min="0.1" name="weight_kg" value={formData.weight_kg} onChange={handleChange} required className="form-input" />
            </div>

            <div className="form-group">
              <label>Shipping Cost (USD) *</label>
              <input type="number" step="0.01" min="0" name="shipping_cost" value={formData.shipping_cost} onChange={handleChange} required className="form-input" />
            </div>

            <div className="form-group">
              <label>Transport Mode *</label>
              <select name="transport_mode" value={formData.transport_mode} onChange={handleChange} required className="form-input">
                <option value="Road">Road</option>
                <option value="Air">Air</option>
                <option value="Sea">Sea</option>
                <option value="Rail">Rail</option>
              </select>
            </div>
            
            <div className="form-group empty-space"></div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input type="checkbox" name="is_delayed" checked={formData.is_delayed} onChange={handleChange} />
                Is Delayed?
              </label>
            </div>

            {formData.is_delayed && (
              <div className="form-group">
                <label>Delay Days *</label>
                <input type="number" min="0" name="delay_days" value={formData.delay_days} onChange={handleChange} required className="form-input" />
              </div>
            )}

            <div className="form-group full-width">
              <label>Notes</label>
              <textarea name="notes" value={formData.notes || ''} onChange={handleChange} className="form-input" rows="3" placeholder="Optional notes..."></textarea>
            </div>

          </div>

          <div className="form-actions">
            <button type="button" onClick={() => navigate('/shipments')} className="btn btn-outline" disabled={submitting}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving...' : 'Save Shipment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ShipmentForm;
