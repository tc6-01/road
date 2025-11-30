<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <aside 
      class="sidebar"
      :class="{ 'sidebar-open': sidebarOpen }"
    >
      <PlaceList 
        :places="places"
        :selected-place="selectedPlace"
        @select="handleSelectPlace"
        @close="sidebarOpen = false"
      />
    </aside>

    <!-- 地图容器 -->
    <main class="map-container">
      <MapView
        :places="places"
        :selected-place="selectedPlace"
        @select="handleSelectPlace"
      />
      
      <!-- 移动端菜单按钮 -->
      <button
        class="mobile-menu-btn"
        @click="sidebarOpen = !sidebarOpen"
      >
        <svg v-if="!sidebarOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </main>

    <!-- 地点详情弹窗 -->
    <PlaceDetail
      v-if="selectedPlace"
      :place="selectedPlace"
      @close="selectedPlace = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MapView from './components/MapView.vue'
import PlaceList from './components/PlaceList.vue'
import PlaceDetail from './components/PlaceDetail.vue'

const places = ref([])
const selectedPlace = ref(null)
const sidebarOpen = ref(false)

// 加载地点数据
const loadPlaces = async () => {
  try {
    const response = await fetch('/data/places.json')
    const data = await response.json()
    places.value = data.places || []
  } catch (error) {
    console.error('加载数据失败:', error)
    places.value = []
  }
}

// 选择地点
const handleSelectPlace = (place) => {
  selectedPlace.value = place
}

onMounted(() => {
  loadPlaces()
})
</script>

<style scoped>
.app-container {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 360px;
  height: 100%;
  background: white;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  transition: transform 0.3s ease;
}

.map-container {
  flex: 1;
  position: relative;
  height: 100%;
}

.mobile-menu-btn {
  display: none;
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 50;
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.mobile-menu-btn:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.mobile-menu-btn:active {
  transform: scale(0.95);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    width: 85%;
    max-width: 360px;
  }

  .sidebar-open {
    transform: translateX(0);
  }

  .mobile-menu-btn {
    display: block;
  }
}
</style>

