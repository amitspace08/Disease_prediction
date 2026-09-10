import api from './api';

export const getDiseases = async () => {
  const response = await api.get('/diseases');
  return response.data.diseases;
};

export const predictDisease = async (diseaseId, data) => {
  const response = await api.post(`/predict/${diseaseId}`, data);
  return response.data;
};

export const getHistory = async () => {
  const response = await api.get('/predict/history');
  return response.data.history;
};
