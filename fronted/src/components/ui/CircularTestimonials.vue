<script setup lang="ts">
import { ref, onMounted, watch, nextTick, type PropType } from 'vue'
import gsap from 'gsap'
import { ArrowLeft, ArrowRight } from 'lucide-vue-next'
 
interface Testimonial {
  quote: string
  name: string
  designation: string
  src: string
}
 
const props = defineProps<{
  testimonials: Testimonial[]
  autoplay?: boolean
  colors?: {
    name?: string
    designation?: string
    testimony?: string
    arrowBackground?: string
    arrowForeground?: string
    arrowHoverBackground?: string
  }
  fontSizes?: {
    name?: string
    designation?: string
    quote?: string
  }
}>()
 
const {
  testimonials,
  autoplay = true,
  colors = {},
  fontSizes = {}
} = props
 
// Default colors
const colorName = colors.name ?? "#000"
const colorDesignation = colors.designation ?? "#6b7280"
const colorTestimony = colors.testimony ?? "#4b5563"
const colorArrowBg = colors.arrowBackground ?? "#141414"
const colorArrowFg = colors.arrowForeground ?? "#f1f1f7"
const colorArrowHoverBg = colors.arrowHoverBackground ?? "#00a6fb"
 
// Default font sizes
const fontSizeName = fontSizes.name ?? "1.5rem"
const fontSizeDesignation = fontSizes.designation ?? "0.925rem"
const fontSizeQuote = fontSizes.quote ?? "1.125rem"
 
const activeIndex = ref(0)
let autoplayInterval: ReturnType<typeof setInterval> | null = null
 
const imageContainer = ref<HTMLElement | null>(null)
const nameRef = ref<HTMLElement | null>(null)
const designationRef = ref<HTMLElement | null>(null)
const quoteRef = ref<HTMLElement | null>(null)
const hoverPrev = ref(false)
const hoverNext = ref(false)
 
function calculateGap(width: number) {
  const minWidth = 1024
  const maxWidth = 1456
  const minGap = 60
  const maxGap = 86
  if (width <= minWidth) return minGap
  if (width >= maxWidth) return Math.max(minGap, maxGap + 0.06018 * (width - maxWidth))
  return minGap + (maxGap - minGap) * ((width - minWidth) / (maxWidth - minWidth))
}
 
function animateWords() {
  if (!quoteRef.value) return
  gsap.from(quoteRef.value.querySelectorAll('.word'), {
    opacity: 0,
    y: 10,
    stagger: 0.02,
    duration: 0.2,
    ease: "power2.out"
  })
}
 
function updateTestimonial(direction: number) {
  activeIndex.value = (activeIndex.value + direction + testimonials.length) % testimonials.length
 
  nextTick(() => {
    if (imageContainer.value) {
      const containerWidth = imageContainer.value.offsetWidth
      const gap = calculateGap(containerWidth)
      const maxStickUp = gap * 0.8
      testimonials.forEach((testimonial, index) => {
        const img = imageContainer.value!.querySelector(`[data-index="${index}"]`) as HTMLElement
        if (!img) return
        const offset = (index - activeIndex.value + testimonials.length) % testimonials.length
        const zIndex = testimonials.length - Math.abs(offset)
        const opacity = index === activeIndex.value ? 1 : 1
        const scale = index === activeIndex.value ? 1 : 0.85
        let translateX, translateY, rotateY
        if (offset === 0) {
          translateX = '0%'
          translateY = '0%'
          rotateY = 0
        } else if (offset === 1 || offset === -2) {
          translateX = '20%'
          translateY = `-${maxStickUp / img.offsetHeight * 100}%`
          rotateY = -15
        } else {
          translateX = '-20%'
          translateY = `-${maxStickUp / img.offsetHeight * 100}%`
          rotateY = 15
        }
        gsap.to(img, {
          zIndex: zIndex,
          opacity: opacity,
          scale: scale,
          x: translateX,
          y: translateY,
          rotateY: rotateY,
          duration: 0.8,
          ease: "power3.out"
        })
      })
    }
 
    if (nameRef.value && designationRef.value) {
      gsap.to([nameRef.value, designationRef.value], {
        opacity: 0, y: -20, duration: 0.3, ease: "power2.in", onComplete: () => {
          nameRef.value!.textContent = testimonials[activeIndex.value].name
          designationRef.value!.textContent = testimonials[activeIndex.value].designation
          gsap.to([nameRef.value, designationRef.value], { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" })
        }
      })
    }
    if (quoteRef.value) {
      gsap.to(quoteRef.value, {
        opacity: 0, y: -20, duration: 0.3, ease: "power2.in", onComplete: () => {
          quoteRef.value!.innerHTML = testimonials[activeIndex.value].quote.split(' ').map(word => `<span class="word">${word}</span>`).join(' ')
          gsap.to(quoteRef.value, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" })
          animateWords()
        }
      })
    }
  })
}
 
function handleNext() {
  updateTestimonial(1)
  stopAutoplay()
}
function handlePrev() {
  updateTestimonial(-1)
  stopAutoplay()
}
function stopAutoplay() {
  if (autoplayInterval) clearInterval(autoplayInterval)
}
 
// Watch for testimonials changes (language switching)
watch(() => props.testimonials, () => {
  nextTick(() => {
    if (nameRef.value) nameRef.value.textContent = testimonials[activeIndex.value].name
    if (designationRef.value) designationRef.value.textContent = testimonials[activeIndex.value].designation
    if (quoteRef.value) {
      quoteRef.value.innerHTML = testimonials[activeIndex.value].quote.split(' ').map(word => `<span class="word">${word}</span>`).join(' ')
      animateWords()
    }
  })
}, { deep: true })

onMounted(() => {
  nextTick(() => {
    if (nameRef.value) nameRef.value.textContent = testimonials[activeIndex.value].name
    if (designationRef.value) designationRef.value.textContent = testimonials[activeIndex.value].designation
    if (quoteRef.value) {
      quoteRef.value.innerHTML = testimonials[activeIndex.value].quote.split(' ').map(word => `<span class="word">${word}</span>`).join(' ')
      animateWords()
    }
    if (imageContainer.value) {
      updateTestimonial(0)
    }
  })
  if (autoplay) {
    autoplayInterval = setInterval(() => updateTestimonial(1), 5000)
  }
  window.addEventListener('resize', () => updateTestimonial(0))
})
</script>
 
<template>
  <div class="testimonial-container">
    <div class="testimonial-grid">
      <div class="image-container" ref="imageContainer">
        <img
          v-for="(testimonial, index) in testimonials"
          :key="testimonial.src"
          :src="testimonial.src"
          :alt="testimonial.name"
          class="testimonial-image"
          :data-index="index"
          :style="{ opacity: index === activeIndex ? 1 : 1, zIndex: testimonials.length - Math.abs(index - activeIndex) }"
        />
      </div>
      <div class="testimonial-content">
        <div>
          <h3 class="name" ref="nameRef" :style="{ color: colorName, fontSize: fontSizeName }"></h3>
          <p class="designation" ref="designationRef" :style="{ color: colorDesignation, fontSize: fontSizeDesignation }"></p>
          <p class="quote" ref="quoteRef" :style="{ color: colorTestimony, fontSize: fontSizeQuote }"></p>
        </div>
        <div class="arrow-buttons">
          <button
            class="arrow-button prev-button"
            @click="handlePrev"
            :style="{ backgroundColor: hoverPrev ? colorArrowHoverBg : colorArrowBg }"
            @mouseenter="hoverPrev = true"
            @mouseleave="hoverPrev = false"
          >
            <ArrowLeft :size="44" :color="colorArrowFg" />
          </button>
          <button
            class="arrow-button next-button"
            @click="handleNext"
            :style="{ backgroundColor: hoverNext ? colorArrowHoverBg : colorArrowBg }"
            @mouseenter="hoverNext = true"
            @mouseleave="hoverNext = false"
          >
            <ArrowRight :size="44" :color="colorArrowFg" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
 
<style scoped>
.testimonial-container {
  width: 100%;
  max-width: 56rem;
  padding: 2rem;
}
.testimonial-grid {
  display: grid;
  gap: 5rem;
}
.image-container {
  position: relative;
  width: 100%;
  height: 24rem;
  perspective: 1000px;
}
.testimonial-image {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
.testimonial-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.name {
  font-weight: bold;
  margin-bottom: 0.25rem;
}
.designation {
  margin-bottom: 2rem;
}
.quote {
  line-height: 1.75;
}
.arrow-buttons {
  display: flex;
  gap: 1.5rem;
  padding-top: 3rem;
}
.arrow-button {
  width: 2.7rem;
  height: 2.7rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
  border: none;
}
.word {
  display: inline-block;
}
@media (min-width: 768px) {
  .testimonial-grid {
    grid-template-columns: 1fr 1fr;
  }
  .arrow-buttons {
    padding-top: 0;
  }
}
</style> 