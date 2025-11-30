<template>
  <div class="detail-overlay" @click="$emit('close')">
    <div class="detail-modal" @click.stop>
      <!-- 关闭按钮 -->
      <button class="close-btn" @click="$emit('close')">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- 内容 -->
      <div class="detail-content">
        <!-- 封面图片 -->
        <div v-if="place.thumbnail" class="detail-cover">
          <img :src="place.thumbnail" :alt="place.name" class="cover-img" />
        </div>

        <!-- 标题 -->
        <div class="detail-header">
          <h2 class="detail-title">{{ place.name }}</h2>
          <p class="detail-location">
            <svg class="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ place.province }} {{ place.city }}
          </p>
          <p v-if="place.address" class="detail-address">{{ place.address }}</p>
        </div>

        <!-- 美食列表 -->
        <div v-if="place.foods && place.foods.length > 0" class="foods-section">
          <h3 class="section-title">
            <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            美食清单
          </h3>
          
          <div class="foods-grid">
            <div
              v-for="(food, index) in place.foods"
              :key="index"
              class="food-card"
            >
              <div class="food-icon">🍽️</div>
              <div class="food-info">
                <h4 class="food-name">{{ food.name }}</h4>
                <p v-if="food.description" class="food-desc">{{ food.description }}</p>
                <div v-if="food.tags && food.tags.length > 0" class="food-tags">
                  <span
                    v-for="(tag, idx) in food.tags"
                    :key="idx"
                    class="food-tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 附加信息 -->
        <div class="meta-section">
          <div class="meta-item">
            <span class="meta-label">添加时间</span>
            <span class="meta-value">{{ formatDate(place.addedDate) }}</span>
          </div>
          <div v-if="place.location" class="meta-item">
            <span class="meta-label">坐标</span>
            <span class="meta-value">{{ place.location.lng.toFixed(6) }}, {{ place.location.lat.toFixed(6) }}</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="actions">
          <a
            v-if="place.videoUrl"
            :href="place.videoUrl"
            target="_blank"
            class="action-btn action-btn-primary"
          >
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            查看原视频
          </a>
          
          <a
            v-if="place.location"
            :href="`https://uri.amap.com/marker?position=${place.location.lng},${place.location.lat}&name=${place.name}`"
            target="_blank"
            class="action-btn action-btn-secondary"
          >
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            导航前往
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  place: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.detail-modal {
  position: relative;
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  background: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  transform: scale(1.1);
}

.detail-content {
  overflow-y: auto;
  max-height: 90vh;
}

.detail-cover {
  width: 100%;
  height: 240px;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.detail-location {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  color: #ef4444;
  font-weight: 600;
  margin-bottom: 8px;
}

.location-icon {
  width: 18px;
  height: 18px;
}

.detail-address {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.foods-section {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
}

.title-icon {
  width: 20px;
  height: 20px;
  color: #ef4444;
}

.foods-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.food-card {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  transition: all 0.2s;
}

.food-card:hover {
  background: #fef2f2;
  transform: translateX(4px);
}

.food-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.food-info {
  flex: 1;
}

.food-name {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 6px;
}

.food-desc {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 8px;
}

.food-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.food-tag {
  display: inline-block;
  padding: 4px 10px;
  background: white;
  color: #ef4444;
  font-size: 12px;
  border-radius: 6px;
  font-weight: 500;
  border: 1px solid #fee2e2;
}

.meta-section {
  padding: 24px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.meta-label {
  font-size: 14px;
  color: #6b7280;
}

.meta-value {
  font-size: 14px;
  color: #1f2937;
  font-weight: 500;
}

.actions {
  padding: 24px;
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.action-btn-primary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.action-btn-primary:hover {
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
  transform: translateY(-2px);
}

.action-btn-secondary {
  background: white;
  color: #ef4444;
  border: 2px solid #ef4444;
}

.action-btn-secondary:hover {
  background: #fef2f2;
  transform: translateY(-2px);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

@media (max-width: 768px) {
  .detail-modal {
    max-width: 100%;
    border-radius: 16px;
  }

  .detail-title {
    font-size: 24px;
  }

  .actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>

