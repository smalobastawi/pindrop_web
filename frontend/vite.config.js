import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  envDir: '../',
  plugins: [vue({
    template: {
      compilerOptions: {
        isCustomElement: (tag) => tag.startsWith('gmp-')
      }
    }
  })],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_APP_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
      '/admin-api': {
        target: process.env.VITE_APP_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: process.env.VITE_APP_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  build: {
    // For development/testing - outputs to dist
    outDir: process.env.NODE_ENV === 'production' 
      ? '../templates/frontend' 
      : 'dist',
    
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['bootstrap']
        }
      }
    }
  }
})