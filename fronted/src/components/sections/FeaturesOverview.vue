<template>
  <section id="features" class="features-overview section">
    <div class="container">
      <div class="section-header fade-up">
        <h2 class="section-title">See what's inside</h2>
      </div>

      <div class="features-grid">
        <!-- Blogging Platform -->
        <a
          href="#detailed-features"
          class="feature-card fade-up animate-delay-200 hover-lift"
          @click.prevent="scrollToSection('detailed-features')"
        >
          <div class="feature-icon">
            <img
              src="https://ext.same-assets.com/2911992724/2059557380.webp"
              alt="Blogging Platform"
              class="icon-img"
            />
          </div>
          <div class="feature-content">
            <h3 class="feature-title">SEO Article Generator</h3>
            <p class="feature-description">
              Intuitive editor, powerful AI. Create SEO-optimized articles effortlessly.
            </p>
          </div>
          <div class="feature-arrow">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
            </svg>
          </div>
        </a>

        <!-- AI Blog Writing -->
        <a
          href="#detailed-features"
          class="feature-card"
          @click.prevent="scrollToSection('detailed-features')"
        >
          <div class="feature-icon">
            <img
              src="https://ext.same-assets.com/2911992724/3440733359.webp"
              alt="AI Blog Writing"
              class="icon-img"
            />
          </div>
          <div class="feature-content">
            <h3 class="feature-title">AI Content Writing</h3>
            <p class="feature-description">
              Integrates real-time knowledge and writing like a pro writer.
            </p>
          </div>
          <div class="feature-arrow">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
            </svg>
          </div>
        </a>

        <!-- SEO -->
        <a
          href="#detailed-features"
          class="feature-card"
          @click.prevent="scrollToSection('detailed-features')"
        >
          <div class="feature-icon">
            <img
              src="https://ext.same-assets.com/2911992724/2728454526.webp"
              alt="SEO Optimization"
              class="icon-img"
            />
          </div>
          <div class="feature-content">
            <h3 class="feature-title">SEO Optimization</h3>
            <p class="feature-description">
              Build SEO-optimized content via AI and get quick SEO wins.
            </p>
          </div>
          <div class="feature-arrow">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
            </svg>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
function scrollToSection(sectionId: string) {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })
  }
}
</script>

<style scoped>
.features-overview {
  background: #fafbff;
  position: relative;
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section {
  padding: 4rem 0;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 1.5rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 0.75rem;
  padding: 2rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.feature-card:hover::before {
  opacity: 0.08;
}

.feature-card:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.85);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 15px 45px rgba(31, 38, 135, 0.15);
}

.feature-card:hover .feature-title {
  color: #6366f1;
}

.feature-card:hover .feature-arrow {
  transform: translateX(4px);
  color: #6366f1;
}

.feature-icon {
  flex-shrink: 0;
  position: relative;
  z-index: 2;
}

.icon-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.feature-content {
  flex: 1;
  position: relative;
  z-index: 2;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 0.5rem;
  transition: color 0.3s ease;
}

.feature-description {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.feature-arrow {
  flex-shrink: 0;
  color: #94a3b8;
  font-size: 1.125rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.fade-up {
  opacity: 0;
  transform: translateY(50px);
  animation: fadeUpAnimation 1s ease-out forwards;
}

.animate-delay-200 {
  animation-delay: 200ms;
}

.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

@keyframes fadeUpAnimation {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .feature-card {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }

  .icon-img {
    width: 60px;
    height: 60px;
  }

  .feature-title {
    font-size: 1.125rem;
  }

  .feature-description {
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.5rem;
  }

  .feature-card {
    padding: 1rem;
  }

  .icon-img {
    width: 48px;
    height: 48px;
  }
}
</style>