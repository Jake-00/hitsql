import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // '^/id/.*': {
      //   target: 'http://localhost:8080/quiz/v1',
      //   changeOrigin: true,
      //   rewrite: (path) => path.replace(/^\/id/, ''),
      // },
      '/transpile': {
        target: 'http://127.0.0.1:8000/transpile',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/transpile/, ''),
      }
    }
  }
})
