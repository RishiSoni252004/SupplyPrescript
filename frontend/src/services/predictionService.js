import api from './api';

export const predictDelay = async (data) => {
  const response = await api.post('/predictions/predict', data);
  return response.data;
};

export const getModelInfo = async () => {
  const response = await api.get('/predictions/model/info');
  return response.data;
};
