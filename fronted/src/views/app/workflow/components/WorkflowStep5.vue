<template>
  <div class="workflow-step">
    <div class="step-content">
      <a-form
        ref="formRef"
        id="step5-form"
        :model="formData"
        :rules="rules"
        layout="vertical"
        @finish="handleSubmit"
      >
        <!-- Settings Row - Moved to top -->
        <div style="margin-bottom: 32px; padding-bottom: 12px; border-bottom: 1px solid #e8e8e8;">
          <a-row :gutter="24">
            <a-col :md="12" :span="24">
              <a-form-item 
                :label="t('workflow.step5.narrative_perspective')"
                name="narrative_perspective"
                :required="true"
              >
                <a-select
                  v-model:value="formData.narrative_perspective"
                  :placeholder="t('workflow.step5.narrative_perspective_placeholder')"
                  size="large"
                  :options="perspectiveOptions"
                />
                <div class="field-hint">
                  <a-typography-text type="secondary">
                    {{ t('workflow.step5.narrative_perspective_hint') }}
                  </a-typography-text>
                </div>
              </a-form-item>
            </a-col>

            <a-col :md="12" :span="24">
              <a-form-item>
                <template #label>
                  <div class="label-with-tooltip">
                    <span>{{ t('workflow.step5.image_generation') }}</span>
                    <a-tooltip 
                      :title="t('workflow.step5.image_generation_tooltip')"
                      placement="top"
                    >
                      <QuestionCircleOutlined class="help-icon" />
                    </a-tooltip>
                  </div>
                </template>
                <a-select
                  v-model:value="formData.image_generation_status"
                  :placeholder="t('workflow.step5.image_generation_placeholder')"
                  size="large"
                  :options="imageGenerationOptions"
                  @change="handleImageOptionChange"
                />
                <div class="field-hint">
                  <a-typography-text type="secondary">
                    {{ t('workflow.step5.image_generation_hint') }}
                  </a-typography-text>
                </div>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <!-- Outline Editor - Moved to bottom -->
        <a-form-item 
          :label="t('workflow.step5.article_outline')" 
          name="article_outline"
          :required="true"
        >
          <OutlineEditor
            v-model="formData.article_outline"
            :h1-title="articleTitle"
          />
          <div class="field-hint">
            <a-typography-text type="secondary">
              {{ t('workflow.step5.outline_hint') }}
            </a-typography-text>
          </div>
        </a-form-item>
      </a-form>
    </div>

    <!-- Fixed Action Button -->
    <div class="fixed-actions">
      <div class="actions-container">
        <button 
          type="submit"
          form="step5-form"
          class="glass-button primary-action-btn"
          :disabled="props.loading || !formData.article_outline || !formData.narrative_perspective || isButtonDisabled"
        >
          <div class="btn-content">
            <span v-if="!props.loading && !isButtonDisabled">{{ t('workflow.step5.generate_article') }}</span>
            <span v-else-if="props.loading">{{ t('workflow.step5.generating') }}</span>
            <span v-else-if="isButtonDisabled">{{ t('workflow.step5.please_wait') }}</span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { QuestionCircleOutlined } from '@ant-design/icons-vue'
import type { FormInstance } from 'ant-design-vue'
import type { WorkflowState } from '@/types/workflow'
import OutlineEditor from '@/components/editors/OutlineEditor.vue'

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
  article_outline: '',
  narrative_perspective: '1',
  main_image_option: true,
  sub_images_option: true,
  image_generation_enabled: true,
  image_generation_status: 'enabled' // 默认值设置为 enabled
})

// Perspective options - 使用响应式翻译
const perspectiveOptions = computed(() => [
  { value: '1', label: t('workflow.step5.perspective_options.first_person') },
  { value: '2', label: t('workflow.step5.perspective_options.second_person') }
])

// Image generation options - 使用响应式翻译
const imageGenerationOptions = computed(() => [
  { value: 'enabled', label: t('workflow.step5.image_options.enabled') },
  { value: 'disabled', label: t('workflow.step5.image_options.disabled') }
])

// 计算文章标题
const articleTitle = computed(() => {
  // 从工作流数据中获取文章标题，优先使用用户输入的标题
  return props.data?.article_title || props.data?.chosen_topic || '文章标题'
})

// Form validation rules - 使用响应式翻译
const rules = computed(() => ({
  article_outline: [
    { required: true, message: t('workflow.step5.validation.outline_required'), trigger: 'blur' },
    { min: 10, message: t('workflow.step5.validation.outline_min_length'), trigger: 'blur' }
  ],
  narrative_perspective: [
    { required: true, message: t('workflow.step5.validation.perspective_required'), trigger: 'change' }
  ]
}))

// Methods
const handleImageSwitchChange = (value: boolean) => {
  formData.main_image_option = value
  formData.sub_images_option = value
}

const handleImageOptionChange = (value: string) => {
  const enabled = value === 'enabled'
  formData.image_generation_enabled = enabled
  formData.main_image_option = enabled
  formData.sub_images_option = enabled
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    
    // Disable button for 8 seconds to prevent multiple submissions
    isButtonDisabled.value = true
    setTimeout(() => {
      isButtonDisabled.value = false
    }, 8000)
    
    emit('next', { ...formData })
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}

// Watch for data changes and initialize form
watch(() => props.data, (newData) => {
  if (newData) {
    formData.article_outline = newData.gen_article_outline || newData.article_outline || ''
    formData.narrative_perspective = newData.narrative_perspective || '1'
    
    // 如果是新的工作流或者没有明确设置图片选项，使用默认值 enabled
    if (newData.main_image_option === undefined && newData.sub_images_option === undefined) {
      formData.main_image_option = true
      formData.sub_images_option = true
      formData.image_generation_enabled = true
      formData.image_generation_status = 'enabled'
    } else {
      formData.main_image_option = newData.main_image_option ?? true
      formData.sub_images_option = newData.sub_images_option ?? true
      formData.image_generation_enabled = (newData.main_image_option ?? true) && (newData.sub_images_option ?? true)
      formData.image_generation_status = formData.image_generation_enabled ? 'enabled' : 'disabled'
    }
  }
}, { immediate: true })
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
  padding-bottom: 100px; /* 为固定按钮留出空间 */
}

.label-with-tooltip {
  display: flex;
  align-items: center;
  gap: 8px;
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

.field-hint {
  margin-top: 4px;
}

/* 大纲编辑器样式优化 */
:deep(.outline-editor) {
  min-height: 400px;
}

/* 确保表单项可以完全展示内容 */
:deep(.ant-form-item) {
  margin-bottom: 24px;
}

/* 移除任何可能的高度限制 */
.step-content {
  max-height: none !important;
  overflow: visible !important;
}

/* Ant Design表单标签加粗 */
:deep(.ant-form-item-label) > label {
  font-weight: 700 !important;
}

.fixed-actions {
  position: fixed;
  bottom: 0;
  left: 240px; /* sidebar宽度240px */
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid #e8e8e8;
  padding: 16px 0;
  z-index: 1000;
}

.actions-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  padding: 0 32px;
}

/* Glass Buttons - 与step1保持一致 */
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
    padding-bottom: 120px; /* 移动端需要更多空间 */
  }
  
  .fixed-actions {
    left: 0 !important; /* 移动端从左边缘开始，使用 !important 确保覆盖 */
  }
  
  .actions-container {
    padding: 0 20px;
  }
  
  .label-with-tooltip {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>