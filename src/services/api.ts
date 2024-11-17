import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (name: string, email: string, password: string) => {
    const response = await api.post('/auth/register', { name, email, password });
    return response.data;
  },
};

export const downloader = {
  youtube: async (url: string, format: string) => {
    const response = await api.post('/download/youtube', { url, format });
    return response.data;
  },
  
  instagram: async (url: string, type: string) => {
    const response = await api.post('/download/instagram', { url, type });
    return response.data;
  },
  
  pinterest: async (url: string, quality: string) => {
    const response = await api.post('/download/pinterest', { url, quality });
    return response.data;
  },

  linkedin: async (url: string, type: string) => {
    const response = await api.post('/download/linkedin', { url, type });
    return response.data;
  },

  twitter: async (url: string, quality: string) => {
    const response = await api.post('/download/twitter', { url, quality });
    return response.data;
  },

  snapchat: async (url: string, type: string) => {
    const response = await api.post('/download/snapchat', { url, type });
    return response.data;
  },
};

export default api;