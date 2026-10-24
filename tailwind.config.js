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
        base: '#0A0A0B',
        raised: '#131316',
        strong: '#000000',
        hairline: '#26262C',
        'text-primary': '#F4F4F5',
        'text-body': '#C4C4CC',
        'text-muted': '#8E8E96',
        brand: '#e85d26',
        ink: '#12140F',
        muted: '#5C6058',
        paper: '#FFFFFF',
        tint: '#F7F7F3',
        line: '#E6E6DF',
        teal: '#0E7C6B',
        gold: '#B7791F',
        night: '#0A0A0B',
        surface: '#131316',
        nightline: '#26262C',
        nighttext: '#F4F4F5',
      },
      fontFamily: {
        sans: ['"Instrument Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
        serif: ['Newsreader', 'Georgia', 'serif'],
      },
      borderRadius: {
        btn: '6px',
        card: '8px',
        xs: '4px',
        sm: '6px',
        md: '8px',
        lg: '12px',
      },
      boxShadow: {
        'card-hover': '0 8px 24px rgba(0, 0, 0, 0.25)',
      }
    },
  },
  plugins: [],
}
