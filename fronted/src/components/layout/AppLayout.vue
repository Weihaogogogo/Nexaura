<template>
  <a-layout class="app-layout">
    <!-- Desktop Sidebar -->
    <a-layout-sider
      v-if="!isMobile"
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      width="240"
      collapsed-width="80"
      class="sidebar desktop-sidebar"
    >
      <AppSidebar :collapsed="collapsed" :is-mobile="false" />
    </a-layout-sider>
    
    <!-- Mobile Sidebar Overlay -->
    <div v-if="isMobile && sidebarVisible" class="mobile-sidebar-overlay" @click="closeMobileSidebar">
      <div class="mobile-sidebar" @click.stop>
        <AppSidebar :collapsed="false" :is-mobile="true" @close="closeMobileSidebar" />
      </div>
    </div>
    
    <!-- Mobile Menu Button -->
    <button 
      v-if="isMobile" 
      ref="mobileMenuBtnRef"
      class="mobile-menu-btn"
      :class="{ 'is-right': isMenuOnRight }"
      :style="menuButtonStyle"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
      @mousedown="handleMouseDown"
    >
      <!-- 边缘指示器 -->
      <div v-if="isDragging" class="edge-indicator" :class="{ 'right': isMenuOnRight }"></div>
      
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    
    <!-- Desktop Sidebar Toggle Button -->
    <button 
      v-if="!isMobile" 
      class="desktop-toggle-btn"
      :style="{ left: collapsed ? '100px' : '260px' }"
      @click="collapsed = !collapsed"
    >
      <svg v-if="collapsed" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="m9 18 6-6-6-6"/>
      </svg>
      <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="m15 18-6-6 6-6"/>
      </svg>
    </button>
    
    <a-layout class="main-layout" :class="{ collapsed }">
      <!-- Removed AppHeader since we now have GlobalNavbar -->
      <a-layout-content class="content" :class="{ 'no-footer': shouldHideFooter }">
        <div class="content-wrapper">
          <router-view />
          
          <!-- HomeFooter - show for article pages, workflow records, and dashboard -->
          <HomeFooter v-if="shouldShowHomeFooter" />
        </div>
      </a-layout-content>
      
      <a-layout-footer v-if="!shouldHideFooter" class="footer">
        <AppFooter />
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from './AppSidebar.vue'
import AppFooter from './AppFooter.vue'
import HomeFooter from './HomeFooter.vue'

const collapsed = ref(false)
const route = useRoute()
const isMobile = ref(false)
const sidebarVisible = ref(false)

// 拖动相关状态
const mobileMenuBtnRef = ref<HTMLElement>()
const isDragging = ref(false)
const isMenuOnRight = ref(false)
const menuPosition = ref({ x: 20, y: 20 })

// 计算菜单按钮样式
const menuButtonStyle = computed(() => ({
  left: isMenuOnRight.value ? 'auto' : `${menuPosition.value.x}px`,
  right: isMenuOnRight.value ? `${menuPosition.value.x}px` : 'auto',
  top: `${menuPosition.value.y}px`,
  transform: isDragging.value ? 'scale(1.1)' : 'scale(1)',
}))

// 拖动状态
let dragStart = { x: 0, y: 0 }
let buttonStart = { x: 0, y: 0 }
let dragDistance = 0
const DRAG_THRESHOLD = 5 // 超过5px才算拖动

// 检测移动端
const checkIsMobile = () => {
  const mobile = window.innerWidth <= 768
  if (mobile !== isMobile.value) {
    isMobile.value = mobile
    // 当切换到桌面端时，关闭移动端侧边栏
    if (!mobile) {
      sidebarVisible.value = false
    }
    // 重置菜单按钮位置
    if (mobile) {
      resetMenuButtonPosition()
    }
  }
}

// 重置菜单按钮位置
const resetMenuButtonPosition = () => {
  menuPosition.value = { x: 20, y: 20 }
  isMenuOnRight.value = false
}

// 吸附到边缘
const snapToEdge = () => {
  const windowWidth = window.innerWidth
  const buttonWidth = 48 // 按钮宽度
  const centerX = windowWidth / 2
  const currentX = isMenuOnRight.value 
    ? windowWidth - menuPosition.value.x - buttonWidth 
    : menuPosition.value.x

  // 判断应该吸附到哪一边
  const shouldBeOnRight = currentX > centerX

  // 吸附到边缘，保持20px的边距
  const edgeMargin = 20
  
  // 确保Y坐标在有效范围内
  const windowHeight = window.innerHeight
  const buttonHeight = 48
  const minY = 20
  const maxY = windowHeight - buttonHeight - 20
  const clampedY = Math.max(minY, Math.min(maxY, menuPosition.value.y))

  // 使用动画吸附到边缘
  const targetX = edgeMargin
  const targetY = clampedY

  // 更新状态
  isMenuOnRight.value = shouldBeOnRight
  menuPosition.value = { x: targetX, y: targetY }

  // 添加吸附动画类
  if (mobileMenuBtnRef.value) {
    mobileMenuBtnRef.value.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
    
    // 延迟移除动画类，确保动画完成
    setTimeout(() => {
      if (mobileMenuBtnRef.value) {
        mobileMenuBtnRef.value.style.transition = ''
      }
    }, 400)
  }
}

// 移动端侧边栏控制
const toggleMobileSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value
}

const closeMobileSidebar = () => {
  sidebarVisible.value = false
}

// 监听窗口大小变化
const handleResize = () => {
  checkIsMobile()
}

// 触摸事件处理
const handleTouchStart = (e: TouchEvent) => {
  e.preventDefault()
  e.stopPropagation()
  const touch = e.touches[0]
  startDrag(touch.clientX, touch.clientY)
}

const handleTouchMove = (e: TouchEvent) => {
  e.preventDefault()
  e.stopPropagation()
  const touch = e.touches[0]
  updateDrag(touch.clientX, touch.clientY)
}

const handleTouchEnd = (e: TouchEvent) => {
  e.preventDefault()
  e.stopPropagation()
  
  // 如果是短距离移动，当作点击处理
  if (dragDistance < DRAG_THRESHOLD) {
    sidebarVisible.value = !sidebarVisible.value
  }
  
  endDrag()
}

// 鼠标事件处理
const handleMouseDown = (e: MouseEvent) => {
  e.preventDefault()
  startDrag(e.clientX, e.clientY)
  
  // 添加全局鼠标事件监听
  document.addEventListener('mousemove', handleDocumentMouseMove)
  document.addEventListener('mouseup', handleDocumentMouseUp)
}



const handleDocumentMouseMove = (e: MouseEvent) => {
  if (!isDragging.value) return
  e.preventDefault()
  updateDrag(e.clientX, e.clientY)
}

const handleDocumentMouseUp = (e: MouseEvent) => {
  e.preventDefault()
  
  // 如果是短距离移动，当作点击处理
  if (dragDistance < DRAG_THRESHOLD) {
    sidebarVisible.value = !sidebarVisible.value
  }
  
  endDrag()
  
  // 移除全局事件监听
  document.removeEventListener('mousemove', handleDocumentMouseMove)
  document.removeEventListener('mouseup', handleDocumentMouseUp)
}

// 开始拖动
const startDrag = (clientX: number, clientY: number) => {
  dragStart = { x: clientX, y: clientY }
  dragDistance = 0
  
  // 记录按钮当前位置
  const currentX = isMenuOnRight.value 
    ? window.innerWidth - menuPosition.value.x - 48
    : menuPosition.value.x
    
  buttonStart = { x: currentX, y: menuPosition.value.y }
}

// 更新拖动位置
const updateDrag = (clientX: number, clientY: number) => {
  const deltaX = clientX - dragStart.x
  const deltaY = clientY - dragStart.y
  
  // 计算拖动距离
  dragDistance = Math.sqrt(deltaX * deltaX + deltaY * deltaY)
  
  // 只有超过阈值才开始拖动
  if (dragDistance < DRAG_THRESHOLD) return
  
  // 如果还没进入拖动状态，现在进入
  if (!isDragging.value) {
    isDragging.value = true
  }
  
  const newX = buttonStart.x + deltaX
  const newY = buttonStart.y + deltaY
  
  // 边界检查
  const windowWidth = window.innerWidth
  const windowHeight = window.innerHeight
  const buttonWidth = 48
  const buttonHeight = 48
  
  const clampedX = Math.max(0, Math.min(windowWidth - buttonWidth, newX))
  const clampedY = Math.max(0, Math.min(windowHeight - buttonHeight, newY))
  
  // 判断当前在左边还是右边
  const centerX = windowWidth / 2
  const shouldBeOnRight = clampedX > centerX
  
  // 更新位置
  if (shouldBeOnRight) {
    menuPosition.value.x = windowWidth - clampedX - buttonWidth
    isMenuOnRight.value = true
  } else {
    menuPosition.value.x = clampedX
    isMenuOnRight.value = false
  }
  
  menuPosition.value.y = clampedY
}

// 结束拖动
const endDrag = () => {
  if (isDragging.value) {
    isDragging.value = false
    snapToEdge()
  }
  // 重置拖动距离，准备下次交互
  dragDistance = 0
}

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  // 清理可能的全局事件监听
  document.removeEventListener('mousemove', handleDocumentMouseMove)
  document.removeEventListener('mouseup', handleDocumentMouseUp)
})

// 判断是否为工作流页面
const isWorkflowPage = computed(() => {
  return route.path.includes('/workflow/')
})

// 判断是否为文章详情页
const isArticleDetailPage = computed(() => {
  return route.path.includes('/articles/') && route.params.id
})

// 判断是否为文章库页面
const isArticleListPage = computed(() => {
  return route.path === '/app/articles'
})

// 判断是否为工作流记录页面
const isWorkflowRecordsPage = computed(() => {
  return route.path === '/app/workflow/records'
})

// 判断是否为dashboard页面
const isDashboardPage = computed(() => {
  return route.path === '/app/dashboard'
})

// 判断是否应该隐藏AppFooter
const shouldHideFooter = computed(() => {
  return isWorkflowPage.value || isArticleDetailPage.value || isArticleListPage.value || isWorkflowRecordsPage.value || isDashboardPage.value
})

// 判断是否应该显示HomeFooter
const shouldShowHomeFooter = computed(() => {
  return isArticleDetailPage.value || isArticleListPage.value || isWorkflowRecordsPage.value || isDashboardPage.value
})
</script>

<style scoped>
.app-layout {
  min-height: calc(100vh - 64px); /* Account for global navbar height */
  padding-top: 0px; /* Add padding for global navbar */
}

.sidebar {
  position: fixed;
  left: 0;
  top: 64px; /* Position below global navbar */
  bottom: 0;
  z-index: 100;
  background: transparent; /* 确保背景透明，避免黑边 */
}

.main-layout {
  margin-left: 240px !important;
  transition: margin-left 0.2s;
}

.main-layout.collapsed {
  margin-left: 80px !important;
}

.content {
  background-color: #f0f2f5;
  min-height: calc(100vh - 64px - 70px); /* Account for navbar and footer */
}

.content.no-footer {
  min-height: calc(100vh - 64px); /* Only account for navbar when no footer */
}

.content-wrapper {
  margin: 0;
  background: linear-gradient(135deg, 
    rgba(99, 102, 241, 0.03) 0%, 
    rgba(139, 92, 246, 0.05) 25%,
    rgba(236, 72, 153, 0.03) 50%,
    rgba(6, 182, 212, 0.04) 75%,
    rgba(244, 114, 182, 0.02) 100%
  );
  border-radius: 0;
  min-height: calc(100vh - 64px - 70px); /* Account for navbar and footer */
}

.no-footer .content-wrapper {
  min-height: calc(100vh - 64px); /* Only account for navbar when no footer */
}

.footer {
  background: #fff;
  text-align: center;
  border-top: 1px solid #f0f0f0;
  padding: 24px 50px;
}

/* Mobile Menu Button */
.mobile-menu-btn {
    position: fixed;
  z-index: 1001;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #333;
  user-select: none;
  touch-action: manipulation;
}

.mobile-menu-btn:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.mobile-menu-btn:active {
  cursor: grabbing;
}

/* 拖动状态 */
.mobile-menu-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 在拖动时禁用过渡效果，使拖动更流畅 */
.mobile-menu-btn[style*="scale(1.1)"] {
  transition: none !important;
  cursor: grabbing;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
  background: rgba(255, 255, 255, 1);
}

/* 右侧位置的样式调整 */
.mobile-menu-btn.is-right {
  /* 可以添加特定的右侧样式 */
}

/* 边缘指示器 */
.edge-indicator {
  position: absolute;
  width: 3px;
  height: 20px;
  background: linear-gradient(to bottom, #667eea, #764ba2);
  border-radius: 2px;
  left: 6px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.8;
  animation: pulse 1s infinite;
}

.edge-indicator.right {
  left: auto;
  right: 6px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.8;
    transform: translateY(-50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translateY(-50%) scale(1.1);
  }
}

/* Desktop Toggle Button */
.desktop-toggle-btn {
  position: fixed;
  top: 20px;
  z-index: 101;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
}

.desktop-toggle-btn:hover {
  background: rgba(255, 255, 255, 1);
  color: #333;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Mobile Sidebar Overlay */
.mobile-sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

.mobile-sidebar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 280px;
  background: white;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  animation: slideInLeft 0.3s ease;
  overflow-y: auto;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInLeft {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

@media (max-width: 768px) {
  .main-layout {
    margin-left: 0 !important;
  }
  
  .content-wrapper {
    margin: 0;
  }
}

/* Desktop Sidebar Styles */
.desktop-sidebar {
  background: transparent !important;
}

:deep(.ant-layout-sider-children) {
  background: transparent !important;
}
</style>