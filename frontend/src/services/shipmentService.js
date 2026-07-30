import api from './api';

export const getShipments = async (skip = 0, limit = 100) => {
  const response = await api.get('/shipments', { params: { skip, limit } });
  return response.data;
};

export const getShipment = async (id) => {
  const response = await api.get(`/shipments/${id}`);
  return response.data;
};

export const createShipment = async (data) => {
  const response = await api.post('/shipments', data);
  return response.data;
};

export const updateShipment = async (id, data) => {
  const response = await api.put(`/shipments/${id}`, data);
  return response.data;
};

export const deleteShipment = async (id) => {
  const response = await api.delete(`/shipments/${id}`);
  return response.data;
};
