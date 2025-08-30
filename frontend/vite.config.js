import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');

  return {
    plugins: [react()],
    server: {
      host: true,
      port: 80,
      proxy: {
        '/^(?!.*\\\.\\w+$).*$': {
          target: 'http://postgrest:3000',
          changeOrigin: true,
        },
      },
      watch: {
        usePolling: true,
      },
    },
    preview: {
      host: true,
      port: 80,
    },
    define: {
      'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
      'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY),
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
  };
});
