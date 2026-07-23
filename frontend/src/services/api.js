/**
 * Centralized Axios instance for all API requests.
 *
 * Base URL points to the FastAPI backend running on localhost:8000.
 * The /api/v1 prefix matches the backend's API_V1_STR setting.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export default api;
