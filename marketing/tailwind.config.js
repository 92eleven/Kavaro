/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1E2128',
        accent: '#00C9E8',
        'deep-accent': '#00A3BF',
        text: '#0F0F1A',
        surface: '#F4F6F9',
        background: '#EAECF0',
      },
      fontFamily: {
        exo: ['"Exo 2"', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'fade-in': 'fade-in 0.5s ease-out forwards',
        'fade-out': 'fade-out 0.5s ease-out forwards',
        'flicker': 'flicker 0.15s ease-in-out',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': {
            textShadow: '0 0 12px #00C9E8, 0 0 24px rgba(0, 201, 232, 0.6)',
          },
          '50%': {
            textShadow: '0 0 16px #00C9E8, 0 0 32px rgba(0, 201, 232, 0.8)',
          },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-out': {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },
        'flicker': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
      },
    },
  },
  plugins: [],
};
