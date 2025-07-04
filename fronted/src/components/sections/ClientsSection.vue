<template>
  <section class="clients-section section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Trusted by leading companies</h2>
        <p class="section-description">
          Join thousands of businesses that trust our AI-powered SEO content generator
        </p>
      </div>

      <div class="clients-grid">
        <div class="client-logo" v-for="client in clients" :key="client.id">
          <div class="logo-placeholder">
            {{ client.name }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const clients = ref([
  { id: 1, name: 'TechCorp' },
  { id: 2, name: 'MarketingPro' },
  { id: 3, name: 'ContentHub' },
  { id: 4, name: 'SEOExperts' },
  { id: 5, name: 'DigitalAgency' },
  { id: 6, name: 'GrowthLabs' }
])
</script>

<style scoped>
.clients-section {
  background: #fafbff;
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
  max-width: 500px;
  margin: 0 auto;
}

.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  align-items: center;
}

.client-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80px;
}

.logo-placeholder {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 0.5rem;
  color: #6366f1;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logo-placeholder:hover {
  background: rgba(99, 102, 241, 0.1);
  border-color: #6366f1;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .clients-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .clients-grid {
    grid-template-columns: 1fr;
  }
}
</style>