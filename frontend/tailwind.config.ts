import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0A1929', // Old money navy blue
        'navy-dark': '#0D1B2A', // Deep navy
        'navy-light': '#1B263B', // Lighter navy
        accent: '#1C8B3E', // Rolex green
        'green-dark': '#155D27', // Darker green
        'green-light': '#2DB954', // Lighter green
        background: '#F5F7FA', // Soft off-white
        'gold-accent': '#D4AF37', // Luxury gold accent
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
export default config

