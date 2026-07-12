import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Le frontend appelle l'API via /api ; en dev, Vite proxie vers le backend.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
