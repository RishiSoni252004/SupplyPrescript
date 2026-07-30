import api from './api';

export const getRecommendations = async (data) => {
  const response = await api.post('/recommendations/', data);
  return response.data;
};

export const getSampleRecommendation = async () => {
  const response = await api.get('/recommendations/sample');
  return response.data;
};
