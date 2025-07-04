<template>
  <div class="workflow-step">
    <div class="step-content">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleSubmit"
      >
        <!-- Topic Selection -->
        <el-form-item 
          :label="t('workflow.step3.topic_selection')" 
          prop="chosen_topic_input"
          class="topic-selection-item"
        >
          <div class="topic-options">
            <div 
              v-for="(topic, index) in topicIdeas" 
              :key="index"
              class="topic-option"
              :class="{ active: selectedTopicIndex === index }"
              @click="selectTopic(topic, index)"
            >
              <div class="topic-content">
                <div class="topic-text">{{ topic }}</div>
              </div>
            </div>
          </div>
          
          <!-- 可编辑的主题输入框 -->
          <div class="topic-input-section">
            <div class="custom-label">
              <span class="label-text">{{ t('workflow.step3.custom_topic') }}</span>
              <el-tooltip 
                :content="t('workflow.step3.custom_topic_tooltip')"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon">
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
            <el-input
              v-model="formData.chosen_topic_input"
              type="textarea"
              :placeholder="t('workflow.step3.topic_input_placeholder')"
              :rows="2"
              :autosize="{ minRows: 2, maxRows: 4 }"
              :maxlength="300"
              show-word-limit
              resize="none"
              class="topic-input"
            />
          </div>
        </el-form-item>

        <!-- Optional Fields -->
        <div style="padding-top:32px; border-top: 1px solid #e8e8e8; margin-top:32px;">
          <el-row :gutter="0">
            <el-col :span="24">
              <el-form-item 
                :label="t('workflow.step3.background_info')" 
                prop="background_information"
                class="background-info-item"
              >
                <el-input
                  v-model="formData.background_information"
                  type="textarea"
                  :placeholder="t('workflow.step3.background_info_placeholder')"
                  :rows="4"
                  :maxlength="500"
                  show-word-limit
                  resize="none"
                />
                <div class="field-hint">
                  <span class="hint-text">
                    {{ t('workflow.step3.background_info_hint') }}
                  </span>
                </div>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="0">
            <el-col :span="24">
              <el-form-item 
                :label="t('workflow.step3.title_requirements')" 
                prop="title_generation_demands"
                class="title-demands-item"
              >
                <el-input
                  v-model="formData.title_generation_demands"
                  type="textarea"
                  :placeholder="t('workflow.step3.title_requirements_placeholder')"
                  :rows="4"
                  :maxlength="300"
                  show-word-limit
                  resize="none"
                />
                <div class="field-hint">
                  <span class="hint-text">
                    {{ t('workflow.step3.title_requirements_hint') }}
                  </span>
                </div>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="step-actions">
          <button 
            type="submit"
            class="glass-button primary-action-btn"
            :disabled="props.loading || !formData.chosen_topic_input || isButtonDisabled"
            @click="handleSubmit"
          >
            <div class="btn-content">
              <span v-if="!props.loading && !isButtonDisabled">{{ t('workflow.step3.generate_titles') }}</span>
              <span v-else-if="props.loading">{{ t('workflow.step3.generating') }}</span>
              <span v-else-if="isButtonDisabled">{{ t('workflow.step3.please_wait') }}</span>
            </div>
          </button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { QuestionFilled } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import type { WorkflowState } from '@/types/workflow'

interface Props {
  data?: WorkflowState | null
  loading?: boolean
}

interface Emits {
  (e: 'next', data: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const { t } = useI18n()

// Form reference
const formRef = ref<FormInstance>()

// Button disabled state for preventing multiple submissions  
const isButtonDisabled = ref(false)

// Form data
const formData = reactive({
  chosen_topic_input: '', // 新的输入框字段
  background_information: '',
  title_generation_demands: ''
})

// 选中的主题索引
const selectedTopicIndex = ref(-1)

// Form validation rules - 使用响应式翻译
const rules = computed(() => ({
  chosen_topic_input: [
    { required: true, message: t('workflow.step3.validation.topic_required'), trigger: 'change' }
  ]
}))

// Computed properties
const topicIdeas = computed(() => {
  if (!props.data?.gen_topic_ideas) return []
  
  if (Array.isArray(props.data.gen_topic_ideas)) {
    return props.data.gen_topic_ideas
  }
  
  // If it's a string, try to parse as JSON or split by lines
  try {
    const parsed = JSON.parse(props.data.gen_topic_ideas)
    return Array.isArray(parsed) ? parsed : [props.data.gen_topic_ideas]
  } catch {
    // If parsing fails, split by lines or return as single item
    const stringValue = String(props.data.gen_topic_ideas)
    return stringValue.split('\n').filter(topic => topic.trim())
  }
})

// Methods
const selectTopic = (topic: string, index: number) => {
  selectedTopicIndex.value = index
  formData.chosen_topic_input = topic
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    
    // Disable button for 8 seconds to prevent multiple submissions
    isButtonDisabled.value = true
    setTimeout(() => {
      isButtonDisabled.value = false
    }, 8000)
    
    // 将chosen_topic_input作为chosen_topic传递给接口
    const submitData = {
      chosen_topic: formData.chosen_topic_input,
      background_information: formData.background_information,
      title_generation_demands: formData.title_generation_demands
    }
    emit('next', submitData)
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// Initialize form data if editing existing workflow
if (props.data) {
  formData.chosen_topic_input = props.data.chosen_topic || ''
  formData.background_information = props.data.background_information || ''
  formData.title_generation_demands = props.data.title_generation_demands || ''
  
  // 如果有已选择的主题，尝试找到对应的索引
  if (props.data.chosen_topic) {
    const index = topicIdeas.value.findIndex(topic => topic === props.data.chosen_topic)
    if (index !== -1) {
      selectedTopicIndex.value = index
    }
  }
}
</script>

<style scoped>
.workflow-step {
  max-width: 900px;
  margin: 0 auto;
}

.step-content {
  background: transparent;
  border-radius: 8px;
  padding: 32px;
}

.topic-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.topic-option {
  background: white;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.topic-option:hover:not(.active) {
  border: 2px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, 
                rgba(91, 95, 241, 0.5) 0%, 
                rgba(124, 58, 237, 0.5) 25%,
                rgba(190, 24, 93, 0.5) 50%,
                rgba(124, 58, 237, 0.5) 75%,
                rgba(91, 95, 241, 0.5) 100%
              ) border-box;
  background-size: 100% 100%, 200% 200%;
  animation: border-flow 3s ease infinite;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12);
}

.topic-option.active {
  border: 2px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, 
                rgba(91, 95, 241, 0.5) 0%, 
                rgba(124, 58, 237, 0.5) 25%,
                rgba(190, 24, 93, 0.5) 50%,
                rgba(124, 58, 237, 0.5) 75%,
                rgba(91, 95, 241, 0.5) 100%
              ) border-box;
  background-size: 100% 100%, 200% 200%;
  animation: border-flow 3s ease infinite;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
  position: relative;
  z-index: 1;
}

.topic-option.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(147, 51, 234, 0.03);
  border-radius: 6px;
  pointer-events: none;
  z-index: -1;
}

@keyframes border-flow {
  0%, 100% {
    background-position: 0% 0%, 0% 50%;
  }
  50% {
    background-position: 0% 0%, 100% 50%;
  }
}

.topic-content {
  display: flex;
  align-items: flex-start;
  width: 100%;
  position: relative;
  z-index: 2;
}

.topic-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  flex: 1;
  word-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  position: relative;
  z-index: 2;
}

.field-hint {
  margin-top: 8px;
}

.hint-text {
  color: #909399;
  font-size: 14px;
  line-height: 1.4;
}

/* Element Plus form item labels加粗 */
.topic-selection-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

.background-info-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

.title-demands-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

/* 自定义label样式 */
.topic-input-section {
  margin-top: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.custom-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  width: 100%;
}

.label-text {
  font-weight: 700;
  font-size: 16px;
  color: #303133;
}

.help-icon {
  color: #909399;
  cursor: pointer;
  font-size: 16px;
  transition: color 0.3s ease;
}

.help-icon:hover {
  color: rgb(128, 96, 244);
}

/* Element Plus textarea样式优化 */
.topic-input {
  width: 100% !important;
  display: block;
}

.topic-input :deep(.el-textarea__inner) {
  width: 100%;
  border-radius: 8px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s ease;
  box-shadow: none;
  font-size: 14px;
  line-height: 1.5;
  min-height: 60px;
}

.topic-input :deep(.el-textarea__inner):hover {
  border-color: #c0c4cc;
}

.topic-input :deep(.el-textarea__inner):focus {
  border-color: rgb(128, 96, 244);
  box-shadow: 0 2px 8px rgba(128, 96, 244, 0.15);
}

/* 其他textarea样式 */
:deep(.el-textarea__inner) {
  border-radius: 8px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s ease;
  font-size: 14px;
  line-height: 1.5;
  box-shadow: none;
}

:deep(.el-textarea__inner):focus {
  border-color: rgb(128, 96, 244);
  box-shadow: 0 2px 8px rgba(128, 96, 244, 0.15);
}

:deep(.el-textarea__inner):hover {
  border-color: #c0c4cc;
}

/* 字数统计样式 */
:deep(.el-input__count) {
  color: #909399;
  font-size: 12px;
}

.step-actions {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e8e8e8;
}

/* Glass Buttons - 与dashboard保持一致 */
.glass-button {
  position: relative;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 12px;
  padding: 0;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s ease;
  min-height: 56px;
  min-width: 200px;
}

.primary-action-btn.glass-button {
  background: linear-gradient(135deg, 
    #5b5ff1, 
    #7c3aed
  ) !important;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  z-index: 2;
  position: relative;
  min-height: 24px;
}

.primary-action-btn.glass-button:hover {
  background: linear-gradient(135deg, 
    #6366f1, 
    #8b5cf6
  ) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.primary-action-btn.glass-button:disabled {
  background: #f5f5f5 !important;
  color: #bfbfbf;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.primary-action-btn.glass-button:disabled .btn-content {
  color: #bfbfbf;
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

.primary-action-btn.glass-button:disabled::before {
  display: none;
}

@media (max-width: 768px) {
  .step-content {
    padding: 20px;
  }
  
  .topic-option {
    padding: 16px;
  }
  
  .topic-content {
    gap: 12px;
  }
  
  .topic-text {
    font-size: 14px;
  }
  
  .custom-label {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>