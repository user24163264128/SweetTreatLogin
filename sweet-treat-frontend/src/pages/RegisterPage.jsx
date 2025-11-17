import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api/api";
import DarkVeil from "../components/DarkVeil";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Simple auto-increment ID (replace with backend-generated in production)
      const id = Date.now();
      await registerUser({ id, username, email, password, role });
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-black overflow-hidden">
      {/* Grid Distortion Background */}
      <div className="absolute inset-0 z-0">
        <DarkVeil></DarkVeil>
      </div>

      {/* Translucent Register Form */}
      <div className="relative z-10 backdrop-blur-lg bg-white/10 border border-white/30 p-10 rounded-2xl shadow-2xl w-full max-w-md">
        <h2 className="text-4xl font-bold mb-8 text-center text-white">Register</h2>
        {error && <p className="text-red-300 mb-6 text-center text-lg">{error}</p>}
        <input
          type="text"
          placeholder="Username"
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg placeholder-white/60 p-4 mb-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg placeholder-white/60 p-4 mb-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg placeholder-white/60 p-4 mb-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg p-4 mb-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
        >
          <option value="user" className="bg-gray-900">User</option>
          <option value="admin" className="bg-gray-900">Admin</option>
        </select>
        <button
          onClick={handleSubmit}
          className="w-full bg-pink-600 text-white text-lg p-4 rounded-lg hover:bg-pink-700 transition font-semibold shadow-lg"
        >
          Register
        </button>
      </div>
    </div>
  );
}