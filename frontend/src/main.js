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
    const AMAP_SECURITY_CODE = import.meta.env.VITE_AMAP_SECURITY_CODE || ''

    if (!AMAP_KEY) {
      console.warn('⚠️  未配置高德地图 API Key')
      console.warn('请在 frontend/.env 文件中配置 VITE_AMAP_KEY')
      console.warn('或在 frontend/index.html 中手动配置')
      resolve(null) // 即使没有配置也继续，只是地图功能不可用
      return
    }

    // 配置安全密钥（可选）
    if (AMAP_SECURITY_CODE) {
      window._AMapSecurityConfig = {
        securityJsCode: AMAP_SECURITY_CODE
      }
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

