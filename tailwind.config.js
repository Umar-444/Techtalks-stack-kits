/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./**/*.html",
    "./assets/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
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
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.03)',
        'soft-hover': '0 2px 8px rgba(0, 0, 0, 0.06), 0 8px 24px rgba(0, 0, 0, 0.05)',
        'hairline-bottom': '0 1px 0 0 rgba(0, 0, 0, 0.08)',
      }
    },
  },
  plugins: [],
}
