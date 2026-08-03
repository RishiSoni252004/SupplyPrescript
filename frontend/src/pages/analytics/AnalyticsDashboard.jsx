import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getAnalyticsDashboard, triggerFeedbackPipeline } from '../../services/analyticsService';
import './AnalyticsDashboard.css';

const COLORS = ['#10b981', '#ef4444', '#f59e0b']; // green, red, yellow

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

  const pieData = [
    { name: 'Successful', value: data.successful_recommendations },
    { name: 'Failed', value: data.failed_recommendations },
    { name: 'Pending', value: data.total_decisions - data.successful_recommendations - data.failed_recommendations },
  ];

  const savingsData = [
    { name: 'Avg Savings', value: data.average_savings },
    { name: 'ROI (%)', value: data.decision_roi }
  ];

  return (
    <div className="analytics-container">
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
        <div className="chart-card glass-panel">
          <h3>Decision Outcomes</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card glass-panel">
          <h3>Savings & ROI</h3>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={savingsData}>
                <XAxis dataKey="name" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }} />
                <Bar dataKey="value" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
