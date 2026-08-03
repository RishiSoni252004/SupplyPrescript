import api from './api';

export const executeDecision = async (decisionData) => {
  const response = await api.post('/analytics/decisions', decisionData);
  return response.data;
};

export const getAnalyticsDashboard = async () => {
  const response = await api.get('/analytics/dashboard');
  return response.data;
};

export const triggerFeedbackPipeline = async () => {
  const response = await api.post('/analytics/feedback');
  return response.data;
};
