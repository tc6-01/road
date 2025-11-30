import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { copyFileSync, mkdirSync } from 'fs'

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'copy-data',
      closeBundle() {
        // 确保dist/data目录存在
        mkdirSync(resolve(__dirname, 'dist/data'), { recursive: true })
        // 复制places.json到dist目录
        copyFileSync(
          resolve(__dirname, '../data/places.json'),
          resolve(__dirname, 'dist/data/places.json')
        )
      }
    }
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  },
  server: {
    port: 3000,
    open: true
  },
  publicDir: 'public'
})

