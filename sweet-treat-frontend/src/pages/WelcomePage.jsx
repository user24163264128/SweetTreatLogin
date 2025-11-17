import { useNavigate } from "react-router-dom";
import Beams from '../components/Beams';
import BlurText from '../components/BlurText';

export default function WelcomePage() {
  const navigate = useNavigate();

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }} className="relative min-h-screen bg-black text-white flex flex-col justify-center items-center overflow-hidden">
      {/* Beams in the background */}
      <div className="absolute inset-0 z-0">
        <Beams
          beamWidth={3}
          beamHeight={24}
          beamNumber={5}
          lightColor="#ffffff"
          speed={2}
          noiseIntensity={2}
          scale={0.15}
          rotation={40}
        />
      </div>

      {/* Background glow effect */}
      <div className="absolute w-[150%] h-[150%]" />

      {/* Main content with translucent box */}
      <div className="relative z-20 backdrop-blur-md bg-white/10 rounded-3xl border border-white/20 shadow-2xl px-12 py-16">
        <div className="text-center space-y-6">
          <BlurText
            text="Sweet Treat"
            delay={150}
            animateBy="words"
            direction="top"
            className="text-6xl md:text-8xl font-extrabold tracking-tight text-white drop-shadow-lg"
          />
          
          <BlurText
            text="The only cooking AI you will need"
            delay={150}
            animateBy="words"
            direction="top"
            className="text-lg md:text-xl text-gray-300 drop-shadow-sm center"
          />

          {/* Buttons */}
          <div className="flex gap-4 justify-center mt-8">
            <button
              onClick={() => navigate("/login")}
              className="px-6 py-3 rounded-full bg-green-500 hover:bg-green-600 transition shadow-lg font-semibold"
            >
              Login
            </button>
            <button
              onClick={() => navigate("/register")}
              className="px-6 py-3 rounded-full border border-white hover:bg-white hover:text-black transition shadow-lg font-semibold"
            >
              Register
            </button>
          </div>
        </div>
      </div>

      {/* Footer info / small text */}
      <div className="absolute bottom-6 text-gray-500 text-sm z-20 text-center">
        <BlurText
          text="© 2025 SweetTreats. All rights reserved."
          delay={150}
          animateBy="words"
          direction="top"
          className="text-gray-500 text-sm"
        />
      </div>
    </div>
  );
}