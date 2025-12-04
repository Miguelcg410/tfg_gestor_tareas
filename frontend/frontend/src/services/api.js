import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
});

// 🔥 INTERCEPTOR JWT — AÑADE TOKEN Y HEADERS A TODAS LAS PETICIONES
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  // Cabeceras necesarias para evitar el error 422 en Flask-JWT
  config.headers["Content-Type"] = "application/json";
  config.headers["Accept"] = "application/json";

  // Añadir token si existe
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
