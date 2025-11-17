// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { loginUser } from "../api/api";
// import Aurora from "../components/Aurora";

// export default function LoginPage() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const res = await loginUser(email, password);
//       const { access_token, redirect } = res.data;
//       localStorage.setItem("access_token", access_token);
//       navigate("/profile");
//     } catch (err) {
//       setError(err.response?.data?.detail || "Login failed");
//     }
//   };

//   return (
//     <div className="relative min-h-screen flex items-center justify-center bg-black overflow-hidden">
//       <div className="absolute inset-0 z-0">
//         <Aurora
//           colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
//           blend={0.5}
//           amplitude={1.0}
//           speed={0.5}
//         />
//       </div>

//       <form
//         onSubmit={handleSubmit}
//         className="relative z-10 bg-black border border-white/20 p-8 rounded-xl shadow-2xl w-full max-w-sm"
//       >
//         <h2 className="text-2xl font-bold mb-6 text-center text-white">Login</h2>
//         {error && <p className="text-red-400 mb-4 text-center">{error}</p>}
//         <input
//           type="email"
//           placeholder="Email"
//           className="w-full bg-gray-900 border border-gray-700 text-white placeholder-gray-400 p-3 mb-4 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//           required
//         />
//         <input
//           type="password"
//           placeholder="Password"
//           className="w-full bg-gray-900 border border-gray-700 text-white placeholder-gray-400 p-3 mb-6 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           required
//         />
//         <button
//           type="submit"
//           className="w-full bg-purple-600 text-white p-3 rounded hover:bg-purple-700 transition font-semibold"
//         >
//           Login
//         </button>
//       </form>
//     </div>
//   );
// }

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/api";
import DarkVeil from "../components/DarkVeil";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(email, password);
      const { access_token, redirect } = res.data;
      localStorage.setItem("access_token", access_token);
      navigate("/profile");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-black overflow-hidden">
      {/* Grid Distortion Background */}
      <div className="absolute inset-0 z-0">
        <DarkVeil></DarkVeil>
      </div>

      {/* Translucent Login Form */}
      <div className="relative z-10 backdrop-blur-lg bg-white/10 border border-white/30 p-10 rounded-2xl shadow-2xl w-full max-w-md">
        <h2 className="text-4xl font-bold mb-8 text-center text-white">LOGIN</h2>
        {error && <p className="text-red-300 mb-6 text-center text-lg">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg placeholder-white/60 p-4 mb-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full bg-white/20 backdrop-blur-sm border border-white/40 text-white text-lg placeholder-white/60 p-4 mb-8 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          onClick={handleSubmit}
          className="w-full bg-purple-600 text-white text-lg p-4 rounded-lg hover:bg-purple-700 transition font-semibold shadow-lg"
        >
          Login
        </button>
      </div>
    </div>
  );
}