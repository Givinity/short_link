/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        accent: '#A855F7',
        'surface-primary': '#0A0A0A',
        'surface-secondary': '#1A1A1A',
        'surface-inverse': '#FFFFFF',
        'fg-primary': '#FFFFFF',
        'fg-secondary': '#A1A1AA',
        'fg-muted': '#71717A',
        'fg-inverse': '#0A0A0A',
        'divider': '#27272A',
        'green-dot': '#22C55E',
      },
      borderRadius: {
        'design-lg': '8px',
        'design-xl': '12px',
        'design-2xl': '16px',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['"Geist Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
