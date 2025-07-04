<template>
  <section id="testimonials" class="testimonials-section section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">What our customers say</h2>
        <p class="section-description">
          Discover how our AI-powered SEO content generator has transformed businesses
        </p>
      </div>

      <div class="testimonials-grid">
        <div class="testimonial-card" v-for="testimonial in testimonials" :key="testimonial.id">
          <div class="testimonial-content">
            <div class="stars">
              <span v-for="i in 5" :key="i" class="star">★</span>
            </div>
            <p class="testimonial-text">{{ testimonial.text }}</p>
          </div>
          <div class="testimonial-author">
            <div class="author-avatar">
              {{ testimonial.author.charAt(0) }}
            </div>
            <div class="author-info">
              <div class="author-name">{{ testimonial.author }}</div>
              <div class="author-role">{{ testimonial.role }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const testimonials = ref([
  {
    id: 1,
    text: "This AI content generator has revolutionized our content marketing strategy. We've seen a 300% increase in organic traffic!",
    author: "Sarah Johnson",
    role: "Marketing Director"
  },
  {
    id: 2,
    text: "The SEO optimization features are incredible. Our articles now rank on the first page consistently.",
    author: "Mike Chen",
    role: "Content Manager"
  },
  {
    id: 3,
    text: "Easy to use and produces high-quality content. It's like having an expert SEO writer on our team 24/7.",
    author: "Emma Rodriguez",
    role: "Digital Marketing Specialist"
  }
])
</script>

<style scoped>
.testimonials-section {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 1rem;
}

.section-description {
  font-size: 1.125rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.75rem;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.testimonial-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.testimonial-card:hover::before {
  opacity: 0.05;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.testimonial-content {
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
}

.stars {
  margin-bottom: 1rem;
}

.star {
  color: #fbbf24;
  font-size: 1.25rem;
  margin-right: 0.25rem;
}

.testimonial-text {
  font-size: 1rem;
  color: #374151;
  line-height: 1.6;
  font-style: italic;
  margin: 0;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.author-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.125rem;
}

.author-name {
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 0.25rem;
}

.author-role {
  font-size: 0.875rem;
  color: #64748b;
}

@media (max-width: 768px) {
  .testimonials-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .testimonial-card {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }
}
</style>