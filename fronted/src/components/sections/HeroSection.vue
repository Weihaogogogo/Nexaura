<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <!-- Main Heading -->
        <h1 class="hero-title fade-up">
          <span class="text-gradient gradient-animate">Best SEO Content AI Generator</span>
        </h1>

        <!-- Subtitle -->
        <p class="hero-subtitle fade-up animate-delay-200">
          Boost Your Website's Popularity Without SEO Pros, Writers, or Web Geeks. Create Great Business Blogs Quickly, Easily, and with Top-Quality!
        </p>

        <!-- CTA Buttons -->
        <div class="hero-actions fade-up animate-delay-400">
          <button class="cta-button hover-lift" @click="handleGetStarted">
            <span>Get Started</span>
            <div class="button-effect"></div>
          </button>
          <button class="demo-button hover-lift" @click="handleBookDemo">
            <span>Learn More</span>
          </button>
        </div>

        <!-- Floating Elements -->
        <div class="floating-elements">
          <div class="float-element float-1 bounce"></div>
          <div class="float-element float-2 pulse"></div>
          <div class="float-element float-3 bounce animate-delay-300"></div>
        </div>
      </div>
    </div>

    <!-- Background Effects -->
    <div class="hero-bg-effects">
      <div class="bg-gradient-1"></div>
      <div class="bg-gradient-2"></div>
      <div class="particles">
        <div class="particle" v-for="i in 20" :key="i"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function handleGetStarted() {
  router.push('/app/dashboard')
}

function handleBookDemo() {
  router.push('/about')
}
</script>

<style scoped>
.hero-section {
  position: relative;
  padding: 6rem 0;
  min-height: 90vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 2rem;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.text-gradient {
  background: linear-gradient(135deg,
    #6366f1 0%,
    #8b5cf6 25%,
    #ec4899 50%,
    #f472b6 75%,
    #6366f1 100%
  );
  background-size: 300% 300%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 5s ease infinite;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 3rem;
  max-width: 650px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}

.cta-button,
.demo-button {
  height: 56px;
  padding: 0 2.5rem;
  font-weight: 600;
  font-size: 1.1rem;
  border-radius: 0.75rem;
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  min-width: 180px;
}

.cta-button {
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.9) 0%,
    rgba(139, 92, 246, 0.9) 50%,
    rgba(236, 72, 153, 0.9) 100%
  );
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
}

.cta-button span {
  position: relative;
  z-index: 2;
}

.button-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.6s ease;
}

.cta-button:hover .button-effect {
  left: 100%;
}

.cta-button:hover {
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 1) 0%,
    rgba(139, 92, 246, 1) 50%,
    rgba(236, 72, 153, 1) 100%
  );
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4);
}

.demo-button {
  background: rgba(255, 255, 255, 0.8);
  color: #6366f1;
  border: 2px solid rgba(99, 102, 241, 0.3);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
}

.demo-button:hover {
  transform: translateY(-3px) scale(1.02);
  background: rgba(255, 255, 255, 0.95);
  border-color: #6366f1;
  box-shadow: 0 15px 35px rgba(99, 102, 241, 0.25);
}

.cta-button:active,
.demo-button:active {
  transform: translateY(-1px) scale(1.01);
}

/* Floating Elements */
.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
}

.float-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
}

.float-1 {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  top: 20%;
  left: 10%;
  animation-duration: 3s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.float-2 {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ec4899, #f472b6);
  top: 60%;
  right: 15%;
  animation-duration: 2.5s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.float-3 {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #06b6d4, #6366f1);
  bottom: 20%;
  left: 80%;
  animation-duration: 4s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Background Effects */
.hero-bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none;
}

.bg-gradient-1 {
  position: absolute;
  top: 0;
  right: 0;
  width: 60%;
  height: 100%;
  background: radial-gradient(
    ellipse at center,
    rgba(99, 102, 241, 0.15) 0%,
    rgba(139, 92, 246, 0.08) 40%,
    transparent 70%
  );
}

.bg-gradient-2 {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60%;
  height: 100%;
  background: radial-gradient(
    ellipse at center,
    rgba(236, 72, 153, 0.12) 0%,
    rgba(244, 114, 182, 0.06) 40%,
    transparent 70%
  );
}

/* Particles */
.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(99, 102, 241, 0.4);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

.particle:nth-child(odd) {
  animation-delay: -2s;
  background: rgba(236, 72, 153, 0.4);
  box-shadow: 0 0 10px rgba(236, 72, 153, 0.3);
}

.particle:nth-child(3n) {
  background: rgba(6, 182, 212, 0.4);
  box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
}

.particle:nth-child(1) { top: 10%; left: 20%; }
.particle:nth-child(2) { top: 20%; left: 80%; }
.particle:nth-child(3) { top: 40%; left: 40%; }
.particle:nth-child(4) { top: 60%; left: 70%; }
.particle:nth-child(5) { top: 80%; left: 30%; }
.particle:nth-child(6) { top: 30%; left: 60%; }
.particle:nth-child(7) { top: 70%; left: 10%; }
.particle:nth-child(8) { top: 15%; left: 50%; }
.particle:nth-child(9) { top: 55%; left: 85%; }
.particle:nth-child(10) { top: 85%; left: 65%; }
.particle:nth-child(11) { top: 25%; left: 15%; }
.particle:nth-child(12) { top: 45%; left: 75%; }
.particle:nth-child(13) { top: 65%; left: 25%; }
.particle:nth-child(14) { top: 35%; left: 90%; }
.particle:nth-child(15) { top: 75%; left: 45%; }
.particle:nth-child(16) { top: 5%; left: 35%; }
.particle:nth-child(17) { top: 95%; left: 55%; }
.particle:nth-child(18) { top: 50%; left: 5%; }
.particle:nth-child(19) { top: 90%; left: 80%; }
.particle:nth-child(20) { top: 10%; left: 90%; }

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.3;
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
    opacity: 0.8;
  }
  66% {
    transform: translateY(20px) rotate(240deg);
    opacity: 0.5;
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

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 闪烁动画 */
@keyframes bounce {
  0%, 100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

.bounce {
  animation: bounce 1s infinite;
}

.fade-up {
  opacity: 0;
  transform: translateY(50px);
  animation: fadeUpAnimation 1s ease-out forwards;
}

.animate-delay-200 {
  animation-delay: 200ms;
}

.animate-delay-400 {
  animation-delay: 400ms;
}

.animate-delay-300 {
  animation-delay: 300ms;
}

@keyframes fadeUpAnimation {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .hero-section {
    padding: 4rem 0;
    min-height: 80vh;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .cta-button,
  .demo-button {
    width: 100%;
    max-width: 300px;
  }

  .float-element {
    display: none;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .cta-button,
  .demo-button {
    height: 48px;
    font-size: 1rem;
  }
}
</style>