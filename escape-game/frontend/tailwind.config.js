/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Palette cyberpunk
        neon: {
          cyan: "#00f0ff",
          pink: "#ff00aa",
          purple: "#a855f7",
          green: "#39ff14",
          yellow: "#fde047",
        },
        bg: {
          dark: "#0a0a0f",
          panel: "#12121a",
          card: "#1a1a25",
          border: "#2a2a3a",
        },
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "'Fira Code'", "monospace"],
        display: ["'Orbitron'", "system-ui", "sans-serif"],
      },
      boxShadow: {
        neon: "0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3)",
        "neon-pink":
          "0 0 10px rgba(255, 0, 170, 0.5), 0 0 20px rgba(255, 0, 170, 0.3)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        scan: "scan 4s linear infinite",
      },
      keyframes: {
        scan: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
      },
    },
  },
  plugins: [],
};
