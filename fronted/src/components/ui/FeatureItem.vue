<template>
  <div :class="`absolute ${position} z-10 group transition-all duration-300 hover:scale-110`">
    <div class="flex items-center gap-2 relative">
      <!-- Dot with constant glow -->
      <div class="relative">
        <div class="w-2 h-2 bg-white rounded-full group-hover:animate-pulse"></div>
        <div class="absolute -inset-1 bg-white/20 rounded-full blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      <div class="text-white relative">
        <div class="font-medium group-hover:text-white transition-colors duration-300">{{ name }}</div>
        <div class="text-white/70 text-sm group-hover:text-white/70 transition-colors duration-300">{{ value }}</div>
        <!-- Constant white glow that intensifies on hover -->
        <div class="absolute -inset-2 bg-white/10 rounded-lg blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  name: string
  value: string
  position: string
}

defineProps<Props>()
</script>

<style scoped>
/* FeatureItem specific styles */
</style> 