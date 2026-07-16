/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: '#7C3AED',
        button: '#FF6B00',
        appBackground: '#F8FAFC',
        appText: '#0F172A',
        appTextSecondary: '#475569',
        buttonText: '#FFFFFF',
        appBorder: '#E2E8F0',
        appCard: '#FFFFFF',
        accent: '#84CC16',

        // Dark mode variants
        'primary-dark': '#6C4FB3',
        'button-dark': '#D25D12',
        'appBackground-dark': '#0B0F19',
        'appText-dark': '#E2E8F0',
        'appTextSecondary-dark': '#94A3B8',
        'buttonText-dark': '#F1F5F9',
        'appBorder-dark': '#1E293B',
        'appCard-dark': '#131C2E',
        'accent-dark': '#557A1E',
      },
    },
  },
  plugins: [],
}