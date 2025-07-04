<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'
import GlobalNavbar from '@/components/layout/GlobalNavbar.vue'

console.log('App.vue loaded')

const route = useRoute()
const userStore = useUserStore()

// Initialize authentication state
onMounted(() => {
  userStore.initializeAuth()
})

// Check if current route should hide navbar
const shouldHideNavbar = () => {
  const hideNavbarRoutes = ['/login', '/register', '/forgot-password']
  return hideNavbarRoutes.includes(route.path)
}
</script>

<template>
  <div id="app">
    <GlobalNavbar v-if="!shouldHideNavbar()" />
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

.ant-layout {
  background: #fff;
}

.ant-layout-content {
  background: #f0f2f5;
}
</style>
