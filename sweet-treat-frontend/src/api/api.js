import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true, // to send cookies for refresh token
});

// Login user
export const loginUser = (email, password) =>
  api.post("/auth/login", new URLSearchParams({ username: email, password }));

// Register user
export const registerUser = ({ id, username, email, password, role }) =>
  api.post("/auth/register", { id, username, email, password, role });

// Refresh token
export const refreshToken = () => api.post("/auth/refresh");

// Get current user
export const getCurrentUser = (token) =>
  api.get("/auth/me", { headers: { Authorization: `Bearer ${token}` } });

export default api;
