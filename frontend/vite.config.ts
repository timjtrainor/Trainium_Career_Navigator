import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Uncomment to proxy API requests to backend
  // server: {
  //   proxy: {
  //     '/api': 'http://localhost:8000',
  //   },
  // },
});
