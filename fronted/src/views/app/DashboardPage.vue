<template>
  <div class="dashboard-page">

    <!-- Hero Section -->
    <div class="hero-section glass-morphism">
      <div class="hero-content">
        <div class="welcome-section">
          <h1 class="hero-title gradient-text">
            {{ t('dashboard.title') }}, {{ userStore.user?.name || 'Creator' }}
          </h1>
          <p class="hero-subtitle">
            {{ t('dashboard.subtitle') }}
          </p>
        </div>
        <div class="hero-actions">
          <button @click="startGeneration" class="primary-action-btn glass-button">
            <div class="btn-content">
              <EditOutlined class="btn-icon" />
              <span>{{ t('dashboard.quick_actions.new_workflow') }}</span>
            </div>
            <div class="btn-glow"></div>
          </button>
          <button @click="viewArticles" class="secondary-action-btn glass-button">
            <div class="btn-content">
              <FileTextOutlined class="btn-icon" />
              <span>{{ t('dashboard.quick_actions.view_articles') }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Content Grid -->
    <div class="content-grid">
      <!-- Usage Analytics -->
      <div class="glass-morphism usage-analytics-panel">
        <div class="panel-header">
          <div>
            <h3 class="panel-title gradient-text">{{ t('dashboard.overview.title') }}</h3>
            <div class="panel-decoration"></div>
          </div>
          <div class="date-controls">
            <span style="margin-right: 12px; color: #6b7280; font-weight: 500;">{{ t('common.date_range') }}:</span>
            <a-range-picker 
              v-model:value="dateRange"
              :format="'YYYY-MM-DD'"
              :placeholder="[t('common.start_date'), t('common.end_date')]"
              @change="handleDateRangeChange"
              style="width: 280px;"
            />
          </div>
        </div>
        
        <div v-if="loading" class="chart-loading">
          <a-spin size="large">
            <template #indicator>
              <loading-outlined style="font-size: 32px; color: #8b5cf6;" spin />
            </template>
          </a-spin>
        </div>
        
        <div v-else class="chart-container">
          <canvas ref="chartCanvas" id="usage-chart"></canvas>
        </div>
      </div>

      <!-- Recent Articles Panel -->
      <div class="recent-articles-panel glass-morphism">
        <div class="panel-header">
          <h3 class="panel-title gradient-text">{{ t('dashboard.recent_articles.title') }}</h3>
          <button class="view-all-btn" @click="viewArticles">
            {{ t('common.view') }} {{ t('nav.articles') }}
            <ArrowRightOutlined />
          </button>
        </div>
        <div class="articles-list" v-if="!loading && recentArticles.length > 0">
          <div class="article-item" v-for="article in recentArticles" :key="article.session_id">
            <div class="article-thumbnail">
              <div class="thumbnail-placeholder gradient-bg-1">
                <FileTextOutlined />
              </div>
            </div>
            <div class="article-content">
              <h4 
                ref="titleRefs" 
                class="article-title"
                :data-truncated="checkTextTruncation(article.article_title, 'title')"
              >
                {{ article.article_title }}
              </h4>
              <p 
                ref="excerptRefs" 
                class="article-excerpt"
                :data-truncated="checkTextTruncation(article.article_description || '', 'excerpt')"
              >
                {{ article.article_description || '' }}
              </p>
              <div class="article-meta">
                <span class="language-tag">
                  {{ getLanguageLabel(article.article_language) }}
                </span>
                <span class="article-date">{{ formatDate(article.updated_time) }}</span>
              </div>
            </div>
            <div class="article-actions">
              <button class="action-btn" @click="viewArticle(article.session_id)" title="View">
                <EyeOutlined />
              </button>
            </div>
          </div>
        </div>
        <div v-else-if="!loading && recentArticles.length === 0" class="empty-articles">
          <a-empty :description="t('dashboard.recent_articles.no_data')" />
      </div>
        <div v-else class="articles-loading">
          <a-spin size="large" :tip="t('dashboard.recent_articles.loading')" />
    </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed, watch, onActivated } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  EditOutlined,
  FileTextOutlined,
  ArrowRightOutlined,
  EyeOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/modules/user'
import { generationApi } from '@/services/api/generation'
import type { ArticleListItem, WorkflowListResponse } from '@/services/api/generation'
import dayjs from 'dayjs'
import type { Dayjs } from 'dayjs'
import { useDateFormat } from '@vueuse/core'

// Import Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend
)

const router = useRouter()
const route = useRoute()
const { t, locale } = useI18n()
const userStore = useUserStore()

const loading = ref(true)
const chartCanvas = ref<HTMLCanvasElement>()
const chart = ref<ChartJS | null>(null)
const dateRange = ref<[Dayjs, Dayjs]>([dayjs().subtract(15, 'day'), dayjs()])
const recentArticles = ref<ArticleListItem[]>([])
const allWorkflows = ref<any[]>([])
const allArticles = ref<ArticleListItem[]>([])
const titleRefs = ref<HTMLElement[]>([])
const excerptRefs = ref<HTMLElement[]>([])

// Computed properties
const workflowTotal = computed(() => allWorkflows.value.length)
const articleTotal = computed(() => allArticles.value.length)

// Generate chart data
const chartData = computed(() => {
  if (!dateRange.value || !Array.isArray(dateRange.value) || dateRange.value.length !== 2) {
    return null
  }

  const [startDate, endDate] = dateRange.value
  if (!startDate || !endDate) return null

  // Generate date labels for the range
  const labels: string[] = []
  const workflowCounts: number[] = []
  const articleCounts: number[] = []
  const workflowPointRadii: number[] = []
  const articlePointRadii: number[] = []

  let currentDate = startDate.clone()
      while (currentDate.isBefore(endDate) || currentDate.isSame(endDate, 'day')) {
    const dateStr = currentDate.format('YYYY-MM-DD')
    labels.push(currentDate.format('MM/DD'))

    // Count workflows for this date - 使用正确的字段名
    const workflowCount = allWorkflows.value.filter(workflow => {
      const workflowDate = dayjs(workflow.created_time || workflow.created_at).format('YYYY-MM-DD')
      return workflowDate === dateStr
    }).length

    // Count articles for this date - 使用正确的字段名
    const articleCount = allArticles.value.filter(article => {
      const articleDate = dayjs(article.created_time).format('YYYY-MM-DD')
      return articleDate === dateStr
    }).length

    workflowCounts.push(workflowCount)
    articleCounts.push(articleCount)
    
    // 如果数据为0，隐藏锚点
    workflowPointRadii.push(workflowCount > 0 ? 4 : 0)
    articlePointRadii.push(articleCount > 0 ? 4 : 0)

    currentDate = currentDate.add(1, 'day')
  }

  return {
    labels,
    datasets: [
      {
        label: t('dashboard.overview.workflow_count'),
        data: workflowCounts,
        borderColor: '#8b5cf6',
        backgroundColor: '#8b5cf6',
        pointBackgroundColor: '#8b5cf6',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: workflowPointRadii,
        pointHoverRadius: workflowPointRadii.map(r => r > 0 ? 6 : 0),
        borderWidth: 2,
        tension: 0.4,
        fill: false
      },
      {
        label: t('dashboard.overview.article_generation'),
        data: articleCounts,
        borderColor: '#ec4899',
        backgroundColor: '#ec4899',
        pointBackgroundColor: '#ec4899',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: articlePointRadii,
        pointHoverRadius: articlePointRadii.map(r => r > 0 ? 6 : 0),
        borderWidth: 2,
        tension: 0.4,
        fill: false
      }
    ]
  }
})

// Initialize chart
const initChart = () => {
  if (!chartCanvas.value || !chartData.value) {
    return
  }

  // 等待DOM完全挂载
  return nextTick(() => {
    // 确保canvas仍然存在于DOM中
    if (!chartCanvas.value || !chartCanvas.value.isConnected) {
      console.warn('Canvas not connected to DOM, retrying...')
      setTimeout(() => initChart(), 100)
      return
    }

    // Destroy existing chart and clear canvas
    if (chart.value) {
      chart.value.destroy()
      chart.value = null
    }

    // Clear any existing Chart.js instances on this canvas
    const existingChart = ChartJS.getChart(chartCanvas.value)
    if (existingChart) {
      existingChart.destroy()
    }

    try {
      const ctx = chartCanvas.value.getContext('2d')
      if (!ctx) {
        console.warn('Cannot get 2d context from canvas')
        return
      }

      // 确保canvas有正确的尺寸
      const container = chartCanvas.value.parentElement
      if (container) {
        const containerRect = container.getBoundingClientRect()
        if (containerRect.width === 0 || containerRect.height === 0) {
          console.warn('Container has zero dimensions, retrying...')
          setTimeout(() => initChart(), 100)
          return
        }
      }

      // Create chart with optimized config
      chart.value = new ChartJS(ctx, {
      type: 'line',
      data: chartData.value,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        resizeDelay: 0,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              usePointStyle: true,
              pointStyle: 'circle',
              padding: 20,
              font: {
                size: 14,
                weight: 500
              },
              color: '#374151',
              generateLabels: function(chart: any) {
                const datasets = chart.data.datasets
                return datasets.map((dataset: any, index: number) => {
                  const meta = chart.getDatasetMeta(index)
                  const isHidden = meta.hidden
                  
                  return {
                    text: dataset.label,
                    fillStyle: isHidden ? '#d1d5db' : dataset.borderColor,
                    strokeStyle: isHidden ? '#d1d5db' : dataset.borderColor,
                    pointStyle: 'circle',
                    hidden: false, // 不使用原生的hidden状态
                    datasetIndex: index,
                    fontColor: isHidden ? '#9ca3af' : '#374151'
                  }
                })
              }
            },
            onClick: (evt: any, item: any, legend: any) => {
              const index = item.datasetIndex
              const meta = legend.chart.getDatasetMeta(index)
              meta.hidden = meta.hidden === null ? !legend.chart.data.datasets[index].hidden : null
              legend.chart.update()
            }
          },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#111827',
            bodyColor: '#374151',
            borderColor: '#e5e7eb',
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true,
            usePointStyle: true,
            padding: 12,
            bodyFont: {
              size: 13
            },
            titleFont: {
              size: 14,
              weight: 600
            },
            callbacks: {
              title: function(context: any) {
                const dataIndex = context[0].dataIndex
                const startDate = dateRange.value![0]
                const currentDate = startDate.add(dataIndex, 'day')
                return currentDate.format('YYYY年MM月DD日')
              },
              label: function(context: any) {
                const datasetLabel = context.dataset.label
                const value = context.parsed.y
                return `${datasetLabel}: ${value}`
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            grid: {
              display: true,
              color: 'rgba(229, 231, 235, 0.5)'
            },
            ticks: {
              color: '#6b7280',
              font: {
                size: 12
              }
            }
          },
          y: {
            display: true,
            beginAtZero: true,
            grid: {
              display: true,
              color: 'rgba(229, 231, 235, 0.5)'
            },
            ticks: {
              color: '#6b7280',
              font: {
                size: 12
              },
              stepSize: 1
            }
          }
        }
      }
    })
    
      } catch (error) {
      console.error('Error creating chart:', error)
    }
  })
}

// Load data
const loadData = async () => {
  try {
    loading.value = true
    
    const [workflowResponse, articlesResponse] = await Promise.all([
      generationApi.getWorkflowList(),
      generationApi.getCompletedArticles({ per_page: 1000 })
    ])
    
    // Flatten all workflows
    allWorkflows.value = [
      ...(workflowResponse.completed || []),
      ...(workflowResponse.in_progress || []),
      ...(workflowResponse.failed || [])
    ]
    
    allArticles.value = articlesResponse.articles || []
    
    // Get recent articles
    const sortedArticles = [...allArticles.value]
      .sort((a, b) => new Date(b.updated_time).getTime() - new Date(a.updated_time).getTime())
      .slice(0, 3)
    
    recentArticles.value = sortedArticles
    
    loading.value = false
    
    // Wait for DOM update and then initialize chart
    await nextTick()
    setTimeout(() => {
      initChart()
      updateTruncationStates()
    }, 200)
    
  } catch (error: any) {
    console.error('Failed to load dashboard data:', error)
    loading.value = false
  }
}

// Handle date range change
const handleDateRangeChange = async () => {
  if (dateRange.value && Array.isArray(dateRange.value) && dateRange.value.length === 2) {
    await nextTick()
    initChart()
  }
}

// Navigation methods
const startGeneration = () => {
  router.push('/app/workflow/new')
}

const viewArticles = () => {
  router.push('/app/articles')
}

const viewArticle = (sessionId: number) => {
  router.push(`/app/articles/${sessionId}`)
}

// Utility methods
const getLanguageLabel = (language: string) => {
  const languageMap: Record<string, string> = {
    'english': '英语',
    'chinese': '中文',
    'spanish': '西班牙语',
    'french': '法语',
    'german': '德语',
    'japanese': '日语'
  }
  return languageMap[language] || language
}

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('MM月DD日')
}

const truncateText = (text: string, maxLength: number): string => {
  if (!text || text.length <= maxLength) return text || ''
  return text.substring(0, maxLength) + '...'
}

// Check if text is truncated
const checkTextTruncation = (text: string, type: 'title' | 'excerpt'): boolean => {
  if (!text) return false
  
  // Use a more responsive approach
  nextTick(() => {
    const elements = type === 'title' ? titleRefs.value : excerptRefs.value
    elements.forEach((element) => {
      if (element && element.textContent === text) {
        const isOverflowing = element.scrollWidth > element.clientWidth
        element.setAttribute('data-truncated', isOverflowing.toString())
      }
    })
  })
  
  // Return false initially, will be updated by nextTick
  return false
}

// Update truncation states for all elements
const updateTruncationStates = () => {
  nextTick(() => {
    // Check title elements
    titleRefs.value.forEach((element) => {
      if (element) {
        const isOverflowing = element.scrollWidth > element.clientWidth
        element.setAttribute('data-truncated', isOverflowing.toString())
      }
    })
    
    // Check excerpt elements  
    excerptRefs.value.forEach((element) => {
      if (element) {
        const isOverflowing = element.scrollWidth > element.clientWidth
        element.setAttribute('data-truncated', isOverflowing.toString())
      }
    })
  })
}

// Utility function for debouncing
const debounce = (func: Function, wait: number) => {
  let timeout: any
  return function executedFunction(...args: any[]) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Handle window resize with debouncing
const handleResize = debounce(() => {
  if (chart.value) {
    chart.value.resize()
  }
  // Update truncation states on resize
  updateTruncationStates()
}, 150)

// 监听语言切换，重新初始化图表
watch(locale, () => {
  // 当语言切换时，重新初始化图表以更新翻译文本
  if (chartCanvas.value && chartData.value && !loading.value) {
    setTimeout(() => {
      initChart()
    }, 100)
  }
}, { immediate: false })

// 监听路由变化，重建图表
watch(() => route.path, (newPath) => {
  if (newPath === '/app/dashboard') {
    // 当切换回dashboard页面时，延迟重建图表
    setTimeout(() => {
      if (chartCanvas.value && chartData.value && !loading.value) {
        initChart()
      }
    }, 300)
  }
}, { immediate: false })

// Lifecycle
onMounted(async () => {
  try {
    await loadData()
    window.addEventListener('resize', handleResize)
  } catch (error) {
    console.error('Dashboard initialization error:', error)
  }
})

onUnmounted(() => {
  // 清理图表实例
  if (chart.value) {
    try {
      chart.value.destroy()
      chart.value = null
    } catch (error) {
      console.warn('Error destroying chart:', error)
    }
  }
  
  // 清理canvas上的所有Chart.js实例
  if (chartCanvas.value) {
    const existingChart = ChartJS.getChart(chartCanvas.value)
    if (existingChart) {
      try {
        existingChart.destroy()
      } catch (error) {
        console.warn('Error destroying existing chart:', error)
      }
    }
  }
  
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* Base Layout */
.dashboard-page {
  min-height: 100vh;
  padding: 24px;
  position: relative;
  background: linear-gradient(135deg, 
    rgba(99, 102, 241, 0.03) 0%, 
    rgba(139, 92, 246, 0.05) 25%,
    rgba(236, 72, 153, 0.03) 50%,
    rgba(6, 182, 212, 0.04) 75%,
    rgba(244, 114, 182, 0.02) 100%
  );
  overflow-x: hidden;
}


/* Glass Morphism Base */
.glass-morphism {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 1;
  transition: background-color 0.2s ease;
}

.glass-morphism:hover {
  background: rgba(255, 255, 255, 0.9);
}

/* Hero Section */
.hero-section {
  margin-bottom: 40px;
  padding: 48px;
  text-align: center;
  overflow: hidden;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  margin: 0 0 24px 0;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, 
    #6366f1 0%, 
    #8b5cf6 25%, 
    #ec4899 50%, 
    #06b6d4 75%, 
    #f472b6 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(55, 65, 81, 0.8);
  margin: 0 0 48px 0;
  line-height: 1.6;
  font-weight: 500;
}

.hero-actions {
  display: flex;
  gap: 24px;
  justify-content: center;
  align-items: center;
}

/* Glass Buttons */
.glass-button {
  position: relative;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 12px;
  padding: 0;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.primary-action-btn.glass-button {
  background: linear-gradient(135deg, 
    #5b5ff1, 
    #7c3aed
  ) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.secondary-action-btn {
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 32px;
  font-size: 18px;
  font-weight: 600;
  color: white;
  z-index: 2;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.secondary-action-btn .btn-content {
  color: #374151;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-icon {
  font-size: 24px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.25);
  border-color: rgba(99, 102, 241, 0.3);
}

.glass-button:hover .btn-icon {
  transform: scale(1.1);
}

.primary-action-btn.glass-button:hover {
  background: linear-gradient(135deg, 
    #6366f1, 
    #8b5cf6
  ) !important;
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4);
  border-color: rgba(139, 92, 246, 0.5);
}

.secondary-action-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  border-color: rgba(156, 163, 175, 0.4);
}

.secondary-action-btn:hover .btn-content {
  color: #1f2937;
}

/* 按钮按下效果 */
.glass-button:active {
  transform: translateY(-1px);
  transition: all 0.1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 轻量级按钮光效 */
.primary-action-btn.glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
  z-index: 1;
}

.primary-action-btn.glass-button:hover::before {
  left: 100%;
}

/* 为secondary按钮也添加光效 */
.secondary-action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: 1;
}

.secondary-action-btn:hover::before {
  left: 100%;
}

/* Content Grid */
.content-grid {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

/* Panel Headers */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(229, 231, 235, 0.4);
}

.panel-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.panel-decoration {
  width: 40px;
  height: 4px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 2px;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #6366f1;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: rgba(99, 102, 241, 0.1);
}

.date-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Usage Analytics Panel */
.usage-analytics-panel {
  padding: 32px;
  flex: 1;
  min-width: 700px;
}

.chart-container {
  height: 300px;
  position: relative;
  width: 100%;
}

.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}

.chart-loading,
.articles-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

/* Recent Articles Panel */
.recent-articles-panel {
  padding: 32px;
  flex: 1;
  min-width: 600px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.2s ease;
}

.article-item:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.article-thumbnail {
  flex-shrink: 0;
}

.thumbnail-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.gradient-bg-1 {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.gradient-bg-2 {
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
}

.gradient-bg-3 {
  background: linear-gradient(135deg, #ec4899, #06b6d4);
}

.gradient-bg-4 {
  background: linear-gradient(135deg, #06b6d4, #f472b6);
}

.article-content {
  flex: 1;
  min-width: 0;
}

.article-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  position: relative;
}

.article-title::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 40px;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.5) 70%, rgba(255, 255, 255, 0.8));
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.article-title[data-truncated="true"]::after {
  opacity: 1;
}

.article-item:hover .article-title::after {
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.6) 70%, rgba(255, 255, 255, 0.9));
}

.article-excerpt {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 12px 0;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  position: relative;
}

.article-excerpt::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 40px;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.5) 70%, rgba(255, 255, 255, 0.8));
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.article-excerpt[data-truncated="true"]::after {
  opacity: 1;
}

.article-item:hover .article-excerpt::after {
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.6) 70%, rgba(255, 255, 255, 0.9));
}

.article-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}

.language-tag {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.article-date {
  font-size: 12px;
  color: #9ca3af;
}

.article-actions {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.8);
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

/* Responsive Design */
@media (max-width: 1400px) {
  .content-grid {
    flex-direction: column;
  }
  
  .usage-analytics-panel,
  .recent-articles-panel {
    min-width: unset;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 16px;
  }
  
  .hero-section {
    padding: 32px 24px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .hero-actions {
    flex-direction: column;
    gap: 16px;
  }
  
  .btn-content {
    padding: 16px 24px;
    font-size: 16px;
  }
  
  .usage-analytics-panel,
  .recent-articles-panel {
    padding: 24px;
    min-width: unset;
  }
  
  .panel-title {
    font-size: 20px;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .date-controls {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .date-controls .ant-picker {
    width: 100% !important;
  }
}

/* Element Plus compatibility */
:deep(.el-date-editor) {
  width: 280px;
}

@media (max-width: 768px) {
  :deep(.el-date-editor) {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .dashboard-page {
    padding: 12px;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .article-item {
    flex-direction: column;
    gap: 12px;
  }
  
  .article-actions {
    align-self: flex-end;
  }
  
  .article-title::after,
  .article-excerpt::after {
    width: 30px;
  }
}

</style>