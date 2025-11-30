import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// 动态加载高德地图 API
const loadAMap = () => {
  return new Promise((resolve, reject) => {
    // 如果已经加载，直接返回
    if (window.AMap) {
      resolve(window.AMap)
      return
    }

    // 获取环境变量中的 API Key
    const AMAP_KEY = import.meta.env.VITE_AMAP_KEY || ''

    console.log('🔍 环境变量检查:')
    console.log('  - 环境模式:', import.meta.env.MODE)
    console.log('  - 生产环境:', import.meta.env.PROD)
    console.log('  - VITE_AMAP_KEY:', AMAP_KEY ? `已设置 (长度: ${AMAP_KEY.length})` : '❌ 未设置')

    if (!AMAP_KEY) {
      console.warn('⚠️  未配置高德地图 API Key')
      if (import.meta.env.PROD) {
        console.warn('生产环境: 请在 GitHub Secrets (Environments > script_env) 中配置 VITE_AMAP_KEY')
      } else {
        console.warn('开发环境: 请在 frontend/.env 文件中配置 VITE_AMAP_KEY')
      }
      resolve(null) // 即使没有配置也继续，只是地图功能不可用
      return
    }

    // 动态创建 script 标签加载高德地图
    const script = document.createElement('script')
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_KEY}`
    script.async = true
    script.onload = () => {
      console.log('✓ 高德地图 API 加载成功')
      resolve(window.AMap)
    }
    script.onerror = () => {
      console.error('✗ 高德地图 API 加载失败')
      console.error('请检查网络连接和 API Key 是否正确')
      resolve(null) // 加载失败也继续，只是地图功能不可用
    }
    document.head.appendChild(script)
  })
}

// 先加载高德地图，再初始化 Vue 应用
loadAMap().then(() => {
  const app = createApp(App)
  app.mount('#app')
})

