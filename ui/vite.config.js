import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';

export default defineConfig({
  base: '/log',
  plugins: [solidPlugin()],
  server: {
    port: 3000,
    proxy: {
      '/api/log': {
        target: 'ws://localhost:8000',
        ws: true,
      }
    }
  },
  build: {
    target: 'esnext',
  },
});
