import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: parseInt(process.env.FRONTEND_PORT || '8080', 10),
    proxy: {
      '/api': {
        target: 'http://agents:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/jobs': {
        target: 'http://jobspy_service:8000',
        changeOrigin: true,
      },
    },
    watch: {
      usePolling: true,
    },
  },
  preview: {
    host: true,
    port: parseInt(process.env.FRONTEND_PORT || '8080', 10),
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
    },
  },
});
