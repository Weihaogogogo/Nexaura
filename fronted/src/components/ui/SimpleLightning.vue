<template>
  <div class="lightning-container">
    <!-- Animated lightning effect using CSS -->
    <div 
      class="lightning-beam"
      :style="{
        '--hue': hue,
        '--intensity': intensity,
        '--speed': speed + 's'
      }"
    ></div>
    <div 
      class="lightning-glow"
      :style="{
        '--hue': hue,
        '--intensity': intensity * 0.5
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  hue?: number
  xOffset?: number
  speed?: number
  intensity?: number
  size?: number
}

withDefaults(defineProps<Props>(), {
  hue: 230,
  xOffset: 0,
  speed: 1,
  intensity: 1,
  size: 1
})
</script>

<style scoped>
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
  animation: lightning-pulse calc(var(--speed) * 2) ease-in-out infinite;
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
</style> 