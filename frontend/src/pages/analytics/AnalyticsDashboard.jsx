import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { getAnalyticsDashboard, triggerFeedbackPipeline } from '../../services/analyticsService';
import './AnalyticsDashboard.css';

import TrendChart from '../../components/charts/TrendChart';
import DistributionPieChart from '../../components/charts/DistributionPieChart';
import PerformanceBarChart from '../../components/charts/PerformanceBarChart';
import AccuracyAreaChart from '../../components/charts/AccuracyAreaChart';

const AnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const result = await getAnalyticsDashboard();
      setData(result);
    } catch (error) {
      toast.error('Failed to load decision analytics.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleRunFeedback = async () => {
    setFeedbackLoading(true);
    try {
      const logs = await triggerFeedbackPipeline();
      toast.success(`Feedback pipeline run successfully. ${logs.length} decisions evaluated.`);
      fetchAnalytics();
    } catch (error) {
      toast.error('Error running feedback pipeline.');
      console.error(error);
    } finally {
      setFeedbackLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  if (!data) return null;

  // Mocking extended data for charts not yet supplied by backend directly
  const pieData = [
    { name: 'Successful', value: data.successful_recommendations },
    { name: 'Failed', value: data.failed_recommendations },
    { name: 'Pending', value: data.total_decisions - data.successful_recommendations - data.failed_recommendations },
  ];

  const carrierData = [
    { name: 'DHL', value: 400 },
    { name: 'FedEx', value: 300 },
    { name: 'UPS', value: 300 },
    { name: 'Maersk', value: 200 }
  ];

  const transportData = [
    { name: 'Air', value: 45 },
    { name: 'Sea', value: 30 },
    { name: 'Road', value: 20 },
    { name: 'Rail', value: 5 }
  ];

  const monthlyData = [
    { name: 'Jan', performance: 65 },
    { name: 'Feb', performance: 72 },
    { name: 'Mar', performance: 80 },
    { name: 'Apr', performance: 85 },
    { name: 'May', performance: data.accuracy_percentage }
  ];

  const accuracyTrend = [
    { date: 'Week 1', accuracy: 70 },
    { date: 'Week 2', accuracy: 75 },
    { date: 'Week 3', accuracy: 82 },
    { date: 'Week 4', accuracy: data.accuracy_percentage }
  ];

  return (
    <div className="analytics-container fade-in">
      <div className="analytics-header">
        <h1>Closed-Loop Analytics</h1>
        <button 
          className="feedback-btn" 
          onClick={handleRunFeedback} 
          disabled={feedbackLoading}
        >
          {feedbackLoading ? 'Running...' : 'Run Feedback Pipeline'}
        </button>
      </div>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Decisions</h3>
          <p className="metric-value">{data.total_decisions}</p>
        </div>
        <div className="metric-card success">
          <h3>Success Rate</h3>
          <p className="metric-value">{data.accuracy_percentage.toFixed(1)}%</p>
        </div>
        <div className="metric-card">
          <h3>Avg Savings</h3>
          <p className="metric-value">${data.average_savings.toFixed(2)}</p>
        </div>
        <div className="metric-card">
          <h3>Decision ROI</h3>
          <p className="metric-value">{data.decision_roi.toFixed(1)}%</p>
        </div>
      </div>

      <div className="charts-grid">
        <DistributionPieChart data={pieData} title="Decision Success Rate" />
        <DistributionPieChart data={carrierData} title="Supplier / Carrier Distribution" />
        <DistributionPieChart data={transportData} title="Transport Mode Distribution" />
        
        <PerformanceBarChart data={monthlyData} title="Monthly Performance" dataKey="performance" fill="#10b981" />
        <AccuracyAreaChart data={accuracyTrend} title="Prediction Accuracy Trend" dataKey="accuracy" stroke="#6366f1" fill="#6366f1" />
        
        <TrendChart data={accuracyTrend} title="ROI Trend" dataKey="accuracy" strokeColor="#f59e0b" />
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
