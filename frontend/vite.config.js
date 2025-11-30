import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { copyFileSync, mkdirSync, existsSync, watch } from 'fs'

export default defineConfig(({ mode }) => {
  // 加载环境变量（优先从系统环境变量读取，兼容 GitHub Actions）
  const env = loadEnv(mode, process.cwd(), '')
  
  // 从系统环境变量读取（GitHub Actions 中使用）
  const VITE_AMAP_KEY = process.env.VITE_AMAP_KEY || env.VITE_AMAP_KEY || ''
  
  console.log('\n' + '='.repeat(60))
  console.log('🔧 Vite 构建配置')
  console.log('='.repeat(60))
  console.log('构建模式:', mode)
  console.log('process.env.VITE_AMAP_KEY:', process.env.VITE_AMAP_KEY ? `✓ 已设置 (${process.env.VITE_AMAP_KEY.length} 字符)` : '✗ 未设置')
  console.log('loadEnv 读取值:', env.VITE_AMAP_KEY ? `✓ 已设置 (${env.VITE_AMAP_KEY.length} 字符)` : '✗ 未设置')
  console.log('最终使用值:', VITE_AMAP_KEY ? `✅ 已设置 (${VITE_AMAP_KEY.length} 字符)` : '❌ 未设置')
  console.log('='.repeat(60) + '\n')
  
  return {
    plugins: [
      vue(),
      {
        name: 'copy-data',
        // 在开发和构建时都复制数据文件
        configureServer(server) {
          // 开发环境：将 data 文件夹内容复制到 public/data
          const publicDataDir = resolve(__dirname, 'public/data')
          const sourceDataFile = resolve(__dirname, '../data/places.json')
          
          if (!existsSync(publicDataDir)) {
            mkdirSync(publicDataDir, { recursive: true })
          }
          
          // 初始复制
          if (existsSync(sourceDataFile)) {
            copyFileSync(sourceDataFile, resolve(publicDataDir, 'places.json'))
          }
          
          // 监听文件变化
          try {
            watch(resolve(__dirname, '../data'), (eventType, filename) => {
              if (filename === 'places.json') {
                copyFileSync(sourceDataFile, resolve(publicDataDir, 'places.json'))
                console.log('✓ places.json 已更新')
              }
            })
          } catch (e) {
            // 忽略监听错误（可能是目录不存在）
          }
        },
        closeBundle() {
          // 构建环境：复制到 dist/data
          mkdirSync(resolve(__dirname, 'dist/data'), { recursive: true })
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
    publicDir: 'public',
    // 定义全局常量替换，确保环境变量在构建时被注入
    define: {
      'import.meta.env.VITE_AMAP_KEY': JSON.stringify(VITE_AMAP_KEY)
    }
  }
})

