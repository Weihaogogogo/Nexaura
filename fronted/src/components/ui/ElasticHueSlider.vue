<template>
  <div class="scale-50 relative w-full max-w-xs flex flex-col items-center" ref="sliderRef">
    <label v-if="label" for="hue-slider-native" class="text-gray-300 text-sm mb-1">{{ label }}</label>
    <div class="relative w-full h-5 flex items-center">
      <!-- Native input: Handles interaction, but visually hidden -->
      <input
        id="hue-slider-native"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        :value="modelValue"
        @input="handleInput"
        @mousedown="handleMouseDown"
        @mouseup="handleMouseUp"
        @touchstart="handleMouseDown"
        @touchend="handleMouseUp"
        class="absolute inset-0 w-full h-full appearance-none bg-transparent cursor-pointer z-20"
        style="appearance: none; -webkit-appearance: none;"
      />

      <!-- Custom Track -->
      <div class="absolute left-0 w-full h-1 bg-gray-700 rounded-full z-0"></div>

      <!-- Custom Fill -->
      <div
        class="absolute left-0 h-1 bg-blue-500 rounded-full z-10"
        :style="{ width: `${thumbPosition}%` }"
      ></div>

      <!-- Custom Thumb (Animated) -->
      <div
        v-motion
        :style="{ left: `${thumbPosition}%` }"
        :initial="{ scale: 1 }"
        :animate="{ scale: isDragging ? 1.2 : 1 }"
        :transition="{ 
          type: 'spring', 
          stiffness: 500, 
          damping: isDragging ? 20 : 30 
        }"
        class="absolute top-1/2 transform -translate-y-1/2 z-30"
      >
        <!-- Thumb dot can be added here if needed -->
      </div>
    </div>

    <!-- Display current value below -->
    <Transition
      name="value-fade"
      mode="out-in"
    >
      <div
        :key="modelValue"
        class="text-xs text-gray-500 mt-2"
      >
        {{ modelValue }}°
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  modelValue: number
  min?: number
  max?: number
  step?: number
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  min: 0,
  max: 360,
  step: 1,
  label: 'Adjust Hue'
})

const emit = defineEmits<{
  'update:modelValue': [value: number]
}>()

const isDragging = ref(false)
const sliderRef = ref<HTMLDivElement>()

const progress = computed(() => (props.modelValue - props.min) / (props.max - props.min))
const thumbPosition = computed(() => progress.value * 100)

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', Number(target.value))
}

const handleMouseDown = () => {
  isDragging.value = true
}

const handleMouseUp = () => {
  isDragging.value = false
}
</script>

<style scoped>
.value-fade-enter-active,
.value-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.value-fade-enter-from {
  opacity: 0;
  transform: translateY(-5px);
}

.value-fade-leave-to {
  opacity: 0;
  transform: translateY(5px);
}

/* Remove default input styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
}

input[type="range"]::-moz-range-thumb {
  appearance: none;
}
</style> 