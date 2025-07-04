<template>
  <div class="app-header">
    <div class="header-left">
      <a-button
        type="text"
        class="trigger"
        @click="$emit('toggle')"
      >
        <MenuUnfoldOutlined v-if="collapsed" />
        <MenuFoldOutlined v-else />
      </a-button>
      
      <div class="breadcrumb">
        <a-breadcrumb>
          <a-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
            <router-link v-if="item.path" :to="item.path">
              {{ item.title }}
            </router-link>
            <span v-else>{{ item.title }}</span>
          </a-breadcrumb-item>
        </a-breadcrumb>
      </div>
    </div>
    
    <div class="header-right">
      <!-- Language Selector -->
      <LanguageSelector :in-header="true" />
      
      <!-- Notifications -->
      <a-dropdown placement="bottomRight">
        <a-badge :count="notifications.length" :offset="[10, 0]">
          <a-button type="text" class="action-btn">
            <BellOutlined />
          </a-button>
        </a-badge>
        <template #overlay>
          <div class="notification-dropdown">
            <div class="notification-header">
              <span>{{ $t('nav.notifications') }}</span>
              <a-button type="link" size="small" @click="clearNotifications">
                {{ $t('common.clear_all') }}
              </a-button>
            </div>
            <a-menu v-if="notifications.length > 0">
              <a-menu-item v-for="notification in notifications" :key="notification.id">
                <div class="notification-item">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-time">{{ notification.time }}</div>
                </div>
              </a-menu-item>
            </a-menu>
            <div v-else class="no-notifications">
              {{ $t('nav.no_notifications') }}
            </div>
          </div>
        </template>
      </a-dropdown>
      
      <!-- User Menu -->
      <a-dropdown placement="bottomRight">
        <a-button type="text" class="user-btn">
          <a-avatar :src="userStore.user?.avatar" :size="32">
            <template #icon>
              <UserOutlined />
            </template>
          </a-avatar>
          <span class="user-name">{{ userStore.user?.name || userStore.user?.email }}</span>
          <DownOutlined />
        </a-button>
        <template #overlay>
          <a-menu @click="handleUserMenuClick">
            <a-menu-item key="profile">
              <UserOutlined />
              {{ $t('nav.profile') }}
            </a-menu-item>
            <a-menu-item key="settings">
              <SettingOutlined />
              {{ $t('nav.settings') }}
            </a-menu-item>
            <a-menu-divider />
            <a-menu-item key="logout">
              <LogoutOutlined />
              {{ $t('nav.logout') }}
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  UserOutlined,
  DownOutlined,
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/modules/user'
import LanguageSelector from '@/components/common/LanguageSelector.vue'

interface Props {
  collapsed: boolean
}

defineProps<Props>()
defineEmits<{
  toggle: []
}>()

const route = useRoute()
const router = useRouter()
const { locale, t } = useI18n()
const userStore = useUserStore()

const notifications = ref([
  {
    id: 1,
    title: 'Article generation completed',
    time: '5 minutes ago'
  }
])

const currentLocale = computed(() => locale.value)

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  const breadcrumbItems = matched.map(item => ({
    path: item.path,
    title: t(item.meta.title as string)
  }))
  
  // Add current page if it has a title
  if (route.meta.title) {
    breadcrumbItems.push({
      path: '',
      title: t(route.meta.title as string)
    })
  }
  
  return breadcrumbItems
})

const handleUserMenuClick = ({ key }: { key: string }) => {
  switch (key) {
    case 'profile':
      router.push({ name: 'Profile' })
      break
    case 'settings':
      router.push({ name: 'Settings' })
      break
    case 'logout':
      userStore.logout()
      router.push({ name: 'Home' })
      break
  }
}

const clearNotifications = () => {
  notifications.value = []
}
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trigger {
  font-size: 18px;
  line-height: 64px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #1890ff;
}

.breadcrumb {
  margin-left: 16px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 12px;
  border-radius: 6px;
}

.action-text {
  font-size: 14px;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 12px;
  border-radius: 6px;
}

.user-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-dropdown {
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-weight: 600;
}

.notification-item {
  padding: 8px 0;
}

.notification-title {
  font-size: 14px;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 12px;
  color: #8c8c8c;
}

.no-notifications {
  padding: 24px;
  text-align: center;
  color: #8c8c8c;
}



@media (max-width: 768px) {
  .action-text {
    display: none;
  }
  
  .user-name {
    display: none;
  }
  
  .breadcrumb {
    display: none;
  }
}
</style>