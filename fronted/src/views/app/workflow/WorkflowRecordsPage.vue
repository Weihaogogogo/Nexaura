<template>
  <div class="workflow-records-page">
    <!-- <div class="page-header">
      <h1 class="page-title">工作流记录</h1>
      <p class="page-description">查看和管理您的所有文章生成工作流</p>
    </div> -->

    <div class="records-content">
      <!-- Statistics Cards -->
      <div class="stats-cards">
        <el-card 
          class="stat-card completed" 
          shadow="hover"
          :body-style="{ padding: '24px' }"
        >
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ workflowList?.completed?.length || 0 }}</div>
              <div class="stat-label">{{ t('workflow.stats.completed') }}</div>
            </div>
          </div>
        </el-card>
        
        <el-card 
          class="stat-card in-progress" 
          shadow="hover"
          :body-style="{ padding: '24px' }"
        >
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ workflowList?.in_progress?.length || 0 }}</div>
              <div class="stat-label">{{ t('workflow.stats.in_progress') }}</div>
            </div>
          </div>
        </el-card>
        
        <el-card 
          class="stat-card failed" 
          shadow="hover"
          :body-style="{ padding: '24px' }"
        >
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><CircleClose /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ workflowList?.failed?.length || 0 }}</div>
              <div class="stat-label">{{ t('workflow.stats.failed') }}</div>
            </div>
          </div>
        </el-card>
        
        <el-card 
          class="stat-card total" 
          shadow="hover"
          :body-style="{ padding: '24px' }"
        >
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ workflowList?.total || 0 }}</div>
              <div class="stat-label">{{ t('workflow.stats.total') }}</div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Workflow Tabs -->
      <div class="workflow-tabs">
        <el-tabs 
          v-model="activeTab" 
          class="demo-tabs"
          @tab-change="handleTabChange"
        >
          <el-tab-pane :label="t('workflow.tabs.completed')" name="completed">
            <!-- Sort Controls -->
            <div class="tab-controls">
              <div class="sort-controls">
                <span class="sort-label">{{ t('workflow.sort.label') }}：</span>
                <el-select 
                  v-model="sortBy" 
                  style="width: 120px; margin-right: 8px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.updated_time')" value="updated_time" />
                  <el-option :label="t('workflow.sort.created_time')" value="created_time" />
                  <el-option :label="t('workflow.sort.keyword')" value="keyword" />
                </el-select>
                
                <el-select 
                  v-model="sortOrder" 
                  style="width: 80px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.desc')" value="desc" />
                  <el-option :label="t('workflow.sort.asc')" value="asc" />
                </el-select>
              </div>
              
              <div class="refresh-controls">
                <el-button 
                  :icon="Refresh" 
                  :loading="loading"
                  size="small"
                  @click="handleRefresh"
                  circle
                  plain
                />
              </div>
            </div>
            
            <div class="workflow-list-container">
              <WorkflowList 
                :workflows="sortedCompletedWorkflows"
                :loading="loading"
                status="completed"
                @select="handleWorkflowSelect"
                @delete="handleWorkflowDelete"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane :label="t('workflow.tabs.in_progress')" name="in_progress">
            <!-- Sort Controls -->
            <div class="tab-controls">
              <div class="sort-controls">
                <span class="sort-label">{{ t('workflow.sort.label') }}：</span>
                <el-select 
                  v-model="sortBy" 
                  style="width: 120px; margin-right: 8px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.updated_time')" value="updated_time" />
                  <el-option :label="t('workflow.sort.created_time')" value="created_time" />
                  <el-option :label="t('workflow.sort.keyword')" value="keyword" />
                </el-select>
                
                <el-select 
                  v-model="sortOrder" 
                  style="width: 80px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.desc')" value="desc" />
                  <el-option :label="t('workflow.sort.asc')" value="asc" />
                </el-select>
              </div>
              
              <div class="refresh-controls">
                <el-button 
                  :icon="Refresh" 
                  :loading="loading"
                  size="small"
                  @click="handleRefresh"
                  circle
                  plain
                />
              </div>
            </div>
            
            <div class="workflow-list-container">
              <WorkflowList 
                :workflows="sortedInProgressWorkflows"
                :loading="loading"
                status="in_progress"
                @select="handleWorkflowSelect"
                @delete="handleWorkflowDelete"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane :label="t('workflow.tabs.failed')" name="failed">
            <!-- Sort Controls -->
            <div class="tab-controls">
              <div class="sort-controls">
                <span class="sort-label">{{ t('workflow.sort.label') }}：</span>
                <el-select 
                  v-model="sortBy" 
                  style="width: 120px; margin-right: 8px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.updated_time')" value="updated_time" />
                  <el-option :label="t('workflow.sort.created_time')" value="created_time" />
                  <el-option :label="t('workflow.sort.keyword')" value="keyword" />
                </el-select>
                
                <el-select 
                  v-model="sortOrder" 
                  style="width: 80px"
                  @change="handleSortChange"
                >
                  <el-option :label="t('workflow.sort.desc')" value="desc" />
                  <el-option :label="t('workflow.sort.asc')" value="asc" />
                </el-select>
              </div>
              
              <div class="refresh-controls">
                <el-button 
                  :icon="Refresh" 
                  :loading="loading"
                  size="small"
                  @click="handleRefresh"
                  circle
                  plain
                />
              </div>
            </div>
            
            <div class="workflow-list-container">
              <WorkflowList 
                :workflows="sortedFailedWorkflows"
                :loading="loading"
                status="failed"
                @select="handleWorkflowSelect"
                @delete="handleWorkflowDelete"
                @retry="handleWorkflowRetry"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { 
  CircleCheck,
  Clock,
  CircleClose,
  Document,
  Refresh
} from '@element-plus/icons-vue'
import { generationApi, type WorkflowListResponse } from '@/services/api/generation'
import type { WorkflowsModel } from '@/types/workflow'
import WorkflowList from './components/WorkflowList.vue'

const router = useRouter()
const { t } = useI18n()

// State
const loading = ref(false)
const activeTab = ref('completed')
const workflowList = ref<WorkflowListResponse | null>(null)
const sortBy = ref<'updated_time' | 'created_time' | 'keyword'>('updated_time')
const sortOrder = ref<'asc' | 'desc'>('desc')

// Computed
const sortedCompletedWorkflows = computed(() => {
  return sortWorkflows(workflowList.value?.completed || [])
})

const sortedInProgressWorkflows = computed(() => {
  return sortWorkflows(workflowList.value?.in_progress || [])
})

const sortedFailedWorkflows = computed(() => {
  return sortWorkflows(workflowList.value?.failed || [])
})

// Methods
const parseDateTime = (dateTimeStr: string): Date => {
  try {
    // Handle YYYY-MM-DD HH:MM:SS format
    if (dateTimeStr && dateTimeStr.includes(' ')) {
      const [datePart, timePart] = dateTimeStr.split(' ')
      const [year, month, day] = datePart.split('-')
      const [hour, minute, second] = timePart.split(':')
      return new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute), parseInt(second || '0'))
    }
    
    // Fallback for other formats
    return new Date(dateTimeStr)
  } catch {
    return new Date(0) // Return epoch if parsing fails
  }
}

const sortWorkflows = (workflows: WorkflowsModel[]) => {
  if (!workflows || workflows.length === 0) return []
  
  return [...workflows].sort((a, b) => {
    let valueA: any
    let valueB: any
    
    switch (sortBy.value) {
      case 'updated_time':
        valueA = parseDateTime(a.updated_time || a.created_time)
        valueB = parseDateTime(b.updated_time || b.created_time)
        break
      case 'created_time':
        valueA = parseDateTime(a.created_time)
        valueB = parseDateTime(b.created_time)
        break
      case 'keyword':
        valueA = (a.keyword || '').toLowerCase()
        valueB = (b.keyword || '').toLowerCase()
        break
      default:
        return 0
    }
    
    if (sortOrder.value === 'asc') {
      return valueA > valueB ? 1 : valueA < valueB ? -1 : 0
    } else {
      return valueA < valueB ? 1 : valueA > valueB ? -1 : 0
    }
  })
}

const handleSortChange = () => {
  // Sorting is handled by computed properties, no need for additional logic
}

const loadWorkflowList = async () => {
  try {
    loading.value = true
    const data = await generationApi.getWorkflowList()
    workflowList.value = data
  } catch (error: any) {
    ElMessage.error(error.message || t('workflow.messages.load_failed'))
  } finally {
    loading.value = false
  }
}

const handleTabChange = (name: string) => {
  activeTab.value = name
}

const handleRefresh = async () => {
  await loadWorkflowList()
  ElMessage.success(t('workflow.messages.refreshed'))
}

const handleWorkflowSelect = (workflow: WorkflowsModel) => {
  // Navigate to workflow page
  router.push(`/app/workflow/${workflow.session_id}`)
}

const handleWorkflowDelete = async (workflow: WorkflowsModel) => {
  try {
    // TODO: Implement delete workflow API
    ElMessage.success(t('workflow.messages.deleted'))
    await loadWorkflowList() // Refresh list
  } catch (error: any) {
    ElMessage.error(error.message || t('workflow.messages.delete_failed'))
  }
}

const handleWorkflowRetry = async (workflow: WorkflowsModel) => {
  try {
    // Navigate to workflow page to retry
    router.push(`/app/workflow/${workflow.session_id}`)
  } catch (error: any) {
    ElMessage.error(error.message || t('workflow.messages.retry_failed'))
  }
}

// Lifecycle
onMounted(() => {
  loadWorkflowList()
})
</script>

<style scoped>
.workflow-records-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.page-description {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.records-content {
  /* 背景颜色将在AppLayout的content-wrapper中设置 */
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  /* cursor: pointer; */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #6b46c1;
  background: linear-gradient(135deg, 
    rgba(139, 92, 246, 0.15) 0%, 
    rgba(99, 102, 241, 0.2) 100%
  );
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 26px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #a0a0a0;
  font-weight: 500;
}

.workflow-tabs {
  margin-top: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

:deep(.el-tabs__header) {
  margin-bottom: 0;
  background: white;
  padding: 0 24px;
  border-radius: 12px 12px 0 0;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.el-tabs__item) {
  height: 60px;
  line-height: 60px;
  font-size: 16px;
  font-weight: 500;
  color: #606266;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  padding: 0 24px !important;
  text-align: center !important;
  box-sizing: border-box !important;
}

/* Element Plus tabs 居中对齐 - 保持自然宽度 */
:deep(.el-tabs__nav) {
  display: flex !important;
  width: 100% !important;
}

:deep(.el-tabs__nav .el-tabs__item) {
  text-align: center !important;
  flex: none !important;
  min-width: auto !important;
}

:deep(.el-tabs__item.is-active) {
  color: #805ff4 !important;
  border-bottom-color: #805ff4 !important;
  background: linear-gradient(180deg, rgba(128, 95, 244, 0.05) 0%, rgba(128, 95, 244, 0.02) 100%);
}

:deep(.el-tabs__item:hover) {
  color: #805ff4 !important;
  background: rgba(128, 95, 244, 0.03);
}

/* 确保激活状态的下划线完全是紫色 */
:deep(.el-tabs__active-bar) {
  background-color: #805ff4 !important;
}

/* 覆盖Element Plus默认的激活指示器 */
:deep(.el-tabs__nav-wrap::after) {
  background-color: transparent !important;
}

/* 确保tab激活时的所有颜色都是紫色 */
:deep(.el-tabs__item.is-active::before),
:deep(.el-tabs__item.is-active::after) {
  background-color: #805ff4 !important;
  border-color: #805ff4 !important;
}

/* 排序选择框紫色主题 - 更强的选择器 */
.workflow-records-page :deep(.el-select) {
  --el-color-primary: #805ff4 !important;
  --el-color-primary-light-3: rgba(128, 95, 244, 0.3) !important;
  --el-color-primary-light-5: rgba(128, 95, 244, 0.5) !important;
  --el-color-primary-light-7: rgba(128, 95, 244, 0.7) !important;
  --el-color-primary-light-8: rgba(128, 95, 244, 0.8) !important;
  --el-color-primary-light-9: rgba(128, 95, 244, 0.9) !important;
}

.workflow-records-page :deep(.el-input__wrapper) {
  transition: all 0.2s ease;
}

.workflow-records-page :deep(.el-input__wrapper:hover) {
  border-color: #9370f4 !important;
}

.workflow-records-page :deep(.el-input__wrapper.is-focus) {
  border-color: #805ff4 !important;
  box-shadow: 0 0 0 2px rgba(128, 95, 244, 0.2) !important;
}

.workflow-records-page :deep(.el-input.is-focus .el-input__wrapper) {
  border-color: #805ff4 !important;
  box-shadow: 0 0 0 2px rgba(128, 95, 244, 0.2) !important;
}

/* 全局下拉选项样式覆盖 */
.el-select-dropdown .el-select-dropdown__item:hover {
  background-color: rgba(128, 95, 244, 0.1) !important;
  color: #805ff4 !important;
}

.el-select-dropdown .el-select-dropdown__item.selected {
  background-color: rgba(128, 95, 244, 0.15) !important;
  color: #805ff4 !important;
  font-weight: 600 !important;
}

.el-select-dropdown .el-select-dropdown__item.hover {
  background-color: rgba(128, 95, 244, 0.1) !important;
  color: #805ff4 !important;
}

/* 更强的选择器覆盖选中项文本颜色 */
:deep(.el-select-dropdown__item.is-selected) {
  color: #805ff4 !important;
  background-color: rgba(128, 95, 244, 0.15) !important;
  font-weight: 600 !important;
}

:deep(.el-select-dropdown__item.is-selected:hover) {
  color: #805ff4 !important;
  background-color: rgba(128, 95, 244, 0.2) !important;
}

/* 选择框输入框中显示的文本颜色 */
.workflow-records-page :deep(.el-input__inner) {
  color: #303133 !important;
}

.workflow-records-page :deep(.el-select .el-input.is-focus .el-input__inner) {
  color: #303133 !important;
}

/* 选择框图标颜色 */
.workflow-records-page :deep(.el-select .el-select__caret) {
  color: #a0a4a8;
  transition: color 0.2s ease;
}

.workflow-records-page :deep(.el-select:hover .el-select__caret) {
  color: #805ff4 !important;
}

.workflow-records-page :deep(.el-input.is-focus .el-select__caret) {
  color: #805ff4 !important;
}

:deep(.el-tabs__content) {
  padding: 0;
  min-height: 500px;
  border: none;
  border-radius: 0;
  background: white;
  overflow: hidden;
}

.tab-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-top: 1px solid #e8e8e8;
  border-bottom: 1px solid #e4e7ed;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.refresh-controls {
  display: flex;
  align-items: center;
}

.workflow-list-container {
  padding: 24px;
  background: #fafbfc;
}

/* 滚动条样式 */
.workflow-list-container::-webkit-scrollbar {
  width: 6px;
}

.workflow-list-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.workflow-list-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.workflow-list-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 终极解决方案：直接覆盖Element Plus主题色 */
.workflow-records-page {
  --el-color-primary: #805ff4;
  --el-color-primary-dark-2: #6d3ff0;
  --el-color-primary-light-3: #9370f4;
  --el-color-primary-light-5: #b59ef7;
  --el-color-primary-light-7: #d7ccfb;
  --el-color-primary-light-8: #e8dffc;
  --el-color-primary-light-9: #f3f1fe;
}

/* 强制覆盖所有可能的选择框下拉选项样式 */
.el-popper.is-pure .el-select-dropdown__item.is-selected,
.el-select-dropdown .el-select-dropdown__item.is-selected,
.el-select__popper .el-select-dropdown__item.is-selected {
  color: #805ff4 !important;
  background-color: rgba(128, 95, 244, 0.15) !important;
  font-weight: 600 !important;
}

.el-popper.is-pure .el-select-dropdown__item.is-selected:hover,
.el-select-dropdown .el-select-dropdown__item.is-selected:hover,
.el-select__popper .el-select-dropdown__item.is-selected:hover {
  color: #805ff4 !important;
  background-color: rgba(128, 95, 244, 0.2) !important;
}

@media (max-width: 768px) {
  .workflow-records-page {
    padding: 16px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .stat-content {
    gap: 12px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  :deep(.el-tabs__item) {
    height: 50px;
    line-height: 50px;
    font-size: 14px;
    padding: 0 16px !important;
    text-align: center !important;
  }
  
  .tab-controls {
    padding: 16px;
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .sort-controls {
    justify-content: space-between;
    gap: 8px;
  }
  
  .workflow-list-container {
    padding: 16px;
  }
}
</style>