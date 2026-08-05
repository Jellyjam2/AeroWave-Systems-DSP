/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Titan Stealth Coating - Deep Void Black & Neon Accents
        void: {
          900: '#0a0a0f', // Deep void black
          800: '#12121a', // Void surface
          700: '#1a1a24', // Void highlight
        },
        neon: {
          cyan: '#00f0ff', // Titan cyan accent
          purple: '#b000ff', // Titan purple accent
          green: '#00ff88', // Titan green accent
          red: '#ff0044', // Titan red accent
        },
        glass: {
          surface: 'rgba(10, 10, 15, 0.8)',
          border: 'rgba(0, 240, 255, 0.1)',
          highlight: 'rgba(0, 240, 255, 0.05)',
        }
      },
      backgroundImage: {
        'void-gradient': 'linear-gradient(135deg, #0a0a0f 0%, #1a1a24 100%)',
        'neon-glow': 'radial-gradient(circle, rgba(0, 240, 255, 0.15) 0%, transparent 70%)',
        'command-grid': `
          linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px)
        `,
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'neon-flicker': 'neon-flicker 2s ease-in-out infinite',
        'scanline': 'scanline 8s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'neon-flicker': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 240, 255, 0.3), 0 0 40px rgba(0, 240, 255, 0.1)',
        'neon-purple': '0 0 20px rgba(176, 0, 255, 0.3), 0 0 40px rgba(176, 0, 255, 0.1)',
        'glass': '0 8px 32px rgba(0, 0, 0, 0.4)',
      },
      backdropBlur: {
        'glass': '20px',
      },
    },
  },
  plugins: [],
}
