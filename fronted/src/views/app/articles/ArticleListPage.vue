<template>
  <div class="article-list-page">
    <!-- Controls -->
    <div class="controls-section">
      <div class="stats">
        <span class="total-count">{{ t('articles.stats.total', { total: totalArticles }) }}</span>
      </div>
      
      <div class="sort-controls">
        <a-select 
          v-model:value="sortBy" 
          style="width: 150px; margin-right: 12px"
          @change="handleSortChange"
        >
          <a-select-option value="updated_time">{{ t('articles.sort.updated_time') }}</a-select-option>
          <a-select-option value="created_time">{{ t('articles.sort.created_time') }}</a-select-option>
          <a-select-option value="article_title">{{ t('articles.sort.article_title') }}</a-select-option>
        </a-select>
        
        <a-select 
          v-model:value="sortOrder" 
          style="width: 100px"
          @change="handleSortChange"
        >
          <a-select-option value="desc">{{ t('articles.sort.desc') }}</a-select-option>
          <a-select-option value="asc">{{ t('articles.sort.asc') }}</a-select-option>
        </a-select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-section">
      <a-spin size="large" :tip="t('articles.loading')" />
    </div>

    <!-- Empty State -->
    <div v-else-if="allArticles.length === 0" class="empty-section">
      <a-empty 
        :description="t('articles.empty.no_articles')"
        :image="h(FileTextOutlined)"
      >
        <template #description>
          <span>{{ t('articles.empty.no_articles') }}</span>
        </template>
        <a-button type="primary" @click="goToWorkflow">
          {{ t('articles.empty.create_new') }}
        </a-button>
      </a-empty>
    </div>

    <!-- Article Grid -->
    <div v-else class="articles-grid">
      <div 
        v-for="article in paginatedArticles" 
        :key="article.session_id"
        class="article-card"
        @click="goToArticleDetail(article.session_id)"
      >
        <div class="card-header">
          <h3 class="article-title">{{ article.article_title }}</h3>
          <div class="article-meta">
            <a-tag :color="getLanguageColor(article.article_language)">
              {{ article.article_language }}
            </a-tag>
            <a-tag color="blue">{{ article.target_market.toUpperCase() }}</a-tag>
          </div>
        </div>
        
        <div class="card-content">
          <div class="article-info">
            <div class="keyword-section">
              <span class="label">{{ t('articles.card.keyword') }}:</span>
              <span class="keyword">{{ article.keyword }}</span>
            </div>
            
            <div v-if="article.article_description" class="description-section">
              <p class="description">{{ truncateText(article.article_description, 100) }}</p>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="timestamps">
            <span class="time-item">
              <CalendarOutlined />
              <span class="time-label">{{ t('articles.card.created') }}:</span>
              {{ formatDate(article.created_time) }}
            </span>
            <span class="time-item">
              <ClockCircleOutlined />
              <span class="time-label">{{ t('articles.card.updated') }}:</span>
              {{ formatDate(article.updated_time) }}
            </span>
          </div>
          
          <div class="actions">
            <a-button 
              type="text" 
              size="small"
              :icon="h(EyeOutlined)"
              @click.stop="goToArticleDetail(article.session_id)"
            >
              {{ t('articles.card.view') }}
            </a-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="allArticles.length > pageSize" class="pagination-container">
      <div class="custom-pagination">
        <!-- 总条数显示 -->
        <div class="pagination-total">
          {{ t('articles.pagination.total', { total: allArticles.length }) }}
        </div>
        
        <!-- 每页显示条数 -->
        <div class="pagination-sizes">
          <el-select v-model="pageSize" @change="handleSizeChange" size="small">
            <el-option :label="`6 ${t('articles.pagination.items_per_page')}`" :value="6" />
            <el-option :label="`10 ${t('articles.pagination.items_per_page')}`" :value="10" />
            <el-option :label="`20 ${t('articles.pagination.items_per_page')}`" :value="20" />
            <el-option :label="`50 ${t('articles.pagination.items_per_page')}`" :value="50" />
          </el-select>
        </div>

        <!-- 核心分页器 -->
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="allArticles.length"
          layout="prev, pager, next"
          background
          @current-change="handleCurrentChange"
        />

        <!-- 跳转到指定页 -->
        <div class="pagination-jumper">
          <span>{{ t('articles.pagination.goto') }}</span>
          <el-input 
            v-model="jumpPageInput" 
            size="small"
            @keyup.enter="handleJumpToPage"
            style="width: 50px; margin: 0 4px;"
          />
          <span>{{ t('articles.pagination.page') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { ElPagination } from 'element-plus'
import { 
  FileTextOutlined,
  CalendarOutlined,
  ClockCircleOutlined,
  EyeOutlined
} from '@ant-design/icons-vue'
import { generationApi } from '@/services/api/generation'
import type { ArticleListItem, PaginationInfo } from '@/services/api/generation'

const router = useRouter()
const { t } = useI18n()

// State
const allArticles = ref<ArticleListItem[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(6)
const sortBy = ref('updated_time')
const sortOrder = ref<'asc' | 'desc'>('desc')
const jumpPageInput = ref('')

// Computed
const totalArticles = computed(() => allArticles.value.length)

// 分页计算
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allArticles.value.slice(start, end)
})

// Methods
const loadArticles = async () => {
  try {
    loading.value = true
    
    // 获取所有文章数据，不使用API分页
    const response = await generationApi.getCompletedArticles({
      page: 1,
      per_page: 1000, // 获取足够多的数据
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    })
    
    allArticles.value = response.articles
    
  } catch (error: any) {
    console.error('Failed to load articles:', error)
    message.error(error.message || t('articles.messages.load_failed'))
  } finally {
    loading.value = false
  }
}

const handleSortChange = () => {
  currentPage.value = 1 // Reset to first page when sorting changes
  loadArticles()
}

// 分页事件处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

const handleJumpToPage = () => {
  const page = parseInt(jumpPageInput.value)
  const maxPage = Math.ceil(allArticles.value.length / pageSize.value)
  
  if (page >= 1 && page <= maxPage) {
    currentPage.value = page
    jumpPageInput.value = ''
  }
}

const goToArticleDetail = (sessionId: number) => {
  router.push(`/app/articles/${sessionId}`)
}

const goToWorkflow = () => {
  router.push('/app/workflow/new')
}

const getLanguageColor = (language: string): string => {
  const colors: Record<string, string> = {
    'english': 'blue',
    'chinese': 'red',
    'spanish': 'orange',
    'french': 'purple',
    'german': 'green'
  }
  return colors[language.toLowerCase()] || 'default'
}

const formatDate = (dateString: string): string => {
  try {
    // Handle YYYY-MM-DD HH:MM:SS format
    if (dateString && dateString.includes(' ')) {
      const [datePart, timePart] = dateString.split(' ')
      const [year, month, day] = datePart.split('-')
      const [hour, minute] = timePart.split(':')
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute))
      
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Fallback for other formats
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}



// Lifecycle
onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
.article-list-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

.controls-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stats .total-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.sort-controls {
  display: flex;
  align-items: center;
}

.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.empty-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 32px;
  min-height: 500px;
}

.article-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
  min-height: 240px;
  max-height: 350px;
  display: flex;
  flex-direction: column;
}

.article-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border: 2px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, 
                rgba(128, 95, 244, 0.8) 0%, 
                rgba(139, 92, 246, 0.9) 25%,
                rgba(147, 51, 234, 0.8) 50%,
                rgba(139, 92, 246, 0.9) 75%,
                rgba(128, 95, 244, 0.8) 100%
              ) border-box;
  background-size: 200% 200%;
  animation: border-flow 3s ease-in-out infinite;
  transform: translateY(-2px);
}

/* 流光边框动画 */
@keyframes border-flow {
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

.card-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 8px;
}

.card-content {
  padding: 16px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.keyword-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.keyword-section .label {
  font-size: 12px;
  color: #999;
  font-weight: 500;
}

.keyword-section .keyword {
  font-size: 14px;
  color: #1890ff;
  font-weight: 500;
  background: #e6f7ff;
  padding: 2px 8px;
  border-radius: 4px;
}

.description-section .description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

.card-footer {
  padding: 16px 20px;
  background: #fafafa;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.timestamps {
  display: flex;
  align-items: center;
  gap: 16px;
}

.time-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.time-item .time-label {
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 8px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #e4e7ed;
  margin-top: 16px;
  background: #fafafa;
}

.custom-pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-total {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.pagination-sizes :deep(.el-select) {
  width: auto;
  min-width: 120px;
}

.pagination-jumper {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #606266;
}

.pagination-jumper :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

.pagination-jumper :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

.pagination-jumper :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

.pagination-sizes :deep(.el-select .el-select__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

.pagination-sizes :deep(.el-select .el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

.pagination-sizes :deep(.el-select .el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

/* 分页器紫色主题样式 */
.pagination-container :deep(.el-pagination .el-pager li.is-active) {
  background-color: rgba(139, 92, 246, 0.9) !important;
  border-color: rgba(139, 92, 246, 0.9) !important;
  color: white !important;
}

.pagination-container :deep(.el-pagination .el-pager li:hover) {
  color: rgba(139, 92, 246, 0.9) !important;
}

.pagination-container :deep(.el-pagination .btn-next:hover),
.pagination-container :deep(.el-pagination .btn-prev:hover) {
  color: rgba(139, 92, 246, 0.9) !important;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .article-list-page {
    padding: 16px;
  }
  
  .controls-section {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .sort-controls {
    justify-content: center;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    min-height: 400px;
  }
  
  .article-card {
    min-height: 200px;
    max-height: 300px;
  }
  
  .card-header {
    padding: 16px;
  }
  
  .card-content {
    padding: 12px 16px;
  }
  
  .card-footer {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .timestamps {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .actions {
    justify-content: center;
  }
  
  .pagination-container {
    padding: 16px 0;
  }
  
  :deep(.el-pagination) {
    justify-content: center;
  }
  
  :deep(.el-pagination .el-pager li) {
    min-width: 28px;
    height: 28px;
    line-height: 28px;
    margin: 0 2px;
  }
}

@media (max-width: 480px) {
  .article-title {
    font-size: 16px;
  }
}


</style>