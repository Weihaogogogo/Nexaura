<template>
  <div class="progress-indicator">
    <!-- Circular Progress -->
    <div v-if="type === 'circle'" class="circular-progress">
      <a-progress
        type="circle"
        :percent="percent"
        :width="size"
        :stroke-color="strokeColor"
        :trail-color="trailColor"
        :stroke-width="strokeWidth"
        :show-info="showInfo"
      >
        <template #format="{ percent }">
          <div class="progress-content">
            <div class="progress-icon" v-if="icon">
              <component :is="icon" />
            </div>
            <div class="progress-text">
              <div class="progress-number">{{ percent }}%</div>
              <div class="progress-label" v-if="label">{{ label }}</div>
            </div>
          </div>
        </template>
      </a-progress>
    </div>
    
    <!-- Line Progress with Steps -->
    <div v-else-if="type === 'steps'" class="steps-progress">
      <div class="steps-header">
        <h4 class="steps-title" v-if="title">{{ title }}</h4>
        <div class="steps-info">
          {{ currentStep }} / {{ totalSteps }}
        </div>
      </div>
      
      <a-progress
        :percent="stepProgress"
        :stroke-color="strokeColor"
        :trail-color="trailColor"
        :show-info="false"
        :stroke-width="8"
        stroke-line-cap="round"
      />
      
      <div class="steps-list" v-if="steps && steps.length > 0">
        <div 
          v-for="(step, index) in steps" 
          :key="index"
          class="step-item"
          :class="{
            completed: index < currentStep - 1,
            active: index === currentStep - 1,
            pending: index >= currentStep
          }"
        >
          <div class="step-indicator">
            <CheckOutlined v-if="index < currentStep - 1" />
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="step-content">
            <div class="step-title">{{ step.title }}</div>
            <div class="step-description" v-if="step.description">
              {{ step.description }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Quota Progress -->
    <div v-else-if="type === 'quota'" class="quota-progress">
      <div class="quota-header">
        <div class="quota-title">{{ title || $t('profile.quota') }}</div>
        <div class="quota-numbers">
          {{ used }} / {{ total }}
        </div>
      </div>
      
      <a-progress
        :percent="quotaPercent"
        :stroke-color="getQuotaColor()"
        :trail-color="'#f0f0f0'"
        :show-info="false"
        :stroke-width="6"
        stroke-line-cap="round"
      />
      
      <div class="quota-footer">
        <span class="quota-label">{{ getQuotaLabel() }}</span>
        <a-button 
          v-if="showUpgrade && quotaPercent > 80" 
          type="link" 
          size="small"
          @click="$emit('upgrade')"
        >
          {{ $t('profile.upgrade') }}
        </a-button>
      </div>
    </div>
    
    <!-- Default Line Progress -->
    <div v-else class="line-progress">
      <div class="progress-header" v-if="title || showPercent">
        <div class="progress-title" v-if="title">{{ title }}</div>
        <div class="progress-percent" v-if="showPercent">{{ percent }}%</div>
      </div>
      
      <a-progress
        :percent="percent"
        :stroke-color="strokeColor"
        :trail-color="trailColor"
        :show-info="false"
        :stroke-width="strokeWidth"
        :stroke-line-cap="strokeLineCap"
      />
      
      <div class="progress-footer" v-if="description">
        <span class="progress-description">{{ description }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { CheckOutlined } from '@ant-design/icons-vue'

interface Step {
  title: string
  description?: string
}

interface Props {
  type?: 'line' | 'circle' | 'steps' | 'quota'
  percent?: number
  title?: string
  description?: string
  label?: string
  icon?: any
  size?: number
  strokeColor?: string | object
  trailColor?: string
  strokeWidth?: number
  strokeLineCap?: 'round' | 'square'
  showInfo?: boolean
  showPercent?: boolean
  showUpgrade?: boolean
  // Steps specific
  steps?: Step[]
  currentStep?: number
  totalSteps?: number
  // Quota specific
  used?: number
  total?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'line',
  percent: 0,
  size: 120,
  strokeColor: '#1890ff',
  trailColor: '#f0f0f0',
  strokeWidth: 6,
  strokeLineCap: 'round',
  showInfo: true,
  showPercent: true,
  showUpgrade: true,
  currentStep: 1,
  totalSteps: 1,
  used: 0,
  total: 100
})

defineEmits<{
  upgrade: []
}>()

const { t } = useI18n()

const stepProgress = computed(() => {
  if (props.totalSteps === 0) return 0
  return Math.round((props.currentStep / props.totalSteps) * 100)
})

const quotaPercent = computed(() => {
  if (props.total === 0) return 0
  return Math.round((props.used / props.total) * 100)
})

const getQuotaColor = () => {
  const percent = quotaPercent.value
  if (percent >= 90) return '#ff4d4f'
  if (percent >= 80) return '#faad14'
  if (percent >= 60) return '#1890ff'
  return '#52c41a'
}

const getQuotaLabel = () => {
  const percent = quotaPercent.value
  if (percent >= 90) return t('profile.quota_critical')
  if (percent >= 80) return t('profile.quota_high')
  if (percent >= 60) return t('profile.quota_normal')
  return t('profile.quota_low')
}
</script>

<style scoped>
.progress-indicator {
  width: 100%;
}

/* Circular Progress */
.circular-progress {
  display: flex;
  justify-content: center;
  align-items: center;
}

.progress-content {
  text-align: center;
}

.progress-icon {
  font-size: 24px;
  color: #1890ff;
  margin-bottom: 8px;
}

.progress-number {
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

.progress-label {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 4px;
}

/* Steps Progress */
.steps-progress {
  width: 100%;
}

.steps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.steps-title {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  margin: 0;
}

.steps-info {
  font-size: 14px;
  color: #8c8c8c;
  font-weight: 500;
}

.steps-list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.step-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  transition: all 0.3s;
}

.step-item.completed .step-indicator {
  background: #52c41a;
  color: white;
}

.step-item.active .step-indicator {
  background: #1890ff;
  color: white;
}

.step-item.pending .step-indicator {
  background: #f0f0f0;
  color: #8c8c8c;
}

.step-content {
  flex: 1;
  padding-top: 4px;
}

.step-title {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
  margin-bottom: 4px;
}

.step-item.pending .step-title {
  color: #8c8c8c;
}

.step-description {
  font-size: 12px;
  color: #8c8c8c;
  line-height: 1.4;
}

/* Quota Progress */
.quota-progress {
  width: 100%;
}

.quota-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.quota-title {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
}

.quota-numbers {
  font-size: 12px;
  color: #8c8c8c;
  font-weight: 500;
}

.quota-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.quota-label {
  font-size: 12px;
  color: #8c8c8c;
}

/* Line Progress */
.line-progress {
  width: 100%;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-title {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
}

.progress-percent {
  font-size: 14px;
  color: #1890ff;
  font-weight: 600;
}

.progress-footer {
  margin-top: 8px;
}

.progress-description {
  font-size: 12px;
  color: #8c8c8c;
}

/* Responsive */
@media (max-width: 768px) {
  .steps-list {
    gap: 12px;
  }
  
  .step-indicator {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .step-title {
    font-size: 13px;
  }
  
  .step-description {
    font-size: 11px;
  }
}
</style>