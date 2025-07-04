<template>
  <div class="test-loading-page">
    <div class="test-container">
      <h1>LoadingModal 测试页面</h1>
      <div class="test-buttons">
        <a-button 
          type="primary" 
          @click="testBasicLoading"
          :loading="isBasicLoading"
        >
          测试基础加载动画
        </a-button>
        
        <a-button 
          type="primary" 
          @click="testAdvancedLoading"
          :loading="isAdvancedLoading"
        >
          测试极客风格加载动画
        </a-button>
        
        <a-button 
          type="default" 
          @click="testProgressLoading"
        >
          测试进度加载动画
        </a-button>
      </div>
    </div>
    
    <!-- 极客风格加载动画 -->
    <LoadingModal
      :visible="showAdvancedModal"
      :progress="progress"
      :current-step="currentStep"
      :show-progress="showProgress"
      type="analysis"
      :config="loadingConfig"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import { SearchOutlined, BulbOutlined, CheckCircleOutlined } from '@ant-design/icons-vue'
import LoadingModal from '@/components/common/LoadingModal.vue'

// 基础状态
const isBasicLoading = ref(false)
const isAdvancedLoading = ref(false)

// 极客风格动画状态
const showAdvancedModal = ref(false)
const progress = ref(0)
const currentStep = ref(1)
const showProgress = ref(true)

// 极客风格加载配置
const loadingConfig = computed(() => ({
  title: '🧠 AI智能分析测试',
  steps: [
    { title: '关键词解析', description: '分析关键词搜索意图和竞争度', icon: SearchOutlined },
    { title: '市场洞察', description: '收集目标市场相关数据', icon: BulbOutlined },
    { title: '策略生成', description: '制定内容创作策略', icon: CheckCircleOutlined }
  ],
  messages: [
    '🔍 正在深度分析关键词语义...',
    '📊 检索相关市场数据中...',
    '🎯 识别目标受众特征...',
    '🚀 生成内容创作建议...',
    '✨ 优化SEO策略参数...'
  ]
}))

// 测试基础加载
const testBasicLoading = () => {
  isBasicLoading.value = true
  message.loading('测试基础加载动画...', 3)
  
  setTimeout(() => {
    isBasicLoading.value = false
    message.success('基础加载动画测试完成！')
  }, 3000)
}

// 测试极客风格加载
const testAdvancedLoading = () => {
  isAdvancedLoading.value = true
  showAdvancedModal.value = true
  progress.value = 0
  currentStep.value = 1
  
  // 模拟进度变化
  const progressSteps = [
    { progress: 20, step: 1, delay: 500 },
    { progress: 45, step: 2, delay: 1500 },
    { progress: 70, step: 2, delay: 2500 },
    { progress: 95, step: 3, delay: 3500 },
    { progress: 100, step: 3, delay: 4500 }
  ]
  
  progressSteps.forEach(({ progress: p, step, delay }) => {
    setTimeout(() => {
      if (showAdvancedModal.value) {
        progress.value = p
        currentStep.value = step
      }
    }, delay)
  })
  
  // 5秒后关闭
  setTimeout(() => {
    showAdvancedModal.value = false
    isAdvancedLoading.value = false
    message.success('🎉 极客风格加载动画测试完成！')
  }, 5000)
}

// 测试进度加载
const testProgressLoading = () => {
  showAdvancedModal.value = true
  progress.value = 0
  currentStep.value = 1
  showProgress.value = true
  
  // 持续进度动画
  const interval = setInterval(() => {
    if (progress.value < 100) {
      progress.value += 10
      if (progress.value >= 33 && currentStep.value === 1) {
        currentStep.value = 2
      } else if (progress.value >= 66 && currentStep.value === 2) {
        currentStep.value = 3
      }
    } else {
      clearInterval(interval)
      setTimeout(() => {
        showAdvancedModal.value = false
        message.success('✅ 进度加载动画测试完成！')
      }, 1000)
    }
  }, 300)
}
</script>

<style scoped>
.test-loading-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.test-container {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.test-container h1 {
  margin-bottom: 32px;
  color: #333;
  font-size: 24px;
  font-weight: 700;
}

.test-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.test-buttons .ant-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}
</style>