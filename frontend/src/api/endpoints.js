// src/api/endpoints.js
import { apiClient } from './client'

export const simulationApi = {
  create: (data) => apiClient.post('/simulations', data),
  get: (id) => apiClient.get(`/simulations/${id}`),
  
  addBody: (id, body) => apiClient.post(`/simulations/${id}/bodies`, body),
  removeBody: (id, bodyId) => apiClient.delete(`/simulations/${id}/bodies/${bodyId}`),
  
  start: (id) => apiClient.post(`/simulations/${id}/start`),
  stop: (id) => apiClient.post(`/simulations/${id}/stop`),
  step: (id, steps = 1) => apiClient.post(`/simulations/${id}/step`, null, { params: { steps } }),
  clear: (id) => apiClient.post(`/simulations/${id}/clear`),
}