<template>
  <div class="map-view">
    <div id="amap-container" class="map-element"></div>
    
    <!-- 地图控制信息 -->
    <div class="map-info">
      <div class="info-card">
        <h3 class="text-lg font-bold text-gray-800">美食地点地图</h3>
        <p class="text-sm text-gray-600 mt-1">共 {{ validPlacesCount }} 个想去的地方</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  places: {
    type: Array,
    default: () => []
  },
  selectedPlace: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['select'])

let map = null
let markers = []

// 计算有效的地点数量（有名称或城市的）
const validPlacesCount = computed(() => {
  return props.places.filter(place => place.name || place.city).length
})

// 初始化地图
const initMap = () => {
  if (!window.AMap) {
    console.error('⚠️ 高德地图API未加载')
    console.error('请在 frontend/index.html 中配置你的高德地图 API Key')
    console.error('获取 API Key: https://console.amap.com/')
    
    // 显示错误提示
    const container = document.getElementById('amap-container')
    if (container) {
      container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 40px; text-align: center; background: #f3f4f6;">
          <div style="font-size: 48px; margin-bottom: 20px;">🗺️</div>
          <h2 style="font-size: 24px; color: #1f2937; margin-bottom: 12px;">地图未配置</h2>
          <p style="color: #6b7280; margin-bottom: 8px;">请配置高德地图 API Key</p>
          <p style="color: #9ca3af; font-size: 14px; max-width: 500px;">
            在 <code style="background: #fff; padding: 2px 6px; border-radius: 4px;">frontend/index.html</code> 中将 
            <code style="background: #fff; padding: 2px 6px; border-radius: 4px;">YOUR_AMAP_KEY</code> 
            替换为你的 API Key
          </p>
          <a href="https://console.amap.com/" target="_blank" style="margin-top: 20px; padding: 10px 20px; background: #ef4444; color: white; text-decoration: none; border-radius: 8px;">
            获取 API Key
          </a>
          <p style="margin-top: 20px; font-size: 14px; color: #6b7280;">
            查看详细说明：<code style="background: #fff; padding: 2px 6px; border-radius: 4px;">frontend/SETUP.md</code>
          </p>
        </div>
      `
    }
    return
  }

  map = new AMap.Map('amap-container', {
    zoom: 4, // 调整缩放级别，更适合查看整个中国
    center: [105, 35], // 中国中心坐标
    mapStyle: 'amap://styles/normal',
    viewMode: '2D',
    features: ['bg', 'road', 'building', 'point'], // 显示背景、道路、建筑、兴趣点
    pitch: 0, // 俯视角度
  })

  // 加载插件
  AMap.plugin(['AMap.ToolBar', 'AMap.Scale'], () => {
    // 添加工具条
    map.addControl(new AMap.ToolBar({
      position: {
        top: '20px',
        right: '20px'
      }
    }))

    // 添加比例尺
    map.addControl(new AMap.Scale())
  })
}

// 创建自定义标记
const createMarker = (place) => {
  if (!place.location || !place.location.lng || !place.location.lat) {
    return null
  }

  const position = new AMap.LngLat(place.location.lng, place.location.lat)

  // 创建自定义HTML标记
  const markerContent = document.createElement('div')
  markerContent.className = 'custom-marker'
  markerContent.innerHTML = `
    <div class="marker-inner">
      ${place.thumbnail 
        ? `<img src="${place.thumbnail}" alt="${place.name}" class="marker-image" />`
        : `<div class="marker-placeholder">🍴</div>`
      }
      <div class="marker-label">${place.name}</div>
    </div>
  `

  const marker = new AMap.Marker({
    position: position,
    content: markerContent,
    offset: new AMap.Pixel(-20, -40)
  })

  // 点击标记事件
  marker.on('click', () => {
    emit('select', place)
    map.setZoomAndCenter(14, position)
  })

  return marker
}

// 添加所有标记
const addMarkers = () => {
  // 清除现有标记
  if (markers.length > 0) {
    map.remove(markers)
    markers = []
  }

  // 添加新标记
  props.places.forEach(place => {
    const marker = createMarker(place)
    if (marker) {
      markers.push(marker)
      map.add(marker)
    }
  })

  // 自动调整视野
  if (markers.length > 0) {
    map.setFitView(markers, true, [50, 50, 50, 50])
  }
}

// 监听选中的地点
watch(() => props.selectedPlace, (newPlace) => {
  if (newPlace && newPlace.location) {
    const position = new AMap.LngLat(newPlace.location.lng, newPlace.location.lat)
    map.setZoomAndCenter(14, position, true)
  }
})

// 监听地点数据变化
watch(() => props.places, () => {
  if (map) {
    addMarkers()
  }
}, { deep: true })

onMounted(() => {
  initMap()
  
  // 等待地图加载完成后添加标记
  setTimeout(() => {
    if (props.places.length > 0) {
      addMarkers()
    }
  }, 500)
})
</script>

<style scoped>
.map-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-element {
  width: 100%;
  height: 100%;
}

.map-info {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  pointer-events: none;
}

.info-card {
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  pointer-events: auto;
}

/* 自定义标记样式 */
:deep(.custom-marker) {
  cursor: pointer;
  transition: all 0.3s ease;
}

:deep(.custom-marker:hover) {
  transform: scale(1.1);
}

:deep(.marker-inner) {
  position: relative;
  width: 40px;
  height: 40px;
}

:deep(.marker-image) {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ef4444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:deep(.marker-placeholder) {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:deep(.marker-label) {
  position: absolute;
  top: 45px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #1f2937;
}

@media (max-width: 768px) {
  .map-info {
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
  }

  .info-card {
    padding: 12px 16px;
  }

  .info-card h3 {
    font-size: 16px;
  }

  .info-card p {
    font-size: 12px;
  }
}
</style>

