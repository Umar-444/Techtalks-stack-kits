/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './**/*.html',
    './assets/js/**/*.js',
    './kits/**/*.html',
    './blog/**/*.html',
    './security/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        ink: '#12140F',
        muted: '#5C6058',
        paper: '#FFFFFF',
        tint: '#F7F7F3',
        line: '#E6E6DF',
        brand: '#E85D26',
        teal: '#0E7C6B',
        gold: '#B7791F',
        night: '#0F1110',
        surface: '#171A18',
        nightline: '#2A2E2A',
        nighttext: '#F2F2EC',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
        serif: ['Newsreader', 'Georgia', 'serif'],
      },
      borderRadius: {
        btn: '6px',
        card: '8px',
        xs: '4px',
        sm: '8px',
        md: '12px',
      },
      boxShadow: {
        'card-hover': '0 8px 24px rgba(18, 20, 15, 0.06)',
      }
    },
  },
  plugins: [],
}
