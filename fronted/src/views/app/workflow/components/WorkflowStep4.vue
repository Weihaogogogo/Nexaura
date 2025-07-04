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
        <!-- Title Selection -->
        <el-form-item 
          :label="t('workflow.step4.title_selection')" 
          prop="article_title_input"
          class="title-selection-item"
        >
          <div class="title-options">
            <div 
              v-for="(title, index) in articleTitles" 
              :key="index"
              class="title-option"
              :class="{ active: selectedTitleIndex === index }"
              @click="selectTitle(title, index)"
            >
              <div class="title-content">
                <div class="title-text">{{ title }}</div>
              </div>
            </div>
          </div>
          
          <!-- 可编辑的标题输入框 -->
          <div class="title-input-section" style="margin-bottom:18px">
            <div class="custom-label">
              <span class="label-text">{{ t('workflow.step4.custom_title') }}</span>
              <el-tooltip 
                :content="t('workflow.step4.custom_title_tooltip')"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon">
                  <QuestionFilled />
                </el-icon>
              </el-tooltip>
            </div>
            <el-input
              v-model="formData.article_title_input"
              type="textarea"
              :placeholder="t('workflow.step4.title_input_placeholder')"
              :rows="2"
              :autosize="{ minRows: 2, maxRows: 4 }"
              :maxlength="300"
              show-word-limit
              resize="none"
              class="title-input"
            />
          </div>
        </el-form-item>

        <!-- Optional Fields -->
        <div style="padding-top:32px; border-top: 1px solid #e8e8e8; margin-top:32px;">
          <el-row :gutter="0">
            <el-col :span="24">
              <el-form-item 
                :label="t('workflow.step4.secondary_keywords')" 
                prop="secondary_keywords"
                class="keywords-item"
              >
                <el-input
                  v-model="formData.secondary_keywords"
                  type="textarea"
                  :placeholder="t('workflow.step4.secondary_keywords_placeholder')"
                  :rows="2"
                  :autosize="{ minRows: 2, maxRows: 3 }"
                  :maxlength="200"
                  show-word-limit
                  resize="none"
                />
                <div class="field-hint">
                  <span class="hint-text">
                    {{ t('workflow.step4.secondary_keywords_hint') }}
                  </span>
                </div>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="0">
            <el-col :span="24">
              <el-form-item 
                :label="t('workflow.step4.outline_requirements')" 
                prop="outline_demand"
                class="outline-item"
              >
                <el-input
                  v-model="formData.outline_demand"
                  type="textarea"
                  :placeholder="t('workflow.step4.outline_requirements_placeholder')"
                  :rows="3"
                  :autosize="{ minRows: 3, maxRows: 5 }"
                  :maxlength="400"
                  show-word-limit
                  resize="none"
                />
                <div class="field-hint">
                  <span class="hint-text">
                    {{ t('workflow.step4.outline_requirements_hint') }}
                  </span>
                </div>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="0">
            <el-col :span="24">
              <el-form-item 
                :label="t('workflow.step4.additional_knowledge')" 
                prop="additional_knowledge_points"
                class="knowledge-item"
              >
                <el-input
                  v-model="formData.additional_knowledge_points"
                  type="textarea"
                  :placeholder="t('workflow.step4.additional_knowledge_placeholder')"
                  :rows="4"
                  :autosize="{ minRows: 4, maxRows: 6 }"
                  :maxlength="500"
                  show-word-limit
                  resize="none"
                />
                <div class="field-hint">
                  <span class="hint-text">
                    {{ t('workflow.step4.additional_knowledge_hint') }}
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
            :disabled="props.loading || !formData.article_title_input || isButtonDisabled"
            @click="handleSubmit"
          >
            <div class="btn-content">
              <span v-if="!props.loading && !isButtonDisabled">{{ t('workflow.step4.generate_outline') }}</span>
              <span v-else-if="props.loading">{{ t('workflow.step4.generating') }}</span>
              <span v-else-if="isButtonDisabled">{{ t('workflow.step4.please_wait') }}</span>
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
  article_title_input: '', // 新的输入框字段
  secondary_keywords: '',
  outline_demand: '',
  additional_knowledge_points: ''
})

// 选中的标题索引
const selectedTitleIndex = ref(-1)

// Form validation rules - 使用响应式翻译
const rules = computed(() => ({
  article_title_input: [
    { required: true, message: t('workflow.step4.validation.title_required'), trigger: 'change' }
  ]
}))

// Computed properties
const articleTitles = computed(() => {
  if (!props.data?.gen_article_titles) return []
  
  if (Array.isArray(props.data.gen_article_titles)) {
    return props.data.gen_article_titles
  }
  
  // If it's a string, try to parse as JSON or split by lines
  try {
    const parsed = JSON.parse(props.data.gen_article_titles)
    return Array.isArray(parsed) ? parsed : [props.data.gen_article_titles]
  } catch {
    // If parsing fails, split by lines or return as single item
    const stringValue = String(props.data.gen_article_titles)
    return stringValue.split('\n').filter(title => title.trim())
  }
})

// Methods
const selectTitle = (title: string, index: number) => {
  selectedTitleIndex.value = index
  formData.article_title_input = title
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    
    // Disable button for 8 seconds to prevent multiple submissions
    isButtonDisabled.value = true
    setTimeout(() => {
      isButtonDisabled.value = false
    }, 8000)
    
    // 将article_title_input作为article_title传递给接口
    const submitData = {
      article_title: formData.article_title_input,
      secondary_keywords: formData.secondary_keywords,
      outline_demand: formData.outline_demand,
      additional_knowledge_points: formData.additional_knowledge_points
    }
    emit('next', submitData)
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// Initialize form data if editing existing workflow
if (props.data) {
  formData.article_title_input = props.data.article_title || ''
  formData.secondary_keywords = props.data.secondary_keywords || ''
  formData.outline_demand = props.data.outline_demand || ''
  formData.additional_knowledge_points = props.data.additional_knowledge_points || ''
  
  // 如果有已选择的标题，尝试找到对应的索引
  if (props.data.article_title) {
    const index = articleTitles.value.findIndex(title => title === props.data.article_title)
    if (index !== -1) {
      selectedTitleIndex.value = index
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

.title-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
  width: 100%;
}

.title-option {
  background: white;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.title-option:hover:not(.active) {
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

.title-option.active {
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

.title-option.active::before {
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

.title-content {
  display: flex;
  align-items: flex-start;
  width: 100%;
  position: relative;
  z-index: 2;
}

.title-text {
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
.title-selection-item {
  width: 100%;
}

.title-selection-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

.title-selection-item :deep(.el-form-item__content) {
  width: 100%;
}

/* 确保所有El Form Item都是全宽 */
:deep(.el-form-item) {
  width: 100%;
}

.keywords-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

.outline-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

.knowledge-item :deep(.el-form-item__label) {
  font-weight: 700 !important;
  font-size: 16px !important;
  color: #303133 !important;
}

/* 自定义label样式 */
.title-input-section {
  margin-top: 20px;
  margin-bottom: 10px;
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
.title-input {
  width: 100% !important;
  display: block;
}

.title-input :deep(.el-textarea__inner) {
  width: 100%;
  border-radius: 8px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s ease;
  box-shadow: none;
  font-size: 14px;
  line-height: 1.5;
  min-height: 60px;
}

.title-input :deep(.el-textarea__inner):hover {
  border-color: #c0c4cc;
}

.title-input :deep(.el-textarea__inner):focus {
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

/* Glass Buttons - 与step3保持一致 */
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

.primary-action-btn.glass-button:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    #6366f1, 
    #8b5cf6
  ) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.primary-action-btn.glass-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@media (max-width: 768px) {
  .step-content {
    padding: 20px;
  }
  
  .title-option {
    padding: 16px;
  }
  
  .title-content {
    gap: 12px;
  }
  
  .title-text {
    font-size: 14px;
  }
  
  .custom-label {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>