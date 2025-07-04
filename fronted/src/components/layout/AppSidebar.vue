<template>
  <div class="app-sidebar" :class="{ collapsed, mobile: isMobile }">
    <!-- Mobile Header with Close Button -->
    <div v-if="isMobile" class="mobile-header">
      <div class="mobile-logo">
        <img src="/logo.ico" alt="Nexaura" class="mobile-logo-icon" />
        <span class="mobile-logo-text">Nexaura</span>
          </div>
      <button class="mobile-close-btn" @click="emit('close')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
        </div>
    
    <!-- 主导航 -->
    <div class="nav-section">
      <div class="nav-category">
        <h3 v-if="!collapsed" class="category-title">
          MAIN
        </h3>
        
        <div class="nav-items" ref="navItemsRef">
          <!-- 动态滑动指示器 -->
          <div 
            class="active-indicator" 
            :style="indicatorStyle"
            v-show="!collapsed && activeIndex !== -1"
          ></div>
          
          <div 
            ref="dashboardRef"
            class="nav-item" 
            :class="{ active: selectedKeys.includes('dashboard') }"
            @click="handleMenuClick({ key: 'dashboard' })"
          >
            <div class="item-icon">
              <div class="icon-bg dashboard">
                <el-icon><Histogram /></el-icon>
              </div>
            </div>
            <div v-if="!collapsed" class="item-content">
              <span class="item-title">{{ t('nav.dashboard') }}</span>
            </div>
            <div class="item-glow"></div>
            <div class="item-ripple"></div>
          </div>
          
          
          <div 
            ref="workflowRef"
            class="nav-item" 
            :class="{ active: selectedKeys.includes('workflow-records') }"
            @click="handleMenuClick({ key: 'workflow-records' })"
          >
            <div class="item-icon">
              <div class="icon-bg workflow">
                <el-icon><List /></el-icon>
              </div>
            </div>
            <div v-if="!collapsed" class="item-content">
              <span class="item-title">{{ t('nav.workflow') }}</span>
            </div>
            <div class="item-glow"></div>
            <div class="item-ripple"></div>
          </div>
          
          <div 
            ref="articlesRef"
            class="nav-item" 
            :class="{ active: selectedKeys.includes('articles') }"
            @click="handleMenuClick({ key: 'articles' })"
          >
            <div class="item-icon">
              <div class="icon-bg articles">
                <el-icon><Document /></el-icon>
              </div>
            </div>
            <div v-if="!collapsed" class="item-content">
              <span class="item-title">{{ t('nav.articles') }}</span>
            </div>
            <div class="item-glow"></div>
            <div class="item-ripple"></div>
          </div>
        </div>
      </div>
      

    </div>
    
    <!-- 桌面端用户信息 & 额度显示 -->
    <div v-if="!collapsed && !isMobile" class="user-section">
      <div class="quota-card">
        <div class="quota-header">
          <span class="quota-title">{{ t('nav.quota_title') }}</span>
        </div>
        
        <div class="quota-progress">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: quotaPercentage + '%' }"
            ></div>
          </div>
          <div class="quota-stats">
            <span class="used">{{ userStore.user?.used_quota || 0 }}</span>
            <span class="separator">/</span>
            <span class="total">{{ userStore.user?.total_quota || 100 }}</span>
          </div>
        </div>
        
        <div class="quota-status">
          <span class="status-text">
            {{ t('nav.quota_remaining', { 
              remaining: (userStore.user?.total_quota || 100) - (userStore.user?.used_quota || 0) 
            }) }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- 移动端用户信息 -->
    <div v-if="isMobile" class="mobile-user-section">
      <div class="mobile-user-info">
        <div class="user-avatar">
          <div class="avatar-placeholder">
            {{ (userStore.user?.name || userStore.user?.email || 'U').charAt(0).toUpperCase() }}
          </div>
        </div>
        <div class="user-details">
          <div class="user-name">{{ userStore.user?.name || userStore.user?.email || 'User' }}</div>
          <div class="user-quota">
            {{ userStore.user?.used_quota || 0 }}/{{ userStore.user?.total_quota || 100 }} {{ t('nav.quota_title') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  Histogram,
  List,
  Document
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/modules/user'

interface Props {
  collapsed: boolean
  isMobile?: boolean
}

interface Emits {
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()

// Refs for nav items and container
const navItemsRef = ref<HTMLElement>()
const dashboardRef = ref<HTMLElement>()
const workflowRef = ref<HTMLElement>()
const articlesRef = ref<HTMLElement>()

const theme = 'light'

const selectedKeys = computed(() => {
  const path = route.path
  if (path.includes('/dashboard')) return ['dashboard']
  if (path.includes('/workflow')) return ['workflow-records']
  if (path.includes('/articles')) return ['articles']
  return ['dashboard']
})

// 活动项索引
const activeIndex = computed(() => {
  if (selectedKeys.value.includes('dashboard')) return 0
  if (selectedKeys.value.includes('workflow-records')) return 1
  if (selectedKeys.value.includes('articles')) return 2
  return -1
})

// 动态指示器样式
const indicatorStyle = ref({
  transform: 'translateY(0px)',
  height: '48px',
  opacity: '0'
})

// 更新指示器位置
const updateIndicatorPosition = async () => {
  await nextTick()
  
  if (props.collapsed || !navItemsRef.value) {
    indicatorStyle.value.opacity = '0'
    return
  }

  const refs = [dashboardRef.value, workflowRef.value, articlesRef.value]
  const activeElement = refs[activeIndex.value]
  
  if (activeElement) {
    const containerRect = navItemsRef.value.getBoundingClientRect()
    const activeRect = activeElement.getBoundingClientRect()
    const offsetTop = activeRect.top - containerRect.top
    
    indicatorStyle.value = {
      transform: `translateY(${offsetTop}px)`,
      height: `${activeRect.height}px`,
      opacity: '1'
    }
  } else {
    indicatorStyle.value.opacity = '0'
  }
}

const quotaPercentage = computed(() => {
  const used = userStore.user?.used_quota || 0
  const total = userStore.user?.total_quota || 100
  return Math.round((used / total) * 100)
})

const handleMenuClick = ({ key }: { key: string }) => {
  const routeMap: Record<string, string> = {
    dashboard: '/app/dashboard',
    'workflow-records': '/app/workflow/records',
    articles: '/app/articles'
  }
  
  const path = routeMap[key]
  if (path) {
    router.push(path)
    // 在移动端点击导航项后自动关闭侧边栏
    if (props.isMobile) {
      emit('close')
    }
  }
}

// 监听路由变化和折叠状态变化
watch(() => route.path, updateIndicatorPosition, { immediate: true })
watch(() => props.collapsed, updateIndicatorPosition)
watch(activeIndex, updateIndicatorPosition)

onMounted(() => {
  updateIndicatorPosition()
})
</script>

<style scoped>
.app-sidebar {
  height: 100vh;
  width: 240px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: 1px solid #e0e0e0;
}

.app-sidebar.collapsed {
  width: 80px;
}



/* Logo区域 */
.logo-section {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
}

.logo-link:hover {
  transform: translateY(-2px);
}

.logo-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
}

.icon-wrapper {
  font-size: 24px;
  z-index: 1;
}


.logo-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-text {
  font-size: 20px;
  font-weight: 800;
  background: linear-gradient(45deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.logo-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 导航区域 */
.nav-section {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
  position: relative;
  z-index: 1;
  min-height: 0; /* 允许flex子项收缩 */
  max-height: calc(100vh - 260px); /* 进一步缩短导航区域高度 */
}

.nav-category {
  margin-bottom: 32px;
}

.category-title {
  margin: 0 0 16px 20px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.5);
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
}


.nav-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
  position: relative;
}

/* 动态滑动指示器 */
.active-indicator {
  position: absolute;
  left: 8px;
  right: 8px;
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.15) 0%, 
    rgba(118, 75, 162, 0.15) 100%
  );
  border: 1px solid rgba(102, 126, 234, 0.25);
  border-radius: 12px;
  transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
  z-index: 0;
  box-shadow: 
    0 4px 12px rgba(102, 126, 234, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.active-indicator::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.08) 0%, 
    rgba(118, 75, 162, 0.08) 100%
  );
  border-radius: 12px;
  animation: gentle-pulse 3s ease-in-out infinite;
}

@keyframes gentle-pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
  background: transparent;
  margin-bottom: 2px;
  overflow: hidden;
  min-height: 48px;
  z-index: 1;
  border: 1px solid transparent;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover::before {
  opacity: 1;
}


.nav-item.active {
  background: transparent;
  border: 1px solid transparent;
}

.nav-item.active::before {
  opacity: 0;
}

.nav-item.featured {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 154, 0, 0.15));
  border: 1px solid rgba(255, 107, 107, 0.2);
  position: relative;
}

.featured-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: linear-gradient(45deg, #ff6b6b, #ff9a00);
  color: white;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
}

.icon-bg {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.icon-bg.dashboard {
  background: #f0f4ff;
  color: #4c63d2;
}

.icon-bg.workflow {
  background: #f0f4ff;
  color: #4c63d2;
}

.icon-bg.articles {
  background: #f0fdf4;
  color: #059669;
}

.nav-item:hover .icon-bg {
  transform: scale(1.08) rotate(1deg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-item.active .icon-bg {
  transform: scale(1.02);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.item-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.nav-item.active .item-title {
  color: rgba(0, 0, 0, 0.95);
  font-weight: 600;
}

.item-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(102, 126, 234, 0.05), transparent);
  opacity: 0;
  transition: opacity 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
  pointer-events: none;
  border-radius: 12px;
}

.nav-item:hover .item-glow {
  opacity: 1;
}

/* 点击涟漪效果 */
.item-ripple {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.nav-item:active .item-ripple::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ripple-animation 0.6s ease-out;
}

@keyframes ripple-animation {
  0% {
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}

/* 悬浮时的微妙放大效果 */
.nav-item:hover {
  transform: translateX(2px);
  background: rgba(102, 126, 234, 0.03);
}

.nav-item.active:hover {
  transform: translateX(2px);
  background: transparent;
}


/* 用户额度区域 */
.user-section {
  padding: 16px 20px 24px;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
  min-height: 160px; /* 确保额度卡片有最小高度 */
}

.quota-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
  position: relative;
  overflow: hidden;
  min-height: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}


.quota-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}

.quota-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.8);
}

.upgrade-btn {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.upgrade-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.quota-progress {
  margin-bottom: 12px;
  position: relative;
  z-index: 1;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}


.quota-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
}

.used {
  color: #8b5cf6;
}

.separator {
  color: rgba(0, 0, 0, 0.5);
}

.total {
  color: rgba(0, 0, 0, 0.7);
}

.quota-status {
  text-align: center;
  position: relative;
  z-index: 1;
}

.status-text {
  font-size: 11px;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
}



/* Mobile Header */
.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
}

.mobile-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mobile-logo-icon {
  width: 32px;
  height: 32px;
}

.mobile-logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.mobile-close-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
}

.mobile-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

/* Mobile Sidebar Styles */
.app-sidebar.mobile {
  width: 280px;
  height: 100vh;
  background: white;
  border-right: none;
  box-shadow: none;
}

.app-sidebar.mobile .nav-section {
  padding: 16px 0;
  max-height: calc(100vh - 140px);
}

.app-sidebar.mobile .nav-item {
  padding: 12px 20px;
  margin: 0 16px 4px 16px;
}

.app-sidebar.mobile .category-title {
  margin: 0 0 12px 20px;
  font-size: 12px;
}

/* 桌面端收起状态优化 */
.app-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 8px;
  margin: 0 8px 4px 8px;
}

.app-sidebar.collapsed .category-title {
  display: none;
}

.app-sidebar.collapsed .featured-badge {
  top: 8px;
  right: 8px;
  font-size: 8px;
  padding: 1px 4px;
}

.app-sidebar.collapsed .active-indicator {
  left: 4px;
  right: 4px;
}

/* 移动端不显示指示器 */
.app-sidebar.mobile .active-indicator {
  display: none;
}

/* Mobile User Section */
.mobile-user-section {
  padding: 16px 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.02);
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  }
  
.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-quota {
  font-size: 12px;
  color: #666;
}

/* 滚动条样式 */
.nav-section::-webkit-scrollbar {
  width: 4px;
}

.nav-section::-webkit-scrollbar-track {
  background: transparent;
}

.nav-section::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.nav-section::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>