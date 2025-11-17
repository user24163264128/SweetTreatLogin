import { useEffect, useState } from "react";
import axios from "axios";
import DarkVeil from "../components/DarkVeil";

export default function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchUser() {
      try {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
          setError("You are not logged in.");
          setLoading(false);
          return;
        }

        const res = await axios.get("http://localhost:8000/auth/me", {
          headers: { Authorization: `Bearer ${accessToken}` },
          withCredentials: true
        });

        setUser(res.data);
      } catch (err) {
        setError("Could not load profile.");
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, []);

  if (loading)
    return (
      <div className="relative min-h-screen bg-black flex items-center justify-center text-white overflow-hidden">
        <div className="absolute inset-0 z-0">
          <DarkVeil></DarkVeil>
        </div>
        <div className="relative z-10 backdrop-blur-lg bg-white/10 border border-white/30 px-12 py-6 rounded-2xl">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-xl font-semibold">Loading profile...</span>
          </div>
        </div>
      </div>
    );

  if (error)
    return (
      <div className="relative min-h-screen bg-black flex flex-col items-center justify-center text-red-400 text-xl overflow-hidden">
        <div className="absolute inset-0 z-0">
          <DarkVeil></DarkVeil>
        </div>
        <div className="relative z-10 backdrop-blur-lg bg-red-500/10 border border-red-400/50 px-12 py-8 rounded-2xl text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <div className="text-2xl font-semibold text-red-300">{error}</div>
          <button
            onClick={() => window.location.href = "/login"}
            className="mt-6 px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg transition font-semibold"
          >
            Go to Login
          </button>
        </div>
      </div>
    );

  return (
    <div className="relative min-h-screen bg-black text-white flex flex-col items-center justify-center overflow-hidden">
      {/* Grid Distortion Background */}
      <div className="absolute inset-0 z-0">
        <DarkVeil></DarkVeil>
      </div>

      {/* Profile Card */}
      <div className="relative z-10 backdrop-blur-xl bg-gradient-to-br from-white/15 to-white/5 p-12 rounded-3xl shadow-2xl border border-white/30 w-11/12 md:w-2/5 lg:w-1/3">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-5xl font-bold shadow-lg">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent drop-shadow-lg">
            {user.username}
          </h1>
          <div className="mt-2 inline-block px-4 py-1 bg-purple-500/30 border border-purple-400/50 rounded-full text-sm font-semibold uppercase tracking-wider">
            {user.role}
          </div>
        </div>

        {/* Profile Details */}
        <div className="space-y-6 mb-10">
          <div className="backdrop-blur-sm bg-white/10 p-5 rounded-xl border border-white/20">
            <div className="text-sm font-semibold text-gray-300 mb-1 uppercase tracking-wide">Email Address</div>
            <div className="text-lg font-medium text-white">{user.email}</div>
          </div>

          <div className="backdrop-blur-sm bg-white/10 p-5 rounded-xl border border-white/20">
            <div className="text-sm font-semibold text-gray-300 mb-1 uppercase tracking-wide">Username</div>
            <div className="text-lg font-medium text-white">{user.username}</div>
          </div>

          <div className="backdrop-blur-sm bg-white/10 p-5 rounded-xl border border-white/20">
            <div className="text-sm font-semibold text-gray-300 mb-1 uppercase tracking-wide">Account Type</div>
            <div className="text-lg font-medium text-white capitalize">{user.role}</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={async () => {
              try {
                await axios.post("http://localhost:8000/auth/logout", {}, { withCredentials: true });
              } catch (err) {}
              localStorage.removeItem("access_token");
              window.location.href = "/login";
            }}
            className="flex-1 px-6 py-4 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl hover:from-red-600 hover:to-pink-600 transition font-semibold shadow-lg text-lg"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}