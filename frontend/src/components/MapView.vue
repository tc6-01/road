<template>
  <div class="map-view">
    <div id="amap-container" class="map-element"></div>
    
    <!-- 地图控制信息 -->
    <div class="map-info">
      <div class="info-card">
        <h3 class="text-lg font-bold text-gray-800">美食地点地图</h3>
        <p class="text-sm text-gray-600 mt-1">共 {{ places.length }} 个想去的地方</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

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

// 初始化地图
const initMap = () => {
  if (!window.AMap) {
    console.error('高德地图API未加载')
    return
  }

  map = new AMap.Map('amap-container', {
    zoom: 5,
    center: [104.06667, 30.57222], // 成都坐标作为默认中心
    mapStyle: 'amap://styles/normal',
    viewMode: '2D'
  })

  // 添加工具条
  map.addControl(new AMap.ToolBar({
    position: {
      top: '20px',
      right: '20px'
    }
  }))

  // 添加比例尺
  map.addControl(new AMap.Scale())
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

