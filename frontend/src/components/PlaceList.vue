<template>
  <div class="place-list">
    <!-- 头部 -->
    <div class="list-header">
      <h2 class="header-title">想去的地方</h2>
      <button class="close-btn" @click="$emit('close')">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 搜索框 -->
    <div class="search-box">
      <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索地点或美食..."
        class="search-input"
      />
    </div>

    <!-- 统计信息 -->
    <div class="stats">
      <div class="stat-item">
        <span class="stat-label">总计</span>
        <span class="stat-value">{{ filteredPlaces.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">城市</span>
        <span class="stat-value">{{ uniqueCities }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">美食</span>
        <span class="stat-value">{{ totalFoods }}</span>
      </div>
    </div>

    <!-- 地点列表 -->
    <div class="places-scroll">
      <div v-if="filteredPlaces.length === 0" class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="empty-text">暂无数据</p>
        <p class="empty-hint">使用Python脚本添加第一个地点吧!</p>
      </div>

      <div v-else>
        <!-- 按省份分组 -->
        <div v-for="(group, province) in groupedPlaces" :key="province" class="province-group">
          <h3 class="province-title">{{ province || '未知省份' }}</h3>
          
          <div
            v-for="place in group"
            :key="place.id"
            class="place-card"
            :class="{ 'place-card-active': selectedPlace?.id === place.id }"
            @click="$emit('select', place)"
          >
            <!-- 缩略图 -->
            <div class="place-thumbnail">
              <img
                v-if="place.thumbnail"
                :src="place.thumbnail"
                :alt="place.name"
                class="thumbnail-img"
              />
              <div v-else class="thumbnail-placeholder">
                🍴
              </div>
            </div>

            <!-- 信息 -->
            <div class="place-info">
              <h4 class="place-name">{{ place.name }}</h4>
              <p class="place-location">
                <svg class="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ place.city }}{{ place.address ? ` · ${place.address.substring(0, 20)}` : '' }}
              </p>
              <div class="place-foods">
                <span
                  v-for="(food, idx) in place.foods.slice(0, 3)"
                  :key="idx"
                  class="food-tag"
                >
                  {{ food.name }}
                </span>
                <span v-if="place.foods.length > 3" class="food-tag">
                  +{{ place.foods.length - 3 }}
                </span>
              </div>
            </div>

            <!-- 箭头 -->
            <div class="place-arrow">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

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

defineEmits(['select', 'close'])

const searchQuery = ref('')

// 过滤地点
const filteredPlaces = computed(() => {
  if (!searchQuery.value) return props.places

  const query = searchQuery.value.toLowerCase()
  return props.places.filter(place => {
    return (
      place.name?.toLowerCase().includes(query) ||
      place.city?.toLowerCase().includes(query) ||
      place.address?.toLowerCase().includes(query) ||
      place.foods?.some(food => food.name.toLowerCase().includes(query))
    )
  })
})

// 按省份分组
const groupedPlaces = computed(() => {
  const groups = {}
  filteredPlaces.value.forEach(place => {
    const province = place.province || '未知省份'
    if (!groups[province]) {
      groups[province] = []
    }
    groups[province].push(place)
  })
  return groups
})

// 统计信息
const uniqueCities = computed(() => {
  const cities = new Set(filteredPlaces.value.map(p => p.city).filter(Boolean))
  return cities.size
})

const totalFoods = computed(() => {
  return filteredPlaces.value.reduce((sum, place) => sum + (place.foods?.length || 0), 0)
})
</script>

<style scoped>
.place-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.close-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.search-box {
  position: relative;
  padding: 0 20px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.search-icon {
  position: absolute;
  left: 32px;
  top: 12px;
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.stats {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: #ef4444;
}

.places-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: #9ca3af;
}

.province-group {
  margin-bottom: 24px;
}

.province-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.place-card {
  display: flex;
  gap: 12px;
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.place-card:hover {
  border-color: #ef4444;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.1);
  transform: translateY(-2px);
}

.place-card-active {
  border-color: #ef4444;
  background: #fef2f2;
}

.place-thumbnail {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.thumbnail-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.place-info {
  flex: 1;
  min-width: 0;
}

.place-name {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.location-icon {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
}

.place-foods {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.food-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #fee2e2;
  color: #dc2626;
  font-size: 12px;
  border-radius: 4px;
  font-weight: 500;
}

.place-arrow {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .close-btn {
    display: block;
  }
}
</style>

