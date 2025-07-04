<template>
  <div class="relative w-full min-h-screen bg-black text-white overflow-hidden">
    <!-- Main container with space for content -->
    <div class="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 min-h-screen">
      <!-- Navigation -->
      <div
        v-motion
        :initial="{ y: -20, opacity: 0 }"
        :enter="{ y: 0, opacity: 1 }"
        :delay="0"
        class="px-4 backdrop-blur-3xl bg-black/50 rounded-full py-4 flex justify-between items-center mb-12"
      >
        <div class="flex items-center">
          <div class="text-2xl font-bold">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
              <path d="M20 5L5 20L20 35L35 20L20 5Z" stroke="white" strokeWidth="2" />
            </svg>
          </div>
          <div class="hidden md:flex items-center space-x-6 ml-8">
            <button class="px-4 py-2 bg-gray-800/50 hover:bg-gray-700/50 rounded-full text-sm transition-colors">Start</button>
            <button class="px-4 py-2 text-sm hover:text-gray-300 transition-colors">Home</button>
            <button class="px-4 py-2 text-sm hover:text-gray-300 transition-colors">Contacts</button>
            <button class="px-4 py-2 text-sm hover:text-gray-300 transition-colors">Help</button>
            <button class="px-4 py-2 text-sm hover:text-gray-300 transition-colors">Docs</button>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <button class="hidden md:block px-4 py-2 text-sm hover:text-gray-300 transition-colors">Register</button>
          <button class="px-4 py-2 bg-gray-800/80 backdrop-blur-sm rounded-full text-sm hover:bg-gray-700/80 transition-colors">Application</button>
          <!-- Mobile menu button -->
          <button
            class="md:hidden p-2 rounded-md focus:outline-none"
            @click="toggleMobileMenu"
          >
            <svg v-if="mobileMenuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div
        v-if="mobileMenuOpen"
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1 }"
        :leave="{ opacity: 0 }"
        class="md:hidden fixed inset-0 z-50 bg-black/95 backdrop-blur-lg"
        style="z-index: 9999;"
      >
        <div class="flex flex-col items-center justify-center h-full space-y-6 text-lg">
          <button
            class="absolute top-6 right-6 p-2"
            @click="toggleMobileMenu"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <button class="px-6 py-3 bg-gray-800/50 rounded-full">Start</button>
          <button class="px-6 py-3">Home</button>
          <button class="px-6 py-3">Contacts</button>
          <button class="px-6 py-3">Help</button>
          <button class="px-6 py-3">Docs</button>
          <button class="px-6 py-3">Register</button>
          <button class="px-6 py-3 bg-gray-800/80 backdrop-blur-sm rounded-full">Application</button>
        </div>
      </div>

      <!-- Feature Items -->
      <div class="w-full z-200 top-[30%] relative">
        <FeatureItem
          v-motion
          :initial="{ x: -50, opacity: 0 }"
          :enter="{ x: 0, opacity: 1 }"
          :delay="200"
          name="Vue3"
          value="for base"
          position="left-0 sm:left-10 top-40"
        />
        <FeatureItem
          v-motion
          :initial="{ y: -50, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="500"
          name="Tailwind"
          value="for styles"
          position="left-1/4 top-24"
        />
        <FeatureItem
          v-motion
          :initial="{ y: -50, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="800"
          name="VueUse Motion"
          value="for animations"
          position="right-1/4 top-24"
        />
        <FeatureItem
          v-motion
          :initial="{ x: 50, opacity: 0 }"
          :enter="{ x: 0, opacity: 1 }"
          :delay="1100"
          name="WebGL"
          value="for lightning"
          position="right-0 sm:right-10 top-40"
        />
      </div>

      <!-- Main hero content -->
      <div class="relative z-30 flex flex-col items-center text-center max-w-4xl mx-auto">
        <!-- Hue Slider -->
        <ElasticHueSlider
          v-model="lightningHue"
          label="Adjust Lightning Hue"
          :min="0"
          :max="360"
          :step="1"
        />

        <!-- Button: "Join us for free world" -->
        <button
          v-motion
          :initial="{ y: 20, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="1400"
          class="group flex items-center space-x-2 px-4 py-2 bg-white/5 hover:bg-white/10 backdrop-blur-sm rounded-full text-sm mb-6 transition-all duration-300 hover:scale-105 active:scale-95"
        >
          <span>Join us for free world</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="transform group-hover:translate-x-1 transition-transform duration-300">
            <path d="M8 3L13 8L8 13M13 8H3" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>

        <h1
          v-motion
          :initial="{ y: 20, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="1700"
          class="text-5xl md:text-7xl font-light mb-2"
        >
          Hero Odyssey
        </h1>

        <h2
          v-motion
          :initial="{ y: 20, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="2000"
          class="text-3xl md:text-5xl pb-3 font-light bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 bg-clip-text text-transparent"
        >
          Lighting Up The Future
        </h2>

        <!-- Description -->
        <p
          v-motion
          :initial="{ y: 20, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="2300"
          class="text-gray-400 mb-9 max-w-2xl"
        >
          Lightning animation is 100% code generated, so feel free to customize it to your liking.
        </p>

        <button
          v-motion
          :initial="{ y: 20, opacity: 0 }"
          :enter="{ y: 0, opacity: 1 }"
          :delay="2600"
          class="mt-[100px] sm:mt-[100px] px-8 py-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors hover:scale-105 active:scale-95"
        >
          Discover Those Worlds
        </button>
      </div>
    </div>

    <!-- Background elements -->
    <div
      v-motion
      :initial="{ opacity: 0 }"
      :enter="{ opacity: 1 }"
      :delay="0"
      :duration="1000"
      class="absolute inset-0 z-0"
    >
      <!-- Dark overlay -->
      <div class="absolute inset-0 bg-black/80"></div>

      <!-- Glowing circle -->
      <div class="absolute top-[55%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-gradient-to-b from-blue-500/20 to-purple-600/10 blur-3xl"></div>

      <!-- Central light beam -->
      <div class="absolute top-0 w-[100%] left-1/2 transform -translate-x-1/2 h-full">
        <Lightning
          :hue="lightningHue"
          :x-offset="0"
          :speed="1.6"
          :intensity="0.6"
          :size="2"
        />
      </div>

      <!-- Planet/sphere -->
      <div class="z-10 absolute top-[55%] left-1/2 transform -translate-x-1/2 w-[600px] h-[600px] backdrop-blur-3xl rounded-full bg-[radial-gradient(circle_at_25%_90%,_#1e386b_15%,_#000000de_70%,_#000000ed_100%)]"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import FeatureItem from './FeatureItem.vue'
import ElasticHueSlider from './ElasticHueSlider.vue'
import Lightning from './SimpleLightning.vue'

const mobileMenuOpen = ref(false)
const lightningHue = ref(220)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}
</script>

<style scoped>
/* 自定义样式 */
</style> 