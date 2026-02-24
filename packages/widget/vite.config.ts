import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: 'src/index.ts',
      name: 'AutoBotWidget',
      formats: ['iife'],
      fileName: () => 'autobot-widget.js',
    },
    rollupOptions: {
      // Bundle everything (React included) for standalone embed
    },
    cssCodeSplit: false,
    minify: 'terser',
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
})
