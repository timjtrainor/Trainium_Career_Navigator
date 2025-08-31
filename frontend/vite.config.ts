import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Development proxy - in production Kong handles API routing
  server: {
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
});
