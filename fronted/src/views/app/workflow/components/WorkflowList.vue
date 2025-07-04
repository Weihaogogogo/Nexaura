<template>
  <div class="workflow-list">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-loading 
        :text="t('common.loading')"
        background="rgba(0, 0, 0, 0.7)"
        element-loading-background="transparent"
      />
    </div>
    
    <!-- Empty State -->
    <div v-else-if="paginatedWorkflows.length === 0" class="empty-container">
      <el-empty :description="emptyDescription">
        <template #image>
          <el-icon :size="60" color="#c0c4cc">
          <component :is="emptyIcon" />
          </el-icon>
        </template>
      </el-empty>
    </div>
    
    <!-- Workflow Grid -->
    <div v-else class="workflow-list-content">
      <div class="workflow-grid">
      <div 
          v-for="workflow in paginatedWorkflows" 
        :key="workflow.session_id"
          class="workflow-card"
        @click="handleSelect(workflow)"
      >
          <!-- Card Header -->
          <div class="card-header">
            <div class="title-section">
              <h3 class="workflow-title">{{ workflow.article_title || workflow.keyword }}</h3>
              <div class="status-badge-wrapper">
                <el-tag 
                  :type="getStatusTagType(status)"
                  :size="'default'"
                  round
                >
                  <el-icon style="margin-right: 4px;">
          <component :is="statusIcon" />
                  </el-icon>
                  {{ getStatusLabel(status) }}
                </el-tag>
        </div>
            </div>
          </div>
          
          <!-- Card Content -->
          <div class="card-content">
            <div class="info-grid">
              <!-- 关键词信息 -->
              <div class="info-item keyword-item">
                <span class="info-label">
                  <el-icon><Key /></el-icon>
                  {{ t('workflow.card.keyword') }}
                </span>
                <span class="keyword-value">{{ workflow.keyword }}</span>
              </div>

              <!-- 市场语言信息 -->
              <div class="info-item">
                <span class="info-label">
                  <el-icon><MapLocation /></el-icon>
                  {{ t('workflow.card.market_language') }}
                </span>
                <div class="info-value">
                  <el-tag size="small" color="#e6f7ff" style="margin-right: 4px;">
                    {{ getMarketLabel(workflow.target_market) }}
                  </el-tag>
                  <el-tag size="small" color="#f6f6f6">
                    {{ getLanguageLabel(workflow.article_language) }}
                  </el-tag>
                </div>
            </div>
            
              <!-- 话题信息 -->
              <div v-if="workflow.chosen_topic" class="info-item full-width">
                <span class="info-label">
                  <el-icon><ChatLineRound /></el-icon>
                  {{ t('workflow.card.topic') }}
                </span>
                <span class="info-value topic-text">{{ workflow.chosen_topic }}</span>
            </div>
            
              <!-- 进度信息（所有状态都显示） -->
              <div v-if="status === 'completed' || status === 'in_progress' || status === 'failed'" class="info-item full-width">
                <span class="info-label">
                  <el-icon><Timer /></el-icon>
                  {{ t('workflow.card.progress') }}
                </span>
                <div class="progress-content">
                  <el-progress 
                    :percentage="getProgressPercent(workflow.current_node_index, status)" 
                    :stroke-width="8"
                    :text-inside="false"
                    style="width: 120px;"
              />
                </div>
            </div>
            
              <!-- 错误信息（仅失败状态显示） -->
              <div v-if="status === 'failed' && workflow.failed_message" class="info-item full-width error-item">
                <span class="info-label">
                  <el-icon><Warning /></el-icon>
                  {{ t('workflow.card.error_info') }}
                </span>
                <span class="info-value error-text">{{ workflow.failed_message }}</span>
              </div>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="card-footer">
            <div class="timestamps">
              <span class="time-item">
                <el-icon><Calendar /></el-icon>
                <span class="time-label">{{ t('workflow.card.created') }}:</span>
                {{ formatDate(workflow.created_time) }}
              </span>
              <span class="time-item">
                <el-icon><Clock /></el-icon>
                <span class="time-label">{{ t('workflow.card.updated') }}:</span>
                {{ formatDate(workflow.updated_time) }}
              </span>
        </div>
        
            <div class="actions">
              <el-button 
                v-if="status === 'completed'"
                type="text" 
                size="small"
                :icon="View"
                @click.stop="handleSelect(workflow)"
              >
                {{ t('workflow.card.view') }}
              </el-button>
              
              <el-button 
                v-if="status === 'in_progress'"
                type="text" 
                size="small"
                :icon="View"
                @click.stop="handleSelect(workflow)"
              >
                {{ t('workflow.card.view_progress') }}
              </el-button>
              
              <el-button 
                v-if="status === 'failed'"
                type="text" 
                size="small"
                :icon="View"
                @click.stop="handleSelect(workflow)"
              >
                {{ t('workflow.card.view') }}
              </el-button>


            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="workflows.length > pageSize" class="pagination-container">
        <div class="custom-pagination">
          <!-- 总条数显示 -->
          <div class="pagination-total">
            {{ t('workflow.pagination.total', { total: workflows.length }) }}
          </div>
          
          <!-- 每页显示条数 -->
          <div class="pagination-sizes">
            <el-select v-model="pageSize" @change="handleSizeChange" size="small">
              <el-option :label="`6 ${t('workflow.pagination.items_per_page')}`" :value="6" />
              <el-option :label="`10 ${t('workflow.pagination.items_per_page')}`" :value="10" />
              <el-option :label="`20 ${t('workflow.pagination.items_per_page')}`" :value="20" />
              <el-option :label="`50 ${t('workflow.pagination.items_per_page')}`" :value="50" />
            </el-select>
          </div>

          <!-- 核心分页器 -->
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="workflows.length"
            layout="prev, pager, next"
            background
            @current-change="handleCurrentChange"
          />

          <!-- 跳转到指定页 -->
          <div class="pagination-jumper">
            <span>{{ t('workflow.pagination.goto') }}</span>
            <el-input 
              v-model="jumpPageInput" 
              size="small"
              @keyup.enter="handleJumpToPage"
              style="width: 50px; margin: 0 4px;"
            />
            <span>{{ t('workflow.pagination.page') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import {
  Select, Timer, CloseBold, Files, Clock, Warning,
  View,
  Calendar, Key, MapLocation, ChatLineRound
} from '@element-plus/icons-vue'
import type { WorkflowsModel } from '@/types/workflow'

interface Props {
  workflows: WorkflowsModel[]
  loading?: boolean
  status: 'completed' | 'in_progress' | 'failed'
}

interface Emits {
  (e: 'select', workflow: WorkflowsModel): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const { t } = useI18n()

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(6)
const jumpPageInput = ref('')

// Computed
const statusIcon = computed(() => {
  switch (props.status) {
    case 'completed': return Select
    case 'in_progress': return Timer
    case 'failed': return CloseBold
    default: return Files
  }
})

const emptyIcon = computed(() => {
  switch (props.status) {
    case 'completed': return Select
    case 'in_progress': return Clock
    case 'failed': return CloseBold
    default: return Files
  }
})

const emptyDescription = computed(() => {
  switch (props.status) {
    case 'completed': return t('workflow.empty.completed')
    case 'in_progress': return t('workflow.empty.in_progress')
    case 'failed': return t('workflow.empty.failed')
    default: return t('workflow.empty.default')
  }
})

// 分页计算
const paginatedWorkflows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return props.workflows.slice(start, end)
})

// 分页器多语言文本
const totalText = computed(() => {
  return t('workflow.pagination.total', { total: props.workflows.length })
})

const jumperBeforeText = computed(() => t('workflow.pagination.goto'))
const jumperAfterText = computed(() => t('workflow.pagination.page'))

// Watch workflows change to reset pagination
watch(() => props.workflows, () => {
  currentPage.value = 1
})

// Methods
const formatDate = (dateStr: string) => {
  try {
    // Handle YYYY-MM-DD HH:MM:SS format
    if (dateStr && dateStr.includes(' ')) {
      const [datePart, timePart] = dateStr.split(' ')
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
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

const getMarketLabel = (market: string) => {
  return t(`workflow.market.${market}`, market)
}

const getLanguageLabel = (language: string) => {
  return t(`workflow.language.${language}`, language)
}

const getProgressPercent = (currentNodeIndex: number, status?: string) => {
  let nodeIndex = currentNodeIndex
  
  // 如果是失败状态，使用 current_node_index - 1
  if (status === 'failed') {
    nodeIndex = currentNodeIndex - 1
  }
  
  const percentage = Math.round((nodeIndex / 4) * 100)
  return percentage > 100 ? 100 : percentage
}

const handleSelect = (workflow: WorkflowsModel) => {
  emit('select', workflow)
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
  const maxPage = Math.ceil(props.workflows.length / pageSize.value)
  
  if (page >= 1 && page <= maxPage) {
    currentPage.value = page
    jumpPageInput.value = ''
  }
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  switch (status) {
    case 'completed': return 'success'
    case 'in_progress': return 'info'  
    case 'failed': return 'danger'
    default: return 'info'
  }
}

// 获取状态标签文本
const getStatusLabel = (status: string) => {
  switch (status) {
    case 'completed': return t('workflow.stats.completed')
    case 'in_progress': return t('workflow.stats.in_progress')
    case 'failed': return t('workflow.stats.failed')
    default: return '未知'
  }
}
</script>

<style scoped>
.workflow-list {
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.loading-container,
.empty-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.workflow-list-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.workflow-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  flex: 1;
  min-height: 500px;
  max-height: 800px;
  overflow-y: auto;
  padding-right: 8px;
  padding-top: 5px;
}

/* 滚动条样式 */
.workflow-grid::-webkit-scrollbar {
  width: 6px;
}

.workflow-grid::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.workflow-grid::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.workflow-grid::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.workflow-card {
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

.workflow-card:hover {
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

.card-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.title-section {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.workflow-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.status-badge-wrapper {
  flex-shrink: 0;
}

.card-content {
  padding: 16px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  flex: 1;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
}

.info-item.keyword-item {
  align-items: center;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
  color: #606266;
  white-space: nowrap;
  font-size: 13px;
  min-width: 80px;
}

.info-value {
  color: #303133;
  line-height: 1.4;
}

.keyword-value {
  color: #409eff;
  font-weight: 500;
  background: #e6f7ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 13px;
  display: inline-block;
  white-space: nowrap;
}

.topic-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.progress-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-text {
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

/* 进度条流光紫色主题 */
.progress-content :deep(.el-progress-bar__outer) {
  background-color: rgba(128, 95, 244, 0.15);
  border-radius: 4px;
}

.progress-content :deep(.el-progress-bar__inner) {
  background: linear-gradient(135deg, 
    rgba(128, 95, 244, 0.8) 0%, 
    rgba(139, 92, 246, 0.9) 50%,
    rgba(147, 51, 234, 0.8) 100%
  );
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

/* 流光动画效果 */
.progress-content :deep(.el-progress-bar__inner::after) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.3), 
    transparent
  );
  animation: progress-flow 2s ease-in-out infinite;
}

@keyframes progress-flow {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
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

.error-item {
  background: #fef0f0;
  border: 1px solid #fde2e2;
  border-radius: 6px;
  padding: 8px;
  margin: -4px 0;
}

.error-text {
  color: #f56c6c;
  font-size: 13px;
  line-height: 1.4;
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
  align-items: center;
  gap: 8px;
}

/* 查看按钮样式，与文章列表保持一致 */
.actions :deep(.el-button--text) {
  color: #595959 !important;
  font-weight: 400;
}

.actions :deep(.el-button--text:hover) {
  color: #000000 !important;
  background-color: rgba(0, 0, 0, 0.04) !important;
}

/* 市场/语言标签颜色覆盖，不使用紫色主题 */
.info-value :deep(.el-tag) {
  border: 1px solid #d9d9d9 !important;
}

/* 市场标签 - 蓝色主题 */
.info-value :deep(.el-tag:first-child) {
  background-color: #e6f7ff !important;
  color: #1890ff !important;
  border-color: #91d5ff !important;
}

/* 语言标签 - 灰色主题 */
.info-value :deep(.el-tag:last-child) {
  background-color: #f6f6f6 !important;
  color: #666666 !important;
  border-color: #d9d9d9 !important;
}

/* 移除重复的样式定义 */

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

.pagination-sizes :deep(.el-select .el-select__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

.pagination-sizes :deep(.el-select .el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

.pagination-sizes :deep(.el-select .el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.9) inset;
}

@media (max-width: 1200px) {
  .workflow-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .workflow-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    min-height: 400px;
    max-height: 600px;
  }
  
  .workflow-card {
    min-height: 200px;
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
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .actions {
    justify-content: center;
  }
  
  .workflow-title {
    font-size: 15px;
  }
  
  .info-label {
    min-width: 70px;
    font-size: 12px;
  }
  
  .info-value {
    font-size: 13px;
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
  .title-section {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .workflow-title {
    font-size: 14px;
  }
}
</style>