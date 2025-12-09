import axios from "axios";

// Leer URL desde variables de entorno de Vercel
const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: `${API_URL}/api`,
});

// 🔥 INTERCEPTOR JWT — AÑADE TOKEN Y HEADERS A TODAS LAS PETICIONES
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  config.headers["Content-Type"] = "application/json";
  config.headers["Accept"] = "application/json";

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
