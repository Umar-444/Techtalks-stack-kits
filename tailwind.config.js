/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./**/*.html",
    "./assets/js/**/*.js",
    "./kits/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          orange: '#E85D26',
          'orange-hover': '#cf4d19',
          'orange-bg': '#FFF1E8',
          'orange-dark-bg': '#2A1E16',
          teal: '#0E7C6B',
          'teal-hover': '#095c4f',
          'teal-dark': '#1DB89E',
          'teal-bg': '#E6F4F1',
          'teal-dark-bg': '#122A26',
          gold: '#B7791F',
          'gold-dark': '#D4952C',
          'gold-bg': '#FEF6D8',
          'gold-dark-bg': '#2A2410',
          bg: '#FFFFFF',
          'bg-dark': '#0F1110',
          bg2: '#F4F4F0',
          'bg2-dark': '#171A18',
          card: '#FFFFFF',
          'card-dark': '#171A18',
          line: '#E6E6DF',
          'line-dark': '#2A2E2A',
          ink: '#12140F',
          'ink-dark': '#F2F2EC',
          muted: '#5C6058',
          'muted-dark': '#A8ACA0',
          soft: '#8A8D84',
          'soft-dark': '#7D8178'
        },
        primary: {
          DEFAULT: '#0075DE',
          link: '#097FE8',
          pressed: '#005BAB',
          tint: '#E6F3FE',
          focus: '#0075DE',
        },
        ink: {
          DEFAULT: '#000000',
          secondary: '#615D59',
          muted: '#A39E98',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          warm: '#F6F5F4',
          card: '#FFFFFF',
          hairline: '#DFDCD9',
        },
        accent: {
          amber: '#FFB110',
          amberDeep: '#E89D01',
          coral: '#F64932',
          red: '#E32D14',
          success: '#1AAE39',
          successTint: '#D0F4D8',
          indigo: '#1313BA',
          lavender: '#EADBFA',
        },
        dark: {
          bg: '#141414',
          surface: '#1A1A1A',
          card: '#202020',
          border: '#2E2E2E',
          text: '#F5F5F5',
          muted: '#9E9E9E',
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['"Lyon Text"', 'Georgia', 'Cambria', 'serif'],
        mono: ['"JetBrains Mono"', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      borderRadius: {
        xs: '4px',
        sm: '8px',
        md: '12px',
        lg: '16px',
        xl: '20px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.03)',
        'soft-hover': '0 2px 8px rgba(0, 0, 0, 0.06), 0 8px 24px rgba(0, 0, 0, 0.05)',
        'card-kit': '0 1px 3px rgba(18, 20, 15, 0.04), 0 6px 16px rgba(18, 20, 15, 0.04)',
        'card-kit-hover': '0 4px 12px rgba(232, 93, 38, 0.08), 0 12px 32px rgba(18, 20, 15, 0.08)',
        'hairline-bottom': '0 1px 0 0 rgba(0, 0, 0, 0.08)',
      }
    },
  },
  plugins: [],
}
