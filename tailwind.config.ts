import type { Config } from "tailwindcss";
import flowbitePlugin from 'flowbite/plugin'


export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],

  darkMode: 'selector',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FFF5F5',
          100: '#FFECEC',
          200: '#FFC7C7',
          300: '#FFA3A3',
          400: '#FF7E7E',
          500: '#FF4949',
          600: '#E63D3D',
          700: '#CC3333',
          800: '#B32A2A',
          900: '#991F1F'

        }
      }
    }
  },

  plugins: [flowbitePlugin],
} as Config;
