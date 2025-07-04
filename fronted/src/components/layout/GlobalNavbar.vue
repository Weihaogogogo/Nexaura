<template>
  <header class="global-navbar fade-in">
    <div class="container">
      <div class="navbar-content">
        <!-- Logo -->
        <div class="logo-section slide-right">
          <router-link to="/" class="logo-link">
            <img src="/logo.ico" alt="Nexaura" class="logo-icon" />
            <span class="logo-text">Nexaura</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="desktop-nav fade-in animate-delay-200">
          <template v-if="isAuthenticated">
            <router-link to="/app/dashboard" class="nav-link" :class="{ 'router-link-active': isAppRoute }">{{ t('nav.dashboard') }}</router-link>
          </template>
          <router-link to="/pricing" class="nav-link">{{ t('nav.pricing') }}</router-link>
          <router-link to="/help" class="nav-link">{{ t('nav.help') }}</router-link>
          <router-link to="/about" class="nav-link">{{ t('nav.about') }}</router-link>
        </nav>

        <!-- Action Buttons -->
        <div class="navbar-actions slide-left animate-delay-300">
          <!-- Language Selector -->
          <LanguageSelector />
          
          <template v-if="!isAuthenticated">
            <router-link to="/login" class="login-btn hover-lift">{{ t('nav.login') }}</router-link>
            <router-link to="/register" class="signup-btn hover-lift">{{ t('nav.register') }}</router-link>
          </template>
          <template v-else>
            <!-- User Menu -->
            <div class="user-menu">
              <a-dropdown trigger="click">
                <div class="user-avatar">
                  <UserOutlined />
                  <span class="user-name">{{ userName }}</span>
                  <DownOutlined class="dropdown-icon" />
                </div>
                <template #overlay>
                  <a-menu>
                    <a-menu-item>
                      <router-link to="/app/profile" class="menu-link">
                        <UserOutlined />
                        {{ t('nav.profile') }}
                      </router-link>
                    </a-menu-item>
                    <a-menu-divider />
                    <a-menu-item @click="handleLogout">
                      <div class="menu-link logout-link">
                        <LogoutOutlined />
                        {{ t('nav.logout') }}
                      </div>
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </div>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { UserOutlined, DownOutlined, LogoutOutlined } from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/modules/user'
import LanguageSelector from '@/components/common/LanguageSelector.vue'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const userStore = useUserStore()

// Computed properties
const isAuthenticated = computed(() => userStore.isAuthenticated)
const userName = computed(() => userStore.user?.name || userStore.user?.email?.split('@')[0] || 'User')
const isAppRoute = computed(() => route.path.startsWith('/app'))

// Methods
const handleLogout = async () => {
  try {
    await userStore.logout()
    message.success('Logged out successfully')
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    message.error('Logout failed')
  }
}
</script>

<style scoped>
.global-navbar {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
  border-bottom: 1px solid #e0e0e0;
  /* box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1); */
}

.global-navbar:hover {
  background: rgba(255, 255, 255, 0.95);
  border-bottom-color: rgba(99, 102, 241, 0.3);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: #16191d;
  transition: all 0.3s ease;
}

.logo-link:hover {
  transform: scale(1.05);
}

.logo-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #16191d;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 4s ease infinite;
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: #16191d;
  text-decoration: none;
  font-weight: 500;
  position: relative;
  transition: all 0.3s ease;
  padding: 0.5rem 0;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: #6366f1;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
  width: 100%;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.login-btn {
  color: #16191d;
  font-weight: 500;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.signup-btn {
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.9) 0%,
    rgba(139, 92, 246, 0.9) 50%,
    rgba(236, 72, 153, 0.9) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  font-weight: 500;
  height: 40px;
  padding: 0 1.5rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.signup-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.signup-btn:hover::before {
  left: 100%;
}

.signup-btn:hover {
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 1) 0%,
    rgba(139, 92, 246, 1) 50%,
    rgba(236, 72, 153, 1) 100%
  );
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
}

.signup-btn:active {
  transform: translateY(0);
}

.user-menu {
  display: flex;
  align-items: center;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: transparent;
  border: none;
}

.user-avatar:hover {
  background: rgba(0, 0, 0, 0.05);
}

.user-name {
  font-weight: 500;
  color: #16191d;
}

.dropdown-icon {
  font-size: 12px;
  color: #6b7280;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #16191d;
  text-decoration: none;
  width: 100%;
}

.logout-link {
  color: #ef4444;
  cursor: pointer;
}

.fade-in {
  opacity: 0;
  animation: fadeInAnimation 1s ease-out forwards;
}

.slide-right {
  opacity: 0;
  transform: translateX(50px);
  animation: slideRightAnimation 1s ease-out forwards;
}

.slide-left {
  opacity: 0;
  transform: translateX(-50px);
  animation: slideLeftAnimation 1s ease-out forwards;
}

.animate-delay-200 {
  animation-delay: 200ms;
}

.animate-delay-300 {
  animation-delay: 300ms;
}

.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
}

@keyframes fadeInAnimation {
  to {
    opacity: 1;
  }
}

@keyframes slideRightAnimation {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideLeftAnimation {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .navbar-actions {
    gap: 0.5rem;
  }

  .signup-btn {
    padding: 0 1rem;
    font-size: 0.875rem;
  }

  .user-name {
    display: none;
  }
}
</style>