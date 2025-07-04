import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { MotionPlugin } from '@vueuse/motion'

import 'flag-icons/css/flag-icons.min.css'
import './style.css'
import App from './App.vue'
import router from './router'
import { i18n } from './plugins/i18n'
import { useUserStore } from './stores/modules/user'



const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(Antd)
app.use(ElementPlus, {
  locale: zhCn,
})
app.use(MotionPlugin)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 初始化用户认证状态和令牌刷新服务
const initAuth = async () => {
  const userStore = useUserStore()
  await userStore.initializeAuth()
  
  // 如果用户已登录，启动令牌刷新服务
  if (userStore.isAuthenticated) {
    const { tokenRefreshService } = await import('./services/tokenRefresh')
  }
}

// Add error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue error:', err)
  console.error('Component:', vm)
  console.error('Info:', info)
}

try {
  app.mount('#app')
  // 在应用挂载后初始化认证
  initAuth()
} catch (error) {
  console.error('Failed to mount Vue app:', error)
}
