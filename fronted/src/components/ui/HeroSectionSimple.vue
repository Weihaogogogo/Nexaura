<template>
  <div class="relative w-full min-h-screen bg-black text-white overflow-hidden">
    <!-- Main container with space for content -->
    <div class="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 min-h-screen">
      <!-- Navigation -->
      <div class="px-4 backdrop-blur-3xl bg-black/50 rounded-full py-4 flex justify-between items-center mb-12">
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
        <div class="absolute left-0 sm:left-10 top-40 z-10 group transition-all duration-300 hover:scale-110">
          <div class="flex items-center gap-2 relative">
            <div class="relative">
              <div class="w-2 h-2 bg-white rounded-full group-hover:animate-pulse"></div>
              <div class="absolute -inset-1 bg-white/20 rounded-full blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <div class="text-white relative">
              <div class="font-medium group-hover:text-white transition-colors duration-300">Vue3</div>
              <div class="text-white/70 text-sm group-hover:text-white/70 transition-colors duration-300">for base</div>
              <div class="absolute -inset-2 bg-white/10 rounded-lg blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
            </div>
          </div>
        </div>
        
        <div class="absolute left-1/4 top-24 z-10 group transition-all duration-300 hover:scale-110">
          <div class="flex items-center gap-2 relative">
            <div class="relative">
              <div class="w-2 h-2 bg-white rounded-full group-hover:animate-pulse"></div>
              <div class="absolute -inset-1 bg-white/20 rounded-full blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <div class="text-white relative">
              <div class="font-medium group-hover:text-white transition-colors duration-300">Tailwind</div>
              <div class="text-white/70 text-sm group-hover:text-white/70 transition-colors duration-300">for styles</div>
              <div class="absolute -inset-2 bg-white/10 rounded-lg blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
            </div>
          </div>
        </div>
        
        <div class="absolute right-1/4 top-24 z-10 group transition-all duration-300 hover:scale-110">
          <div class="flex items-center gap-2 relative">
            <div class="relative">
              <div class="w-2 h-2 bg-white rounded-full group-hover:animate-pulse"></div>
              <div class="absolute -inset-1 bg-white/20 rounded-full blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <div class="text-white relative">
              <div class="font-medium group-hover:text-white transition-colors duration-300">VueUse Motion</div>
              <div class="text-white/70 text-sm group-hover:text-white/70 transition-colors duration-300">for animations</div>
              <div class="absolute -inset-2 bg-white/10 rounded-lg blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
            </div>
          </div>
        </div>
        
        <div class="absolute right-0 sm:right-10 top-40 z-10 group transition-all duration-300 hover:scale-110">
          <div class="flex items-center gap-2 relative">
            <div class="relative">
              <div class="w-2 h-2 bg-white rounded-full group-hover:animate-pulse"></div>
              <div class="absolute -inset-1 bg-white/20 rounded-full blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <div class="text-white relative">
              <div class="font-medium group-hover:text-white transition-colors duration-300">WebGL</div>
              <div class="text-white/70 text-sm group-hover:text-white/70 transition-colors duration-300">for lightning</div>
              <div class="absolute -inset-2 bg-white/10 rounded-lg blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main hero content -->
      <div class="relative z-30 flex flex-col items-center text-center max-w-4xl mx-auto">
        <!-- Hue Slider -->
        <div class="scale-50 relative w-full max-w-xs flex flex-col items-center mb-6">
          <label class="text-gray-300 text-sm mb-1">Adjust Lightning Hue</label>
          <div class="relative w-full h-5 flex items-center">
            <input
              type="range"
              min="0"
              max="360"
              step="1"
              v-model="lightningHue"
              class="w-full h-1 bg-gray-700 rounded-full appearance-none cursor-pointer"
            />
          </div>
          <div class="text-xs text-gray-500 mt-2">{{ lightningHue }}°</div>
        </div>

        <!-- Button: "Join us for free world" -->
        <button class="group flex items-center space-x-2 px-4 py-2 bg-white/5 hover:bg-white/10 backdrop-blur-sm rounded-full text-sm mb-6 transition-all duration-300 hover:scale-105 active:scale-95">
          <span>Join us for free world</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="transform group-hover:translate-x-1 transition-transform duration-300">
            <path d="M8 3L13 8L8 13M13 8H3" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>

        <h1 class="text-5xl md:text-7xl font-light mb-2">
          Hero Odyssey
        </h1>

        <h2 class="text-3xl md:text-5xl pb-3 font-light bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 bg-clip-text text-transparent">
          Lighting Up The Future
        </h2>

        <!-- Description -->
        <p class="text-gray-400 mb-9 max-w-2xl">
          Lightning animation is 100% code generated, so feel free to customize it to your liking.
        </p>

        <button class="mt-[100px] sm:mt-[100px] px-8 py-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors hover:scale-105 active:scale-95">
          Discover Those Worlds
        </button>
      </div>
    </div>

    <!-- Background elements -->
    <div class="absolute inset-0 z-0">
      <!-- Dark overlay -->
      <div class="absolute inset-0 bg-black/80"></div>

      <!-- Glowing circle -->
      <div class="absolute top-[55%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-gradient-to-b from-blue-500/20 to-purple-600/10 blur-3xl"></div>

      <!-- Central light beam with CSS lightning effect -->
      <div class="absolute top-0 w-[100%] left-1/2 transform -translate-x-1/2 h-full">
        <div class="lightning-container">
          <div 
            class="lightning-beam"
            :style="{
              '--hue': lightningHue,
              '--intensity': 0.6,
              '--speed': '1.6s'
            }"
          ></div>
          <div 
            class="lightning-glow"
            :style="{
              '--hue': lightningHue,
              '--intensity': 0.3
            }"
          ></div>
        </div>
      </div>

      <!-- Planet/sphere -->
      <div class="z-10 absolute top-[55%] left-1/2 transform -translate-x-1/2 w-[600px] h-[600px] backdrop-blur-3xl rounded-full bg-[radial-gradient(circle_at_25%_90%,_#1e386b_15%,_#000000de_70%,_#000000ed_100%)]"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
const lightningHue = ref(220)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}
</script>

<style scoped>
/* Lightning Effects */
.lightning-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.lightning-beam {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 100%;
  background: linear-gradient(
    0deg,
    transparent 0%,
    hsl(calc(var(--hue) * 1deg), 70%, 60%) 20%,
    hsl(calc(var(--hue) * 1deg), 80%, 80%) 50%,
    hsl(calc(var(--hue) * 1deg), 70%, 60%) 80%,
    transparent 100%
  );
  filter: blur(1px);
  opacity: calc(var(--intensity) * 0.8);
  animation: lightning-flicker var(--speed) ease-in-out infinite;
}

.lightning-glow {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 100%;
  background: linear-gradient(
    0deg,
    transparent 0%,
    hsl(calc(var(--hue) * 1deg), 60%, 50%) 30%,
    hsl(calc(var(--hue) * 1deg), 70%, 60%) 50%,
    hsl(calc(var(--hue) * 1deg), 60%, 50%) 70%,
    transparent 100%
  );
  filter: blur(10px);
  opacity: calc(var(--intensity) * 0.4);
  animation: lightning-pulse calc(var(--speed, 1.6s) * 2) ease-in-out infinite;
}

@keyframes lightning-flicker {
  0%, 100% { 
    opacity: calc(var(--intensity) * 0.3);
    transform: translateX(-50%) scaleY(0.8);
  }
  10% { 
    opacity: calc(var(--intensity) * 1);
    transform: translateX(-50%) scaleY(1.2);
  }
  20% { 
    opacity: calc(var(--intensity) * 0.1);
    transform: translateX(-50%) scaleY(0.6);
  }
  30% { 
    opacity: calc(var(--intensity) * 0.9);
    transform: translateX(-50%) scaleY(1.1);
  }
  50% { 
    opacity: calc(var(--intensity) * 0.7);
    transform: translateX(-50%) scaleY(1);
  }
  70% { 
    opacity: calc(var(--intensity) * 0.2);
    transform: translateX(-50%) scaleY(0.9);
  }
  80% { 
    opacity: calc(var(--intensity) * 1);
    transform: translateX(-50%) scaleY(1.3);
  }
}

@keyframes lightning-pulse {
  0%, 100% { 
    opacity: calc(var(--intensity) * 0.2);
    transform: translateX(-50%) scaleX(0.8);
  }
  50% { 
    opacity: calc(var(--intensity) * 0.6);
    transform: translateX(-50%) scaleX(1.2);
  }
}

/* Input range styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
</style> 