<template>
  <a-modal
    :open="visible"
    :closable="false"
    :maskClosable="false"
    :footer="null"
    :width="800"
    centered
    wrap-class-name="loading-modal-wrapper"
    class="geek-loading-modal"
  >
    <div class="loading-container">
      <!-- Holographic Background -->
      <div class="holographic-bg">
        <div class="grid-lines"></div>
        <div class="energy-rings">
          <div class="ring ring-1"></div>
          <div class="ring ring-2"></div>
          <div class="ring ring-3"></div>
        </div>
        <div class="particles"></div>
      </div>

      <!-- Main Content -->
      <div class="loading-content">
        <!-- Title Section -->
        <div class="loading-header">
          <div class="title-container">
            <div class="neural-icon">
              <div class="neural-core"></div>
              <div class="neural-pulse"></div>
            </div>
            <h3 class="loading-title">{{ currentTitle }}</h3>
          </div>
          <div class="system-status">
            <span class="status-indicator" :class="statusClass"></span>
            <span class="status-text">{{ statusText }}</span>
          </div>
        </div>

        <!-- Progress Section -->
        <div class="progress-section" v-if="showProgress">
          <div class="progress-info">
            <span class="current-step">步骤 {{ currentStep }}</span>
            <span class="progress-percentage">{{ Math.round(progress) }}%</span>
          </div>
          
          <!-- Holographic Progress Bar -->
          <div class="progress-container">
            <div class="progress-track">
              <div 
                class="progress-fill"
                :style="{ width: `${progress}%` }"
              ></div>
              <div class="progress-glow"></div>
            </div>
          </div>
        </div>

        <!-- Workflow Steps -->
        <div class="workflow-steps" v-if="workflowSteps.length > 0">
          <div 
            v-for="(step, index) in workflowSteps" 
            :key="index"
            class="workflow-step"
            :class="{
              'active': index + 1 === currentStep,
              'completed': index + 1 < currentStep,
              'pending': index + 1 > currentStep
            }"
          >
            <div class="step-connector" v-if="index > 0"></div>
            <div class="step-node">
              <div class="node-inner">
                <div class="node-icon">
                  <component :is="step.icon" v-if="index + 1 <= currentStep" />
                  <div v-else class="pending-dot"></div>
                </div>
              </div>
              <div class="node-glow"></div>
            </div>
            <div class="step-info">
              <div class="step-title">{{ step.title }}</div>
              <div class="step-description">{{ step.description }}</div>
            </div>
          </div>
        </div>

        <!-- Neural Network Animation -->
        <div class="neural-network">
          <svg class="network-svg" viewBox="0 0 400 100">
            <defs>
              <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#6366f1;stop-opacity:0" />
                <stop offset="50%" style="stop-color:#6366f1;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:0" />
              </linearGradient>
            </defs>
            
            <!-- Animated connecting lines -->
            <g class="connection-lines">
              <path 
                v-for="(path, index) in networkPaths" 
                :key="index"
                :d="path.d"
                class="network-path"
                :style="{ animationDelay: `${index * 0.2}s` }"
              />
            </g>
            
            <!-- Network nodes -->
            <g class="network-nodes">
              <circle 
                v-for="(node, index) in networkNodes" 
                :key="index"
                :cx="node.x"
                :cy="node.y"
                :r="node.r"
                class="network-node"
                :class="{ active: node.active }"
                :style="{ animationDelay: `${index * 0.1}s` }"
              />
            </g>
          </svg>
        </div>

        <!-- Loading Message -->
        <div class="loading-message">
          <div class="message-container">
            <div class="terminal-cursor"></div>
            <span class="message-text">{{ currentMessage }}</span>
          </div>
        </div>
      </div>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { 
  SearchOutlined, 
  BulbOutlined, 
  FileTextOutlined, 
  EditOutlined,
  CheckCircleOutlined,
  ThunderboltOutlined 
} from '@ant-design/icons-vue'

interface LoadingConfig {
  title: string
  steps?: Array<{
    title: string
    description: string
    icon: any
  }>
  messages?: string[]
}

interface Props {
  visible: boolean
  progress?: number
  currentStep?: number
  showProgress?: boolean
  type?: 'analysis' | 'topics' | 'titles' | 'outline' | 'article' | 'optimization' | 'custom'
  title?: string
  subtitle?: string
  statusMessages?: string[]
  iconType?: string
  config?: LoadingConfig
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  progress: 0,
  currentStep: 1,
  showProgress: false,
  type: 'custom',
  title: '',
  subtitle: '',
  statusMessages: () => [],
  iconType: '',
  config: () => ({
    title: 'AI 处理中...',
    steps: []
  })
})

// LoadingModal不需要emit事件，因为它是只读显示的

// Default workflow configurations
const defaultWorkflowSteps = {
  analysis: [
    { title: '关键词分析', description: '正在分析搜索意图', icon: SearchOutlined },
    { title: '数据收集', description: '收集相关信息', icon: BulbOutlined },
    { title: '结果准备', description: '准备分析结果', icon: CheckCircleOutlined }
  ],
  topics: [
    { title: '市场分析', description: '分析目标市场', icon: SearchOutlined },
    { title: '主题生成', description: '生成文章主题', icon: BulbOutlined },
    { title: '主题筛选', description: '筛选最佳主题', icon: CheckCircleOutlined }
  ],
  titles: [
    { title: '关键词优化', description: '优化SEO关键词', icon: SearchOutlined },
    { title: '标题生成', description: '生成多个标题', icon: EditOutlined },
    { title: '标题评分', description: '评估标题质量', icon: CheckCircleOutlined }
  ],
  outline: [
    { title: '结构规划', description: '规划文章结构', icon: FileTextOutlined },
    { title: '大纲生成', description: '生成详细大纲', icon: EditOutlined },
    { title: '内容优化', description: '优化大纲内容', icon: CheckCircleOutlined }
  ],
  article: [
    { title: '内容生成', description: '生成文章内容', icon: EditOutlined },
    { title: '文本优化', description: '优化文章质量', icon: ThunderboltOutlined },
    { title: '最终检查', description: '检查文章完整性', icon: CheckCircleOutlined }
  ],
  optimization: [
    { title: 'SEO分析', description: '分析SEO优化点', icon: SearchOutlined },
    { title: '内容优化', description: '优化文章内容', icon: ThunderboltOutlined },
    { title: '最终完成', description: '完成所有优化', icon: CheckCircleOutlined }
  ]
}

// Reactive computed properties
const statusClass = computed(() => {
  if (props.progress >= 100) return 'completed'
  if (props.progress > 0) return 'processing'
  return 'initializing'
})

const statusText = computed(() => {
  if (props.progress >= 100) return '处理完成'
  if (props.progress > 0) return '正在处理'
  return '初始化中'
})

const currentTitle = computed(() => {
  if (props.config?.title) return props.config.title
  if (props.title) return props.title
  
  const titleMap = {
    analysis: '智能分析中',
    topics: '主题生成中',
    titles: '标题创作中',
    outline: '大纲构建中',
    article: '文章生成中',
    optimization: 'SEO优化中'
  }
  
  return titleMap[props.type as keyof typeof titleMap] || 'AI处理中...'
})

const workflowSteps = computed(() => {
  if (props.config?.steps && props.config.steps.length > 0) {
    return props.config.steps
  }
  
  return defaultWorkflowSteps[props.type as keyof typeof defaultWorkflowSteps] || []
})

// Loading messages cycling
const currentMessage = ref('')
const messageIndex = ref(0)
const messages = computed(() => {
  if (props.config?.messages && props.config.messages.length > 0) {
    return props.config.messages
  }
  
  if (props.statusMessages.length > 0) {
    return props.statusMessages
  }
  
  const messageMap = {
    analysis: ['正在分析关键词...', '处理搜索意图...', '收集相关数据...', '准备分析结果...'],
    topics: ['分析市场趋势...', '识别热门话题...', '生成主题建议...', '排序主题优先级...'],
    titles: ['分析关键词密度...', '优化SEO效果...', '创建标题变体...', '评估标题质量...'],
    outline: ['构建内容结构...', '组织章节逻辑...', '规划内容流程...', '完善大纲细节...'],
    article: ['撰写文章开头...', '发展主要内容...', '添加细节描述...', '润色文章文本...'],
    optimization: ['分析内容质量...', '检查SEO要素...', '提升可读性...', '完成最终优化...']
  }
  
  return messageMap[props.type as keyof typeof messageMap] || [
    '正在处理请求...',
    '分析数据中...',
    '生成内容中...',
    '即将完成...'
  ]
})

// Neural network animation data
const networkNodes = ref([
  { x: 50, y: 30, r: 4, active: false },
  { x: 120, y: 20, r: 3, active: false },
  { x: 120, y: 50, r: 3, active: false },
  { x: 120, y: 80, r: 3, active: false },
  { x: 200, y: 35, r: 4, active: false },
  { x: 200, y: 65, r: 4, active: false },
  { x: 280, y: 25, r: 3, active: false },
  { x: 280, y: 75, r: 3, active: false },
  { x: 350, y: 50, r: 4, active: false }
])

const networkPaths = ref([
  { d: 'M50,30 Q85,15 120,20' },
  { d: 'M50,30 Q85,40 120,50' },
  { d: 'M50,30 Q85,65 120,80' },
  { d: 'M120,20 Q160,27 200,35' },
  { d: 'M120,50 Q160,42 200,35' },
  { d: 'M120,50 Q160,58 200,65' },
  { d: 'M120,80 Q160,73 200,65' },
  { d: 'M200,35 Q240,30 280,25' },
  { d: 'M200,35 Q275,42 350,50' },
  { d: 'M200,65 Q240,70 280,75' },
  { d: 'M200,65 Q275,58 350,50' },
  { d: 'M280,25 Q315,37 350,50' },
  { d: 'M280,75 Q315,63 350,50' }
])

// Animation intervals
let messageInterval: number
let nodeActivationInterval: number

// Message cycling
const cycleMessages = () => {
  messageIndex.value = (messageIndex.value + 1) % messages.value.length
  currentMessage.value = messages.value[messageIndex.value]
}

// Neural network node activation
const activateRandomNode = () => {
  const randomIndex = Math.floor(Math.random() * networkNodes.value.length)
  networkNodes.value[randomIndex].active = true
  
  setTimeout(() => {
    networkNodes.value[randomIndex].active = false
  }, 1000)
}

// Lifecycle hooks
onMounted(() => {
  currentMessage.value = messages.value[0]
  
  // Start message cycling
  messageInterval = window.setInterval(cycleMessages, 2000)
  
  // Start neural network animation
  nodeActivationInterval = window.setInterval(activateRandomNode, 800)
})

onUnmounted(() => {
  if (messageInterval) clearInterval(messageInterval)
  if (nodeActivationInterval) clearInterval(nodeActivationInterval)
})

// Watch for visibility changes
watch(() => props.visible, (newVal) => {
  if (newVal) {
    // Reset animations when modal opens
    currentMessage.value = messages.value[0]
    messageIndex.value = 0
  }
})
</script>

<style scoped>
/* Modal wrapper */
:deep(.loading-modal-wrapper .ant-modal) {
  background: transparent;
  box-shadow: none;
}

:deep(.loading-modal-wrapper .ant-modal-content) {
  background: transparent;
  box-shadow: none;
  padding: 0;
}

:deep(.loading-modal-wrapper .ant-modal-body) {
  padding: 0;
}

/* Main container */
.loading-container {
  position: relative;
  padding: 40px;
  min-height: 500px;
  background: linear-gradient(135deg, 
    rgba(15, 15, 35, 0.95) 0%, 
    rgba(26, 29, 35, 0.95) 50%,
    rgba(45, 55, 72, 0.95) 100%
  );
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

/* Holographic background */
.holographic-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(99, 102, 241, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 102, 241, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(30px, 30px) rotate(360deg); }
}

.energy-rings {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  border: 2px solid;
  border-radius: 50%;
  animation: ringPulse 3s ease-in-out infinite;
}

.ring-1 {
  width: 200px;
  height: 200px;
  margin: -100px 0 0 -100px;
  border-color: rgba(99, 102, 241, 0.3);
  animation-delay: 0s;
}

.ring-2 {
  width: 300px;
  height: 300px;
  margin: -150px 0 0 -150px;
  border-color: rgba(236, 72, 153, 0.2);
  animation-delay: 1s;
}

.ring-3 {
  width: 400px;
  height: 400px;
  margin: -200px 0 0 -200px;
  border-color: rgba(6, 182, 212, 0.1);
  animation-delay: 2s;
}

@keyframes ringPulse {
  0%, 100% { 
    transform: scale(0.8);
    opacity: 0.3;
  }
  50% { 
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(99, 102, 241, 0.4), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(236, 72, 153, 0.3), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(6, 182, 212, 0.3), transparent);
  background-size: 150px 150px;
  animation: particleFloat 15s linear infinite;
}

@keyframes particleFloat {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-150px, -150px); }
}

/* Loading content */
.loading-content {
  position: relative;
  z-index: 1;
}

/* Header section */
.loading-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.title-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.neural-icon {
  position: relative;
  width: 48px;
  height: 48px;
}

.neural-core {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: coreRotate 3s linear infinite;
}

.neural-pulse {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 2px solid rgba(99, 102, 241, 0.5);
  border-radius: 50%;
  animation: neuralPulse 2s ease-in-out infinite;
}

@keyframes coreRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes neuralPulse {
  0%, 100% { 
    transform: scale(1);
    opacity: 1;
  }
  50% { 
    transform: scale(1.2);
    opacity: 0.5;
  }
}

.loading-title {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0;
  background: linear-gradient(135deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: relative;
}

.status-indicator.initializing {
  background: #fbbf24;
  animation: statusBlink 1s infinite;
}

.status-indicator.processing {
  background: #3b82f6;
  animation: statusPulse 1.5s infinite;
}

.status-indicator.completed {
  background: #10b981;
}

@keyframes statusBlink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.3; }
}

@keyframes statusPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.status-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

/* Progress section */
.progress-section {
  margin-bottom: 40px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.current-step {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 600;
}

.progress-percentage {
  color: #06b6d4;
  font-size: 18px;
  font-weight: 700;
  font-family: monospace;
}

.progress-container {
  position: relative;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-track {
  position: relative;
  width: 100%;
  height: 100%;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, 
    #6366f1 0%, 
    #06b6d4 50%,
    #ec4899 100%
  );
  border-radius: 4px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.4), 
    transparent
  );
  animation: progressShine 2s infinite;
}

@keyframes progressShine {
  0% { left: -100%; }
  100% { left: 100%; }
}

.progress-glow {
  position: absolute;
  top: -2px;
  left: 0;
  right: 0;
  bottom: -2px;
  background: linear-gradient(90deg, 
    #6366f1, 
    #06b6d4
  );
  border-radius: 6px;
  opacity: 0.3;
  filter: blur(4px);
  z-index: -1;
}

/* Workflow steps */
.workflow-steps {
  margin-bottom: 32px;
}

.workflow-step {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 12px 0;
}

.step-connector {
  position: absolute;
  left: 24px;
  top: -12px;
  width: 2px;
  height: 24px;
  background: linear-gradient(180deg, 
    rgba(99, 102, 241, 0.3) 0%, 
    rgba(99, 102, 241, 0.1) 100%
  );
}

.step-node {
  position: relative;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.node-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.workflow-step.pending .node-inner {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.workflow-step.active .node-inner {
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  border: 2px solid rgba(99, 102, 241, 0.5);
  animation: nodeActive 2s infinite;
}

.workflow-step.completed .node-inner {
  background: linear-gradient(135deg, #10b981, #059669);
  border: 2px solid rgba(16, 185, 129, 0.5);
}

@keyframes nodeActive {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
  }
  50% { 
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
  }
}

.node-icon {
  color: white;
  font-size: 20px;
}

.pending-dot {
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

.node-glow {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.workflow-step.active .node-glow {
  background: radial-gradient(circle, 
    rgba(99, 102, 241, 0.3) 0%, 
    transparent 70%
  );
  opacity: 1;
  animation: glowPulse 2s infinite;
}

@keyframes glowPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.step-info {
  flex: 1;
}

.step-title {
  color: white;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.workflow-step.pending .step-title {
  color: rgba(255, 255, 255, 0.5);
}

.step-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  line-height: 1.4;
}

.workflow-step.pending .step-description {
  color: rgba(255, 255, 255, 0.3);
}

/* Neural network */
.neural-network {
  margin-bottom: 32px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.network-svg {
  width: 100%;
  height: 100%;
  max-width: 400px;
}

.network-path {
  stroke: url(#lineGradient);
  stroke-width: 2;
  fill: none;
  stroke-dasharray: 5, 5;
  animation: pathFlow 3s linear infinite;
}

@keyframes pathFlow {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 20; }
}

.network-node {
  fill: rgba(255, 255, 255, 0.3);
  animation: nodePulse 2s ease-in-out infinite;
}

.network-node.active {
  fill: #6366f1;
  filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.8));
}

@keyframes nodePulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

/* Loading message */
.loading-message {
  text-align: center;
}

.message-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.terminal-cursor {
  width: 2px;
  height: 20px;
  background: #06b6d4;
  animation: cursorBlink 1s infinite;
}

@keyframes cursorBlink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.message-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 500;
  font-family: monospace;
}

/* Responsive design */
@media (max-width: 768px) {
  .loading-container {
    padding: 24px;
    min-height: 400px;
  }
  
  .loading-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .workflow-step {
    gap: 12px;
  }
  
  .step-node {
    width: 40px;
    height: 40px;
  }
  
  .node-icon {
    font-size: 18px;
  }
  
  .step-title {
    font-size: 14px;
  }
  
  .step-description {
    font-size: 12px;
  }
}
</style>