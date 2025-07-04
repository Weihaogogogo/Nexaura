<template>
  <div class="relative w-full min-h-screen bg-black text-white overflow-hidden">
    <!-- Main container with space for content -->
    <div class="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 min-h-screen">




      <!-- Main hero content -->
      <div class="part1-container relative z-30 flex flex-col items-center text-center max-w-5xl mx-auto">
        <h1 class="title-text text-5xl md:text-7xl font-light mb-2">
          {{ t('homepage.hero.main_title') }}
        </h1>

        <p class="description-text text-gray-400 text-base">
          {{ t('homepage.hero.title') }}
        </p>
        <p class="description-text text-gray-400 text-base">
          {{ t('homepage.hero.subtitle') }}
        </p>

        <button 
          @click="handleGetStarted"
          class="start-button mt-[100px] sm:mt-[100px] px-12 py-4 bg-purple-600 hover:bg-purple-500 rounded-full transition-colors duration-200 text-white font-semibold text-lg">
          {{ t('homepage.hero.get_started') }}
        </button>
        <div class="images-container">
          <img src="/assets/images/page.png" alt="Nexaura" class="part1-image">
          <img src="/assets/images/page_cover.png" alt="Cover" class="part1-cover-image">
        </div>
      </div>
      <!-- Part 2 -->
      <div class="part2-container relative z-30 max-w-6xl mx-auto">
        <h2 class="part2-title text-4xl md:text-5xl font-light text-center mb-16 bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 bg-clip-text text-transparent">
          <span v-if="locale === 'zh'">
            只需要几次点击，马上就能提升<br/>SEO、GEO带来的自然流量
          </span>
          <span v-else>
            {{ t('homepage.workflow.title') }}
          </span>
        </h2>
        
                 <!-- Carousel Container -->
         <div class="carousel-container flex flex-col lg:flex-row gap-8 lg:gap-12" 
              @mouseenter="stopAutoPlay" 
              @mouseleave="startAutoPlay">
           <!-- Left Side - Navigation Tabs -->
           <div class="carousel-nav flex flex-col gap-4 w-full lg:w-1/2">
            <div 
              v-for="(item, index) in carouselItems" 
              :key="index"
                             @click="handleSlideClick(index)"
                             class="nav-item flex items-start gap-4 p-4 rounded-xl cursor-pointer transition-all duration-300"
              :class="activeSlide === index ? 'nav-item-active' : 'nav-item-inactive'"
            >
              <!-- Check Icon -->
                             <div class="check-icon flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors duration-300"
                   :class="activeSlide === index ? 'border-purple-400 bg-purple-400/20' : 'border-gray-600'">
                                  <svg v-if="activeSlide === index" class="w-3 h-3 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              
              <!-- Content -->
              <div class="text-left">
                                 <h3 class="text-lg font-semibold mb-1 transition-colors duration-300"
                    :class="activeSlide === index ? 'text-white' : 'text-gray-400'">
                  {{ item.title }}
                </h3>
                                 <p class="text-xs transition-colors duration-300"
                   :class="activeSlide === index ? 'text-gray-300' : 'text-gray-500'">
                  {{ item.description }}
                </p>
              </div>
            </div>
          </div>
          
                     <!-- Right Side - Carousel Content -->
           <div class="carousel-content w-full lg:w-1/2 relative flex flex-col justify-center">
            <div class="carousel-slide-container relative overflow-hidden rounded-2xl h-80 lg:h-[400px]">
              <div 
                v-for="(item, index) in carouselItems" 
                :key="index"
                class="carousel-slide absolute inset-0 transition-all duration-500 ease-in-out"
                :class="activeSlide === index ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full'"
              >
                <img 
                  :src="item.image" 
                  :alt="item.title"
                  class="w-full h-full object-cover rounded-2xl"
                />
               </div>
             </div>
             
             <!-- Progress Indicators -->
             <div class="flex justify-center mt-6 gap-3">
               <div 
                 v-for="(item, index) in carouselItems" 
                 :key="index"
                 @click="handleSlideClick(index)"
                 class="progress-dot w-3 h-3 rounded-full cursor-pointer transition-all duration-300"
                 :class="activeSlide === index ? 'bg-purple-400 shadow-lg shadow-purple-400/50' : 'bg-gray-600 hover:bg-gray-500'"
               ></div>
             </div>
           </div>
         </div>
      </div>
      
      <!-- Part 3 -->
      <div class="part3-container relative z-30 max-w-7xl mx-auto">
        <h2 class="part3-title text-4xl md:text-5xl font-light text-center mb-16 bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 bg-clip-text text-transparent">
          {{ t('homepage.testimonials.title') }}
        </h2>
        
        <div class="testimonials-wrapper flex justify-center w-full max-w-6xl mx-auto">
          <CircularTestimonials
            :key="testimonialsKey"
            :testimonials="testimonials"
            :autoplay="true"
            :style="{
              padding: '0px'
            }"
            :colors="{
              name: '#fff',
              designation: '#999',
              testimony: '#e1e1e1',
              arrowBackground: 'rgba(147, 51, 234, 0.2)',
              arrowForeground: '#fff',
              arrowHoverBackground: 'rgba(147, 51, 234, 0.8)'
            }"
            :fontSizes="{
              name: '1.75rem',
              designation: '1rem',
              quote: '1.25rem'
            }"
          />
        </div>
      </div>
    </div>

    <!-- Footer - Full Width -->
    <footer class="footer-container relative z-30 w-full">
      <div class="footer-content max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <!-- Main Footer Content -->
        <div class="footer-grid grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <!-- Brand Section -->
          <div class="brand-section">
            <div class="flex items-center gap-3 mb-6">
              <img src="/logo.ico" alt="Nexaura" class="w-8 h-8" />
              <span class="brand-name text-xl font-bold text-white">Nexaura</span>
            </div>
            <p class="brand-description text-gray-400 text-sm leading-relaxed">
              {{ t('homepage.footer.brand.description') }}
            </p>
            <!-- Social Icons -->
            <div class="social-icons flex gap-3 mt-6">
              <a href="#" class="social-icon">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              <a href="#" class="social-icon">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" class="social-icon">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              <a href="#" class="social-icon">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
              <a href="#" class="social-icon">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 2.567-1.645 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Product Column -->
          <div class="footer-column">
            <h3 class="footer-heading text-white font-semibold mb-4">{{ t('homepage.footer.products.title') }}</h3>
            <ul class="footer-links space-y-3">
              <li><a @click="handleAIWriterClick" class="footer-link cursor-pointer">{{ t('homepage.footer.products.ai_writer') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.products.seo_tools') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.products.content_planner') }}</a></li>
            </ul>
          </div>

          <!-- Tools Column -->
          <div class="footer-column">
            <h3 class="footer-heading text-white font-semibold mb-4">{{ t('homepage.footer.tools.title') }}</h3>
            <ul class="footer-links space-y-3">
              <li><a href="#" class="footer-link">{{ t('homepage.footer.tools.keyword_research') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.tools.topic_generator') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.tools.outline_builder') }}</a></li>
            </ul>
          </div>

          <!-- Resources & Support Column -->
          <div class="footer-column">
            <h3 class="footer-heading text-white font-semibold mb-4">{{ t('homepage.footer.support.title') }}</h3>
            <ul class="footer-links space-y-3">
              <li><a href="#" class="footer-link">{{ t('homepage.footer.support.help_center') }}</a></li>
              <li><a href="/blog" class="footer-link">{{ t('homepage.footer.support.documentation') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.support.community') }}</a></li>
              <li><a href="#" class="footer-link">{{ t('homepage.footer.support.contact') }}</a></li>
            </ul>
          </div>
        </div>

        <!-- Footer Bottom -->
        <div class="footer-bottom pt-8 border-t border-gray-800">
          <div class="flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="footer-copyright text-gray-400 text-sm">
              {{ t('homepage.footer.copyright') }}
            </div>
            <div class="footer-legal flex gap-6">
              <a href="#" class="footer-link text-sm">{{ t('nav.privacy') }}</a>
              <a href="#" class="footer-link text-sm">{{ t('nav.terms') }}</a>
            </div>
            <div class="back-to-top">
              <button class="back-to-top-btn" @click="scrollToTop">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                </svg>
                {{ t('homepage.footer.back_to_top') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>

    <!-- Background elements -->
    <div class="absolute inset-0 z-0">
      <!-- Dark overlay -->
      <div class="absolute inset-0 bg-black/80"></div>

      <!-- Glowing circle -->
      <div class="absolute top-[55%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-gradient-to-b from-blue-500/20 to-purple-600/10 blur-3xl"></div>

      <!-- Central WebGL Lightning effect -->
      <div class="lightning-container absolute top-0 w-full left-1/2 transform -translate-x-1/2 h-full">
        <Lightning
          :hue="lightningHue"
          :xOffset="0"
          :speed="1.6"
          :intensity="0.6"
          :size="2"
        />
      </div>


    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/stores/modules/user'
import Lightning from '@/components/ui/Lightning.vue'
import CircularTestimonials from '@/components/ui/CircularTestimonials.vue'

const { t, locale } = useI18n()
const lightningHue = ref(270)
const router = useRouter()
const userStore = useUserStore()
const testimonialsKey = ref(0)

// Carousel data and state
const activeSlide = ref(0)
let autoPlayInterval: any = null

const carouselItems = computed(() => [
  {
    title: t('homepage.workflow.steps.step1.title'),
    description: t('homepage.workflow.steps.step1.description'),
    image: '/assets/images/step1.png'
  },
  {
    title: t('homepage.workflow.steps.step2.title'),
    description: t('homepage.workflow.steps.step2.description'),
    image: '/assets/images/step2.png'
  },
  {
    title: t('homepage.workflow.steps.step3.title'),
    description: t('homepage.workflow.steps.step3.description'),
    image: '/assets/images/step3.png'
  },
  {
    title: t('homepage.workflow.steps.step4.title'),
    description: t('homepage.workflow.steps.step4.description'),
    image: '/assets/images/step4.png'
  },
  {
    title: t('homepage.workflow.steps.step5.title'),
    description: t('homepage.workflow.steps.step5.description'),
    image: '/assets/images/step5.png'
  }
])

// Testimonials data
const testimonials = computed(() => [
  {
    quote: t('homepage.testimonials.list.card1.description'),
    name: t('homepage.testimonials.list.card1.title'),
    designation: t('homepage.testimonials.list.card1.subtitle'),
    src: "/assets/images/multi_lang.png",
  },
  {
    quote: t('homepage.testimonials.list.card2.description'),
    name: t('homepage.testimonials.list.card2.title'),
    designation: t('homepage.testimonials.list.card2.subtitle'),
    src: "/assets/images/speed.png",
  }
])

// Auto-play functionality
const startAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
  }
  autoPlayInterval = setInterval(() => {
    activeSlide.value = (activeSlide.value + 1) % carouselItems.value.length
  }, 4000) // 切换间隔4秒
}

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
    autoPlayInterval = null
  }
}

const handleSlideClick = (index: number) => {
  activeSlide.value = index
  // 用户主动切换后，重新开始自动轮播
  startAutoPlay()
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}



const handleGetStarted = () => {
  // 检查登录状态
  if (userStore.isAuthenticated) {
    // 如果已登录，跳转到dashboard
    router.push('/app/dashboard')
  } else {
    // 如果未登录，跳转到登录页面
    router.push('/login')
  }
}

// 处理AI Writer点击事件
const handleAIWriterClick = () => {
  // 检查登录状态
  if (userStore.isAuthenticated) {
    // 如果已登录，跳转到创建工作流页面
    router.push('/app/workflow/new')
  } else {
    // 如果未登录，跳转到登录页面
    router.push('/login')
  }
}

// Watch for locale changes to force re-render of testimonials
watch(locale, () => {
  testimonialsKey.value += 1
})

onMounted(() => {
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.part1-container {
  margin-top: 100px;
  margin-bottom: 250px;
  overflow: visible; /* 允许子元素超出容器边界 */
}

.title-text {
  font-family: 'Poppins', sans-serif;
  font-size: 60px;
  font-weight: 700;
  margin-bottom: 30px;
  line-height: 1.2;
  text-shadow: 
    0 0 10px rgba(255, 255, 255, 0.4),
    0 0 20px rgba(255, 255, 255, 0.3),
    0 0 30px rgba(255, 255, 255, 0.2),
    0 0 40px rgba(255, 255, 255, 0.1),
    0 0 50px rgba(147, 51, 234, 0.2),
    0 0 60px rgba(147, 51, 234, 0.2);
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.3)) drop-shadow(0 0 25px rgba(147, 51, 234, 0.2));
}

.subtitle-text {
  font-family: 'Poppins', sans-serif;
  margin-bottom: 0px;
}

.description-text {
  font-family: 'Poppins', sans-serif;
  font-weight: 400;
  font-size: 20px;
  line-height: 1.6;
}

.start-button {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  margin-top: 50px;
  transition: all 0.2s ease;
  margin-bottom: 30px;
}

.images-container {
  position: relative;
  margin-top: 40px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  max-width: 1000px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  overflow: visible; /* 允许子元素超出容器 */
}

.part1-image {
  max-width: 1000px;
  width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 
  0 0 10px rgba(255, 255, 255, 0.3),
    /* 0 20px 40px rgba(0, 0, 0, 0.3), */
    0 0 20px rgba(147, 51, 234, 0.3),
    0 0 40px rgba(147, 51, 234, 0.2),
    0 0 60px rgba(147, 51, 234, 0.1);
  opacity: 1;
  filter: 
    drop-shadow(0 0 10px rgba(147, 51, 234, 0.3))
    drop-shadow(0 0 20px rgba(147, 51, 234, 0.2));
  position: relative;
  z-index: 1;
}

.part1-cover-image {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120%; /* 超过part1-image和容器的宽度 */
  height: auto;
  z-index: 2;
  pointer-events: none; /* 确保不会阻挡下层图片的交互 */
  max-width: none; /* 移除最大宽度限制，允许超出容器 */
}



/* Part 2 */
.part2-container {
  margin-bottom: 250px;
  margin-top: 180px;
}

.part2-title {
  font-family: 'Poppins', sans-serif;
  line-height: 1.3;
}

/* Carousel Styles */
.carousel-container {
  font-family: 'Poppins', sans-serif;
}

.carousel-nav {
  @media (max-width: 1024px) {
    order: 2;
  }
}

.carousel-content {
  @media (max-width: 1024px) {
    order: 1;
  }
}

.nav-item {
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
}

.nav-item-active {
  background: rgba(147, 51, 234, 0.15);
  border-color: rgba(147, 51, 234, 0.4);
  box-shadow: 
    0 8px 32px rgba(147, 51, 234, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 20px rgba(147, 51, 234, 0.2);
}

.nav-item-inactive:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.carousel-slide-container {
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(147, 51, 234, 0.3),
    0 0 60px rgba(147, 51, 234, 0.2);
  border: 1px solid rgba(147, 51, 234, 0.2);
}

.carousel-slide img {
  /* 移除所有滤镜效果 */
}

/* Progress Indicators */
.progress-dot {
  position: relative;
}

.progress-dot:hover {
  transform: scale(1.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .carousel-slide-container {
    height: 250px;
  }
  
  .nav-item {
    padding: 1rem;
  }
  
  .check-icon {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .progress-dot {
    width: 0.75rem;
    height: 0.75rem;
  }
}

.lightning-container {
  height: 1200px;
}

/* Part 3 */

.part3-container {
  margin-top: 200px;
  width: 100%;
}

.part3-title {
  font-family: 'Poppins', sans-serif;
}

.testimonials-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0 2rem;
}

/* 使用深层选择器来调整testimonials组件内部的布局 */
.testimonials-wrapper :deep(.testimonial-grid) {
  @media (min-width: 768px) {
    grid-template-columns: auto 1fr; /* 图片保持原有大小(auto)，文本占据剩余空间并向右延伸 */
    gap: 3rem; /* 增加图片和文本之间的间距 */
  }
}

/* 设置图片区域的固定宽度，保持原有大小 */
.testimonials-wrapper :deep(.image-container) {
  @media (min-width: 768px) {
    width: 24rem; /* 固定图片容器宽度，保持原有大小 */
    flex-shrink: 0; /* 防止图片被压缩 */
  }
}

/* 文本区域向右延伸，占据更多空间 */
.testimonials-wrapper :deep(.testimonial-content) {
  margin-left:50px;
  @media (min-width: 768px) {
    min-width: 0; /* 允许文本内容灵活调整 */
    flex: 1; /* 占据剩余的所有空间 */
  }
}

/* Footer Styles */
.footer-container {
  margin-top: 150px;
  background: rgb(19, 10, 46);
  border-top: 1px solid rgba(147, 51, 234, 0.2);
  backdrop-filter: blur(10px);
}

.footer-content {
  font-family: 'Poppins', sans-serif;
}

.brand-name {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

.brand-description {
  max-width: 300px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.social-icon:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}

.footer-heading {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.1rem;
  color: #fff;
}

.footer-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.9rem;
}

.footer-link:hover {
  color: #fff;
}

.footer-copyright {
  font-family: 'Poppins', sans-serif;
  color: rgba(255, 255, 255, 0.7);
}

.footer-bottom {
  border-color: rgba(255, 255, 255, 0.2);
}

.back-to-top-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
  backdrop-filter: blur(10px);
}

.back-to-top-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}

/* Responsive Footer */
@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-bottom {
    text-align: center;
  }
  
  .footer-bottom > div {
    flex-direction: column;
    gap: 1rem;
  }
}
</style> 