import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { predictDelay } from '../../services/predictionService';
import { getRecommendations } from '../../services/recommendationService';
import Spinner from '../../components/Spinner';
import './PredictionPage.css';

const initialForm = {
  supplier: 'BlueDart',
  origin: 'Mumbai',
  destination: 'Delhi',
  transport_mode: 'Road',
  distance_km: 1400,
  shipping_cost: 1200,
  weather_condition: 'Clear',
  traffic_level: 'Moderate',
  order_priority: 'High',
  expected_delivery_days: 3,
  // Fields needed for recommendation
  budget: 20000,
  inventory_level: 50,
};

const PredictionPage = () => {
  const [formData, setFormData] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  
  // Results state
  const [predictionResult, setPredictionResult] = useState(null);
  const [recommendationResult, setRecommendationResult] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPredictionResult(null);
    setRecommendationResult(null);

    try {
      // 1. Format payload for prediction
      const predictPayload = {
        supplier: formData.supplier,
        origin: formData.origin,
        destination: formData.destination,
        transport_mode: formData.transport_mode,
        distance_km: parseFloat(formData.distance_km),
        shipping_cost: parseFloat(formData.shipping_cost),
        weather_condition: formData.weather_condition,
        traffic_level: formData.traffic_level,
        order_priority: formData.order_priority,
        expected_delivery_days: parseInt(formData.expected_delivery_days, 10),
      };

      const predRes = await predictDelay(predictPayload);
      setPredictionResult(predRes);
      toast.success('Prediction completed successfully!');

      // 2. Automatically get recommendations if delay is predicted
      // (Even if on-time, we can ask for recs, but let's just pass the delay probability or a static value)
      // The backend expects predicted_delay_days, which we estimate based on probability or just pass a mock value 
      // since the prediction model just returns a probability.
      // We'll estimate delay days as round(probability * 10) if delayed, else 0.
      const isDelayed = predRes.prediction === 'Delayed';
      const estimatedDelayDays = isDelayed ? Math.max(1, Math.round(predRes.delay_probability * 10)) : 0;

      const recPayload = {
        predicted_delay_days: estimatedDelayDays,
        budget: parseFloat(formData.budget),
        priority: formData.order_priority,
        inventory_level: parseInt(formData.inventory_level, 10)
      };

      const recRes = await getRecommendations(recPayload);
      setRecommendationResult(recRes);
      
    } catch (err) {
      const msg = err.response?.data?.detail || 'An error occurred during prediction.';
      toast.error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = () => {
    // Mocking execution
    toast.success('Decision executed successfully! Generating new shipment plan...');
    setTimeout(() => {
      navigate('/shipments');
    }, 2000);
  };

  return (
    <div className="page-content">
      <div className="page-header">
        <h2 className="page-title">Prediction & Recommendation</h2>
        <p className="page-subtitle">Predict shipment delays and receive prescriptive AI actions</p>
      </div>

      <div className="prediction-layout">
        <div className="form-section box-card">
          <h3 className="section-title">Shipment Details</h3>
          <form onSubmit={handlePredict} className="pred-form">
            <div className="form-grid">
              
              <div className="form-group">
                <label>Carrier / Supplier</label>
                <input type="text" name="supplier" value={formData.supplier} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Origin</label>
                <input type="text" name="origin" value={formData.origin} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Destination</label>
                <input type="text" name="destination" value={formData.destination} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Transport Mode</label>
                <select name="transport_mode" value={formData.transport_mode} onChange={handleChange} className="form-input">
                  <option value="Road">Road</option>
                  <option value="Air">Air</option>
                  <option value="Sea">Sea</option>
                  <option value="Rail">Rail</option>
                </select>
              </div>
              <div className="form-group">
                <label>Distance (km)</label>
                <input type="number" name="distance_km" value={formData.distance_km} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Expected Days</label>
                <input type="number" name="expected_delivery_days" value={formData.expected_delivery_days} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Weather</label>
                <select name="weather_condition" value={formData.weather_condition} onChange={handleChange} className="form-input">
                  <option value="Clear">Clear</option>
                  <option value="Rain">Rain</option>
                  <option value="Storm">Storm</option>
                  <option value="Snow">Snow</option>
                </select>
              </div>
              <div className="form-group">
                <label>Traffic Level</label>
                <select name="traffic_level" value={formData.traffic_level} onChange={handleChange} className="form-input">
                  <option value="Low">Low</option>
                  <option value="Moderate">Moderate</option>
                  <option value="High">High</option>
                </select>
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select name="order_priority" value={formData.order_priority} onChange={handleChange} className="form-input">
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>
              <div className="form-group">
                <label>Budget (USD)</label>
                <input type="number" name="budget" value={formData.budget} onChange={handleChange} className="form-input" required />
              </div>
              <div className="form-group">
                <label>Inventory Level</label>
                <input type="number" name="inventory_level" value={formData.inventory_level} onChange={handleChange} className="form-input" required />
              </div>

            </div>
            
            <button type="submit" className="btn btn-primary mt-4" disabled={loading} style={{ width: '100%' }}>
              {loading ? 'Analyzing...' : 'Run Analysis'}
            </button>
          </form>
        </div>

        <div className="results-section">
          {loading && (
            <div className="box-card loading-card">
              <Spinner message="Running ML Pipeline..." />
            </div>
          )}

          {!loading && predictionResult && (
            <div className="box-card prediction-card">
              <h3 className="section-title">Prediction Result</h3>
              <div className={`pred-status ${predictionResult.prediction === 'Delayed' ? 'pred-delayed' : 'pred-ontime'}`}>
                {predictionResult.prediction}
              </div>
              <div className="pred-metrics">
                <div className="metric-box">
                  <span className="metric-label">Probability</span>
                  <span className="metric-value">{(predictionResult.delay_probability * 100).toFixed(1)}%</span>
                </div>
                <div className="metric-box">
                  <span className="metric-label">Confidence</span>
                  <span className="metric-value">{predictionResult.confidence}</span>
                </div>
              </div>
            </div>
          )}

          {!loading && recommendationResult && (
            <div className="box-card recommendation-card">
              <h3 className="section-title">Prescriptive Recommendation</h3>
              
              <div className="rec-best">
                <div className="rec-best-header">Best Option</div>
                <div className="rec-best-title">{recommendationResult.best_option}</div>
                <div className="rec-best-reason">{recommendationResult.reason}</div>
                
                <div className="rec-metrics">
                  <div><strong>Est. Cost:</strong> ${recommendationResult.estimated_cost.toFixed(2)}</div>
                  <div><strong>Est. Delay:</strong> {recommendationResult.estimated_delay} days</div>
                </div>

                <button onClick={handleExecute} className="btn btn-primary mt-4 w-full execute-btn">
                  Execute Decision
                </button>
              </div>

              {recommendationResult.alternatives && recommendationResult.alternatives.length > 0 && (
                <div className="rec-alternatives">
                  <h4 className="alt-title">Alternatives Considered</h4>
                  <ul className="alt-list">
                    {recommendationResult.alternatives.map((alt, idx) => (
                      <li key={idx} className="alt-item">
                        <div className="alt-name">{alt.name}</div>
                        <div className="alt-details">
                          Cost: ${alt.estimated_cost} | Delay: {alt.estimated_delay}d
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {!loading && !predictionResult && (
            <div className="box-card empty-results">
              Fill the form and click "Run Analysis" to see ML predictions and prescriptive recommendations.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictionPage;
