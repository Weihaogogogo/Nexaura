<template>
  <section id="stats" class="stats-section section">
    <div class="container">
      <div class="stats-header">
        <h2 class="stats-title">More data. Additional insights</h2>
        <p class="stats-description">
          Unlock comprehensive insights with our feature, providing extensive data on content generation,
          rapid indexation, and rich analysis for enhanced SEO performance.
        </p>
      </div>

      <div class="stats-grid">
        <div class="stat-item" v-for="stat in stats" :key="stat.id">
          <div class="stat-number">{{ stat.number }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const stats = ref([
  { id: 1, number: '100,000+', label: 'Generated Articles' },
  { id: 2, number: '20,000+', label: 'Active Users' },
  { id: 3, number: '15,000+', label: 'Customers' },
  { id: 4, number: '50,000+', label: 'Keywords Analyzed' },
  { id: 5, number: '40,000+', label: 'SEO Reports' }
])
</script>

<style scoped>
.stats-section {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.stats-header {
  text-align: center;
  margin-bottom: 4rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.stats-title {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1e1b4b;
  margin-bottom: 1rem;
}

.stats-description {
  font-size: 1.125rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.stat-item {
  text-align: center;
  padding: 2rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-item::before {
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

.stat-item:hover::before {
  opacity: 0.05;
}

.stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.stat-label {
  font-size: 1rem;
  font-weight: 500;
  color: #64748b;
  position: relative;
  z-index: 1;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .stat-item {
    padding: 1.5rem 1rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .stats-title {
    font-size: 1.5rem;
  }

  .stats-description {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-number {
    font-size: 1.875rem;
  }
}
</style>