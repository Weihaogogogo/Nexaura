<template>
  <div class="skeleton-screen">
    <!-- Article Skeleton -->
    <div v-if="type === 'article'" class="article-skeleton">
      <a-skeleton-title :width="'60%'" />
      <a-skeleton-paragraph :rows="1" :width="['80%']" />
      
      <div class="skeleton-section" v-for="i in sections" :key="i">
        <a-skeleton-title :width="'40%'" size="small" />
        <a-skeleton-paragraph :rows="3" :width="['100%', '95%', '85%']" />
      </div>
    </div>
    
    <!-- Card List Skeleton -->
    <div v-else-if="type === 'cards'" class="cards-skeleton">
      <div v-for="i in count" :key="i" class="skeleton-card">
        <a-skeleton-avatar size="large" />
        <div class="skeleton-card-content">
          <a-skeleton-title :width="'70%'" />
          <a-skeleton-paragraph :rows="2" :width="['100%', '60%']" />
        </div>
      </div>
    </div>
    
    <!-- Topics Skeleton -->
    <div v-else-if="type === 'topics'" class="topics-skeleton">
      <div v-for="i in count" :key="i" class="skeleton-topic">
        <div class="skeleton-topic-header">
          <a-skeleton-title :width="'80%'" />
          <a-skeleton-avatar shape="square" size="small" />
        </div>
        <a-skeleton-paragraph :rows="2" :width="['100%', '70%']" />
        <div class="skeleton-tags">
          <a-skeleton-button v-for="j in 3" :key="j" size="small" />
        </div>
      </div>
    </div>
    
    <!-- Titles Skeleton -->
    <div v-else-if="type === 'titles'" class="titles-skeleton">
      <div v-for="i in count" :key="i" class="skeleton-title-item">
        <div class="skeleton-title-content">
          <a-skeleton-title :width="'85%'" />
          <div class="skeleton-title-meta">
            <a-skeleton-button size="small" />
            <a-skeleton-button size="small" />
            <a-skeleton-button size="small" />
          </div>
        </div>
        <a-skeleton-button shape="round" />
      </div>
    </div>
    
    <!-- Outline Skeleton -->
    <div v-else-if="type === 'outline'" class="outline-skeleton">
      <div v-for="i in sections" :key="i" class="skeleton-outline-section">
        <div class="skeleton-outline-item level-1">
          <a-skeleton-avatar shape="square" size="small" />
          <a-skeleton-title :width="'50%'" />
        </div>
        <div v-for="j in 2" :key="j" class="skeleton-outline-item level-2">
          <a-skeleton-avatar shape="square" size="small" />
          <a-skeleton-title :width="'40%'" size="small" />
        </div>
      </div>
    </div>
    
    <!-- Default Content Skeleton -->
    <div v-else class="content-skeleton">
      <a-skeleton :paragraph="{ rows: rows, width: widths }" :title="showTitle" :loading="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  type?: 'article' | 'cards' | 'topics' | 'titles' | 'outline' | 'content'
  count?: number
  sections?: number
  rows?: number
  widths?: string[]
  showTitle?: boolean
}

withDefaults(defineProps<Props>(), {
  type: 'content',
  count: 3,
  sections: 4,
  rows: 4,
  widths: () => ['100%', '100%', '100%', '60%'],
  showTitle: true
})
</script>

<style scoped>
.skeleton-screen {
  padding: 24px;
}

/* Article Skeleton */
.article-skeleton {
  max-width: 800px;
  margin: 0 auto;
}

.skeleton-section {
  margin: 32px 0;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.skeleton-section:last-child {
  border-bottom: none;
}

/* Cards Skeleton */
.cards-skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.skeleton-card-content {
  flex: 1;
}

/* Topics Skeleton */
.topics-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.skeleton-topic {
  padding: 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
}

.skeleton-topic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.skeleton-tags {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

/* Titles Skeleton */
.titles-skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-title-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.skeleton-title-content {
  flex: 1;
  margin-right: 16px;
}

.skeleton-title-meta {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

/* Outline Skeleton */
.outline-skeleton {
  background: white;
  border-radius: 8px;
  padding: 24px;
}

.skeleton-outline-section {
  margin-bottom: 24px;
}

.skeleton-outline-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
}

.skeleton-outline-item.level-1 {
  margin-left: 0;
}

.skeleton-outline-item.level-2 {
  margin-left: 32px;
}

/* Responsive */
@media (max-width: 768px) {
  .skeleton-screen {
    padding: 16px;
  }
  
  .topics-skeleton {
    grid-template-columns: 1fr;
  }
  
  .skeleton-title-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .skeleton-title-content {
    margin-right: 0;
    width: 100%;
  }
}
</style>