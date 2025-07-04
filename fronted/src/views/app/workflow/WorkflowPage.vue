<template>
  <div class="workflow-page">
    <div class="workflow-header">
      <div class="workflow-progress">
        <div class="custom-steps-container">
          <div 
            v-for="(step, index) in steps" 
            :key="index"
            class="step-item"
            :class="getStepClass(index)"
          >
            <!-- 步骤节点 -->
            <div class="step-node">
              <div class="step-icon">
                <i v-if="getStepStatus(index) === 'completed'" class="step-check">✓</i>
                <span v-else-if="getStepStatus(index) === 'error'" class="step-error">✕</span>
                <span v-else class="step-number">{{ index + 1 }}</span>
              </div>
            </div>
            
            <!-- 连接线 -->
            <div 
              v-if="index < steps.length - 1" 
              class="step-line"
              :class="{ 'line-active': getLineStatus(index) === 'active' }"
            ></div>
            
            <!-- 步骤标题 -->
            <div class="step-title">{{ step }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="workflow-content">
      <!-- Loading overlay for in_progress status -->
      <div v-if="workflowData?.status === 'in_progress'" class="loading-overlay">
        <div class="loading-content">
          <div class="simple-spinner"></div>
          <div class="loading-text">{{ loadingText }}</div>
        </div>
      </div>

      <!-- Step 1: Keyword Input -->
      <WorkflowStep1 
        v-if="workflowData?.status !== 'in_progress' && currentStep === 1"
        :data="workflowData"
        :loading="isSubmitting" 
        @next="handleStep1Submit"
      />

      <!-- Step 2: Topic Selection (formerly Step 3) -->
      <WorkflowStep3 
        v-if="workflowData?.status !== 'in_progress' && currentStep === 2"
        :data="workflowData"
        :loading="isSubmitting"
        @next="handleStep3Submit"
      />

      <!-- Step 3: Title Selection (formerly Step 4) -->
      <WorkflowStep4 
        v-if="workflowData?.status !== 'in_progress' && currentStep === 3"
        :data="workflowData"
        :loading="isSubmitting"
        @next="handleStep4Submit"
      />

      <!-- Step 4: Outline Modification (formerly Step 5) -->
      <WorkflowStep5 
        v-if="workflowData?.status !== 'in_progress' && currentStep === 4"
        :data="workflowData"
        :loading="isSubmitting"
        @next="handleStep5Submit"
      />

      <!-- Step 5: Article Display (formerly Step 6) -->
      <WorkflowStep6 
        v-if="workflowData?.status !== 'in_progress' && currentStep === 5"
        :data="workflowData"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { generationApi } from '@/services/api/generation'
import type { WorkflowState } from '@/types/workflow'
import WorkflowStep1 from './components/WorkflowStep1.vue'
import WorkflowStep3 from './components/WorkflowStep3.vue'
import WorkflowStep4 from './components/WorkflowStep4.vue'
import WorkflowStep5 from './components/WorkflowStep5.vue'
import WorkflowStep6 from './components/WorkflowStep6.vue'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

// State
const workflowData = ref<WorkflowState | null>(null)
const currentStep = ref(1)
const isLoading = ref(false)
const loadingText = ref('正在处理中...')
const pollingTimer = ref<number | null>(null)
const isSubmitting = ref(false)
const expectedNextStep = ref<number | null>(null) // 记录期望的下一步

// 步骤数据 - 使用多语言翻译
const steps = computed(() => [
  t('workflow.steps.keyword_input'), 
  t('workflow.steps.topic_selection'), 
  t('workflow.steps.title_selection'), 
  t('workflow.steps.outline_editing'), 
  t('workflow.steps.article_generation')
])

// Methods
const determineCurrentStep = (workflow: any): number => {
  console.log('Determining current step for workflow:', workflow)
  
  const currentNodeIndex = workflow.current_step || 1
  const status = workflow.status
  
  if (status === 'completed') {
    // completed状态：进入current_node_index+1表单页面
    console.log(`Completed: showing form step ${currentNodeIndex + 1}`)
    return currentNodeIndex + 1
  } else if (status === 'failed') {
    // failed状态：渲染current_node_index表单页面
    console.log(`Failed: showing form step ${currentNodeIndex}`)
    return currentNodeIndex
  } else {
    // 其他情况（包括in_progress，但in_progress应该显示loading页面）
    console.log(`Other status (${status}): showing step ${currentNodeIndex}`)
    return currentNodeIndex
  }
}

const initializeWorkflow = async () => {
  const sessionId = route.params.sessionId as string
  
  // 清除期望步骤
  expectedNextStep.value = null
  
  if (sessionId && sessionId !== 'new') {
    // Load existing workflow
    await loadWorkflow(sessionId)
  } else {
    // Start new workflow
    currentStep.value = 1
    workflowData.value = null
  }
}

const loadWorkflow = async (sessionId: string) => {
  try {
    console.log('🔄 Setting isLoading to true at start of loadWorkflow')
    isLoading.value = true
    
    console.log('Loading workflow with session ID:', sessionId)
    
    // 直接获取完整的工作流数据
    try {
      const workflow = await generationApi.getWorkflowResult(sessionId)
      workflowData.value = workflow
      
      console.log('Loaded workflow data:', workflow)
      console.log('📊 Workflow status:', workflow.status)
      console.log('📊 Current step:', workflow.current_step)
      
      // 根据工作流状态决定下一步行为
      if (workflow.status === 'in_progress') {
        console.log('✅ Workflow is in progress, starting polling...')
        console.log('🔄 Keeping isLoading = true, setting loadingText')
        // 如果工作流正在进行中，设置加载状态并开始轮询
        loadingText.value = '工作流正在进行中...'
        currentStep.value = workflow.current_step || 1
        console.log('🚀 Starting polling with no delay')
        startPolling(sessionId, 0) // 无延迟，因为这是恢复现有的进行中工作流
        console.log('⚠️ NOT setting isLoading to false - letting polling control it')
        // 注意：这里不设置 isLoading.value = false，让轮询来控制加载状态
      } else if (workflow.status === 'failed') {
        console.log('❌ Workflow failed, showing current step for user to retry...')
        // 工作流失败，显示当前步骤供用户重新填写
        currentStep.value = determineCurrentStep(workflow)
        console.log('🔄 Setting isLoading to false for failed workflow')
        isLoading.value = false
        
        // 显示失败提示（如果有失败消息）
        if (workflow.failed_message) {
          ElMessage.error(workflow.failed_message)
        } else {
          ElMessage.error('工作流执行失败，请重新提交')
        }
      } else {
        // 工作流已完成，确定当前步骤
        console.log('✅ Workflow completed, determining current step...')
        currentStep.value = determineCurrentStep(workflow)
        console.log('🔄 Setting isLoading to false for completed workflow')
        isLoading.value = false
      }
    } catch (resultError: any) {
      // 如果获取完整数据失败，可能是工作流正在进行中，尝试status接口
      console.log('⚠️ Failed to get workflow result, trying status check:', resultError)
      
      try {
        const statusResponse = await generationApi.getWorkflowStatus(sessionId)
        console.log('Status check result:', statusResponse.workflow)
        workflowData.value = statusResponse.workflow
        console.log('📊 Status response - status:', statusResponse.workflow.status)
        
        if (statusResponse.workflow.status === 'in_progress') {
          console.log('✅ Status shows in_progress, starting polling...')
          console.log('🔄 Keeping isLoading = true, setting loadingText from status')
          loadingText.value = statusResponse.workflow.loading_text || '工作流正在进行中...'
          currentStep.value = statusResponse.workflow.current_step || 1
          console.log('🚀 Starting polling with no delay (fallback)')
          startPolling(sessionId, 0) // 无延迟，因为这是fallback恢复现有工作流
          console.log('⚠️ NOT setting isLoading to false - letting polling control it (fallback)')
        } else {
          // 如果status接口显示非进行中，但result接口失败，说明有问题
          console.log('❌ Status not in_progress but result failed')
          console.log('🔄 Setting isLoading to false due to error')
          isLoading.value = false
          throw resultError
        }
      } catch (statusError: any) {
        // 两个接口都失败了
        console.error('Both result and status APIs failed')
        console.log('🔄 Setting isLoading to false due to both APIs failing')
        throw statusError
      }
    }
    
  } catch (error: any) {
    console.error('Failed to load workflow:', error)
    console.log('🔄 Setting isLoading to false due to catch block')
    ElMessage.error(error.message || '加载工作流失败')
    isLoading.value = false
  }
}

const startPolling = (sessionId: string, delayMs: number = 3000) => {
  const poll = async () => {
    try {
      console.log('🔄 Polling - making API call...')
      const response = await generationApi.getWorkflowStatus(sessionId, true)
      
      console.log('Polling response:', response)
      console.log('📊 Polling - workflow status:', response.workflow.status)
      console.log('📊 Polling - current step:', response.workflow.current_step)
      console.log('Gen search intent:', response.workflow.gen_search_intent)
      
      if (response.workflow.status === 'in_progress') {
        console.log('✅ Polling - workflow still in progress')
        // 更新加载文案和工作流数据
        loadingText.value = response.workflow.loading_text || '正在处理中...'
        workflowData.value = response.workflow
        currentStep.value = response.workflow.current_step || 1
        
        console.log('Polling - workflow still in progress')
        console.log('Loading text:', loadingText.value)
        console.log('Current step:', currentStep.value)
        console.log('🔄 Polling - current isLoading value:', isLoading.value)
        
        // 确保加载状态保持开启，重置提交状态
        if (!isLoading.value) {
          console.log('🔄 Polling - isLoading was false, setting to true')
          isLoading.value = true
        } else {
          console.log('✅ Polling - isLoading already true, keeping it')
        }
        isSubmitting.value = false
        
        // Continue polling
        console.log('🔄 Polling - scheduling next poll in 2 seconds')
        pollingTimer.value = window.setTimeout(poll, 2000)
      } else {
        // Workflow completed or failed - 获取完整数据
        console.log('✅ Polling - workflow completed/failed, fetching complete data...')
        console.log('🔄 Polling - will set isLoading to false after processing')
        
        try {
          // 获取完整的工作流数据而不是status接口的简化数据
          const completeWorkflow = await generationApi.getWorkflowResult(response.workflow.session_id)
          workflowData.value = completeWorkflow
          
          console.log('Complete workflow data loaded:', completeWorkflow)
          
          // 如果有期望的下一步，优先使用期望的步骤
          if (expectedNextStep.value !== null) {
            console.log('Using expected next step:', expectedNextStep.value)
            currentStep.value = expectedNextStep.value
            expectedNextStep.value = null // 清除期望步骤
          } else {
            // 根据工作流状态和数据确定当前应该显示的步骤
            currentStep.value = determineCurrentStep(completeWorkflow)
          }
        } catch (error) {
          console.error('Failed to fetch complete workflow data:', error)
          // 如果获取完整数据失败，使用status接口的数据
          workflowData.value = response.workflow
          if (expectedNextStep.value !== null) {
            console.log('Using expected next step (fallback):', expectedNextStep.value)
            currentStep.value = expectedNextStep.value
            expectedNextStep.value = null
          } else {
            currentStep.value = determineCurrentStep(response.workflow)
          }
        }
        
        console.log('🔄 Polling - setting isLoading to false (workflow completed/failed)')
        isLoading.value = false
        isSubmitting.value = false
        
        if (response.workflow.status === 'failed') {
          ElMessage.error('工作流执行失败，请重试')
        } else if (response.workflow.status === 'completed') {
          // 根据当前步骤显示不同的成功消息
          const step = currentStep.value
          const stepMessages = {
            2: '主题创意生成完成，请选择您喜欢的主题',
            3: '文章标题生成完成，请选择合适的标题',
            4: '文章大纲生成完成，请检查并修改大纲',
            5: '文章生成完成！'
          }
          const msg = stepMessages[step as keyof typeof stepMessages]
          if (msg) {
            ElMessage.success(msg)
          }
        }
      }
    } catch (error: any) {
      console.error('❌ Polling error:', error)
      
      // 检查是否是400错误（工作流失败）
      if (error.response?.status === 400) {
        console.log('❌ Workflow failed with 400 error')
        
        // 停止轮询
        console.log('🔄 Polling error - setting isLoading to false due to 400 error')
        isLoading.value = false
        isSubmitting.value = false
        
        // 提取错误消息并显示
        const errorMessage = error.response?.data?.message || '工作流执行失败'
        ElMessage.error(errorMessage)
        
        // 尝试获取失败的工作流数据以显示当前步骤
        try {
          const sessionId = route.params.sessionId as string
          const failedWorkflow = await generationApi.getWorkflowResult(sessionId)
          workflowData.value = failedWorkflow
          currentStep.value = determineCurrentStep(failedWorkflow)
        } catch (fetchError) {
          console.error('Failed to fetch failed workflow data:', fetchError)
          // 如果无法获取数据，保持当前状态
        }
        
        return // 不再重试轮询
      }
      
      // 对于其他错误，继续重试
      console.log('🔄 Polling error - retrying in 5 seconds')
      pollingTimer.value = window.setTimeout(poll, 5000)
    }
  }
  
  console.log('🚀 startPolling called with sessionId:', sessionId, 'delay:', delayMs)
  console.log('🔄 startPolling - setting isLoading to true')
  isLoading.value = true
  isSubmitting.value = false
  
  // 延迟开始轮询，给后端时间更新状态
  console.log(`⏳ Delaying polling for ${delayMs}ms to allow backend status update`)
  pollingTimer.value = window.setTimeout(() => {
    console.log('🚀 Starting delayed polling')
    poll()
  }, delayMs)
}

const stopPolling = () => {
  if (pollingTimer.value) {
    clearTimeout(pollingTimer.value)
    pollingTimer.value = null
  }
  isLoading.value = false
  isSubmitting.value = false
  expectedNextStep.value = null // 清除期望步骤
}

// Step handlers
const handleStep1Submit = async (data: any) => {
  try {
    isSubmitting.value = true
    
    console.log('Step 1 submit - route sessionId:', route.params.sessionId)
    console.log('Step 1 submit - workflowData:', workflowData.value)
    console.log('Step 1 submit - data:', data)
    
    let sessionId: string
    
    // 检查是否是新建工作流还是重新提交失败的工作流
    if (route.params.sessionId === 'new' || !workflowData.value) {
      // 新建工作流
      console.log('Creating new workflow')
      const response = await generationApi.startWorkflow(data)
      sessionId = response.session_id
      
      // Update URL to include session ID
      router.replace(`/app/workflow/${sessionId}`)
    } else {
      // 重新提交失败的工作流
      console.log('Continuing existing workflow with session:', workflowData.value.session_id)
      
      const nodeInput = {
        keyword: data.keyword,
        target_market: data.target_market,
        article_language: data.article_language
      }
      
      console.log('Calling continueWorkflow with:', nodeInput)
      const response = await generationApi.continueWorkflow(workflowData.value.session_id, nodeInput)
      console.log('continueWorkflow response:', response)
      
      sessionId = workflowData.value.session_id
    }
    
    // Set expected next step (跳过原Step2，直接到Step3，现在是Step2)
    expectedNextStep.value = 2
    
    // Set loading state and start polling for results
    isLoading.value = true
    loadingText.value = '正在生成主题创意...'
    console.log('Starting polling for session:', sessionId)
    startPolling(sessionId) // 使用默认延迟3秒
    
  } catch (error: any) {
    console.error('Step 1 submit error:', error)
    
    // 特殊处理400状态码错误
    if (error.response && error.response.status === 400) {
      const errorMessage = error.response.data?.message || error.message || '请求参数错误'
      
      // 特殊处理额度不足的错误消息
      const displayMessage = errorMessage === '该用户额度不足' ? '您的使用额度不足' : errorMessage
      
      ElMessage.error(displayMessage)
    } else {
      // 其他错误使用原有逻辑
      ElMessage.error(error.message || '启动工作流失败')
    }
    
    isSubmitting.value = false
    expectedNextStep.value = null
  }
}

const handleStep3Submit = async (data: any) => {
  if (!workflowData.value) return
  
  try {
    isSubmitting.value = true
    
    console.log('Step 3 submit - workflow status:', workflowData.value.status)
    console.log('Step 3 submit - session ID:', workflowData.value.session_id)
    console.log('Step 3 submit - data:', data)
    
    const nodeInput = {
      chosen_topic: data.chosen_topic,
      background_information: data.background_information || '',
      title_generation_demands: data.title_generation_demands || ''
    }
    
    console.log('Calling continueWorkflow with:', nodeInput)
    const response = await generationApi.continueWorkflow(workflowData.value.session_id, nodeInput)
    console.log('continueWorkflow response:', response)
    
    // Set expected next step
    expectedNextStep.value = 3
    
    // Set loading state and start polling
    isLoading.value = true
    loadingText.value = '正在生成深度研究报告和文章标题...'
    console.log('Starting polling for session:', workflowData.value.session_id)
    startPolling(workflowData.value.session_id) // 使用默认延迟3秒
    
  } catch (error: any) {
    console.error('Step 3 submit error:', error)
    
    // 特殊处理400状态码错误
    if (error.response && error.response.status === 400) {
      const errorMessage = error.response.data?.message || error.message || '请求参数错误'
      
      // 特殊处理额度不足的错误消息
      const displayMessage = errorMessage === '该用户额度不足' ? '您的使用额度不足' : errorMessage
      
      ElMessage.error(displayMessage)
    } else {
      // 其他错误使用原有逻辑
      ElMessage.error(error.message || '提交失败')
    }
    
    isSubmitting.value = false
    expectedNextStep.value = null
  }
}

const handleStep4Submit = async (data: any) => {
  if (!workflowData.value) return
  
  try {
    isSubmitting.value = true
    
    console.log('Step 4 submit - workflow status:', workflowData.value.status)
    console.log('Step 4 submit - session ID:', workflowData.value.session_id)
    console.log('Step 4 submit - data:', data)
    
    const nodeInput = {
      article_title: data.article_title,
      secondary_keywords: data.secondary_keywords || '',
      outline_demand: data.outline_demand || '',
      additional_knowledge_points: data.additional_knowledge_points || ''
    }
    
    console.log('Calling continueWorkflow with:', nodeInput)
    const response = await generationApi.continueWorkflow(workflowData.value.session_id, nodeInput)
    console.log('continueWorkflow response:', response)
    
    // Set expected next step
    expectedNextStep.value = 4
    
    // Set loading state and start polling
    isLoading.value = true
    loadingText.value = '正在生成文章大纲...'
    console.log('Starting polling for session:', workflowData.value.session_id)
    startPolling(workflowData.value.session_id) // 使用默认延迟3秒
    
  } catch (error: any) {
    console.error('Step 4 submit error:', error)
    
    // 特殊处理400状态码错误
    if (error.response && error.response.status === 400) {
      const errorMessage = error.response.data?.message || error.message || '请求参数错误'
      
      // 特殊处理额度不足的错误消息
      const displayMessage = errorMessage === '该用户额度不足' ? '您的使用额度不足' : errorMessage
      
      ElMessage.error(displayMessage)
    } else {
      // 其他错误使用原有逻辑
      ElMessage.error(error.message || '提交失败')
    }
    
    isSubmitting.value = false
    expectedNextStep.value = null
  }
}

const handleStep5Submit = async (data: any) => {
  if (!workflowData.value) return
  
  try {
    isSubmitting.value = true
    
    console.log('Step 5 submit - workflow status:', workflowData.value.status)
    console.log('Step 5 submit - session ID:', workflowData.value.session_id)
    console.log('Step 5 submit - data:', data)
    
    const nodeInput = {
      article_outline: data.article_outline,
      narrative_perspective: data.narrative_perspective,
      main_image_option: data.main_image_option,
      sub_images_option: data.sub_images_option
    }
    
    console.log('Calling continueWorkflow with:', nodeInput)
    const response = await generationApi.continueWorkflow(workflowData.value.session_id, nodeInput)
    console.log('continueWorkflow response:', response)
    
    // Set expected next step
    expectedNextStep.value = 5
    
    // Set loading state and start polling
    isLoading.value = true
    loadingText.value = '正在生成文章草稿、图片和最终文章...'
    console.log('Starting polling for session:', workflowData.value.session_id)
    startPolling(workflowData.value.session_id) // 使用默认延迟3秒
    
  } catch (error: any) {
    console.error('Step 5 submit error:', error)
    
    // 特殊处理400状态码错误
    if (error.response && error.response.status === 400) {
      const errorMessage = error.response.data?.message || error.message || '请求参数错误'
      
      // 特殊处理额度不足的错误消息
      const displayMessage = errorMessage === '该用户额度不足' ? '您的使用额度不足' : errorMessage
      
      ElMessage.error(displayMessage)
    } else {
      // 其他错误使用原有逻辑
      ElMessage.error(error.message || '提交失败')
    }
    
    isSubmitting.value = false
    expectedNextStep.value = null
  }
}

// 获取步骤状态
const getStepStatus = (stepIndex: number) => {
  if (!workflowData.value) {
    // 没有数据时，第一个步骤为当前状态，其他为等待状态
    return stepIndex === 0 ? 'current' : 'pending'
  }
  
  const currentNodeIndex = workflowData.value.current_step || 1
  const status = workflowData.value.status
  
  if (status === 'completed') {
    // completed状态：current_node_index及之前的为完成，current_node_index+1为当前，之后为等待
    if (stepIndex < currentNodeIndex) {
      return 'completed' // 紫色填充+打勾
    } else if (stepIndex === currentNodeIndex) {
      return 'current' // 紫色描边
    } else {
      return 'pending' // 灰色
    }
  } else if (status === 'in_progress') {
    // in_progress状态：current_node_index及之前的为完成，之后为等待
    if (stepIndex < currentNodeIndex) {
      return 'completed' // 紫色填充+打勾
    } else {
      return 'pending' // 灰色
    }
  } else if (status === 'failed') {
    // failed状态：current_node_index之前的为完成，current_node_index为错误，之后为等待
    if (stepIndex < currentNodeIndex - 1) {
      return 'completed' // 紫色填充+打勾
    } else if (stepIndex === currentNodeIndex - 1) {
      return 'error' // 红色描边
    } else {
      return 'pending' // 灰色
    }
  }
  
  // 默认情况
  return stepIndex === 0 ? 'current' : 'pending'
}

// 获取连接线状态
const getLineStatus = (lineIndex: number) => {
  if (!workflowData.value) {
    return 'inactive'
  }
  
  const currentNodeIndex = workflowData.value.current_step || 1
  const status = workflowData.value.status
  
  // 连接线激活的条件：前面的step-node不是灰色状态
  if (status === 'completed') {
    // lineIndex表示第几条连接线（0-3），连接第lineIndex和lineIndex+1个节点
    return lineIndex < currentNodeIndex ? 'active' : 'inactive'
  } else if (status === 'in_progress') {
    return lineIndex < currentNodeIndex - 1 ? 'active' : 'inactive'
  } else if (status === 'failed') {
    return lineIndex < currentNodeIndex - 1 ? 'active' : 'inactive'
  }
  
  return 'inactive'
}

// 获取步骤CSS类
const getStepClass = (stepIndex: number) => {
  const status = getStepStatus(stepIndex)
  return {
    'step-completed': status === 'completed',
    'step-current': status === 'current',
    'step-error': status === 'error',
    'step-pending': status === 'pending'
  }
}

// Lifecycle
onMounted(() => {
  initializeWorkflow()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style>
.workflow-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

.workflow-header {
  margin-bottom: 32px;
  text-align: center;
}

.workflow-progress {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 0;
}

/* 自定义步骤条样式 */
.custom-steps-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  position: relative;
  width: 100%;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

/* 步骤节点 */
.step-node {
  position: relative;
  z-index: 2;
  margin-bottom: 16px;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  border: 3px solid;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

/* 步骤标题 */
.step-title {
  font-size: 16px;
  font-weight: 500;
  color: #606266;
  text-align: center;
  line-height: 1.4;
  max-width: 120px;
}

/* 连接线 */
.step-line {
  position: absolute;
  top: 20px;
  left: 50%;
  right: -50%;
  height: 4px;
  z-index: 1;
  border-radius: 2px;
  background: #e4e7ed;
  transition: all 0.3s ease;
}

/* 激活的连接线 - 流光紫色 */
.step-line.line-active {
  background: linear-gradient(90deg, 
    #805ff4 0%, 
    #8b5cf6 25%,
    #9333ea 50%,
    #8b5cf6 75%,
    #805ff4 100%
  );
  background-size: 200% 100%;
  animation: line-flow 3s ease-in-out infinite;
}

@keyframes line-flow {
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

/* 已完成状态 - 紫色填充+打勾 */
.step-completed .step-icon {
  background: #805ff4;
  border-color: #805ff4;
  color: white;
}

.step-completed .step-title {
  color: #805ff4;
  font-weight: 600;
}

/* 当前进行中状态 - 紫色描边 */
.step-current .step-icon {
  background: white;
  border-color: #805ff4;
  color: #805ff4;
}

.step-current .step-title {
  color: #805ff4;
  font-weight: 600;
}

/* 错误状态 - 红色描边 */
.step-error .step-icon {
  background: white;
  border-color: #f56c6c;
  color: #f56c6c;
}

.step-error .step-title {
  color: #f56c6c;
  font-weight: 600;
}

/* 等待状态 - 灰色 */
.step-pending .step-icon {
  background: #f5f7fa;
  border-color: #dcdfe6;
  color: #c0c4cc;
}

.step-pending .step-title {
  color: #c0c4cc;
}

/* 特殊样式调整 */
.step-check {
  font-style: normal;
  font-size: 20px;
  font-weight: bold;
}

.step-error {
  font-size: 20px;
  font-weight: bold;
}

.step-number {
  font-size: 16px;
  font-weight: 600;
}

.workflow-content {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  min-height: 500px;
  max-height: none;
  overflow: visible;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  z-index: 100;
  backdrop-filter: blur(2px);
}

.loading-content {
  padding: 30px;
  background: white;
  border-radius: 12px;
  text-align: center;
  min-width: 300px;
}

.simple-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #805ff4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #606266;
  font-weight: 500;
  text-align: center;
}

@media (max-width: 768px) {
  .workflow-page {
    padding: 16px;
  }
  
  .workflow-content {
    padding: 20px;
  }
  
  .step-icon {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
  
  .step-title {
    font-size: 14px;
    max-width: 100px;
  }
  
  .step-line {
    top: 16px;
  }
}
</style>