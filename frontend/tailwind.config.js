/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1A2B4B',
          foreground: '#FFFFFF',
        },
        secondary: {
          DEFAULT: '#5D7A68',
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#C87961',
          foreground: '#FFFFFF',
        },
        background: '#F9F8F6',
        paper: '#FFFFFF',
        subtle: '#F2F0EB',
        border: 'rgba(0, 0, 0, 0.08)',
        input: 'rgba(0, 0, 0, 0.1)',
        ring: '#1A2B4B',
      },
      fontFamily: {
        heading: ['Playfair Display', 'serif'],
        body: ['Manrope', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '24px',
      },
      boxShadow: {
        card: '0 2px 8px -2px rgba(26, 43, 75, 0.05), 0 4px 16px -4px rgba(26, 43, 75, 0.02)',
        float: '0 12px 32px -8px rgba(26, 43, 75, 0.12)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
