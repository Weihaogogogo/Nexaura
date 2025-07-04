<template>
  <div class="workflow-step">
    <div class="step-content">
      <a-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        layout="vertical"
        @finish="handleSubmit"
      >
        <a-row :gutter="24">
          <a-col :span="24">
            <a-form-item 
              :label="t('workflow.step1.main_keyword')" 
              name="keyword"
              :required="true"
            >
              <a-input
                v-model:value="formData.keyword"
                :placeholder="t('workflow.step1.main_keyword_placeholder')"
                size="large"
                :maxlength="50"
                show-count
              />
              <div class="field-hint">
                <a-typography-text type="secondary">
                  {{ t('workflow.step1.main_keyword_hint') }}
                </a-typography-text>
              </div>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :md="12" :span="24" :style="{ marginTop: '10px' }">
            <a-form-item 
              :label="t('workflow.step1.target_country')" 
              name="target_market"
              :required="true"
            >
              <a-select
                v-model:value="formData.target_market"
                :placeholder="t('workflow.step1.target_country_placeholder')"
                size="large"
                :options="targetMarketOptions"
                show-search
                :filter-option="(input, option) => option.label.toLowerCase().includes(input.toLowerCase())"
              />
              <div class="field-hint">
                <a-typography-text type="secondary">
                  {{ t('workflow.step1.target_country_hint') }}
                </a-typography-text>
              </div>
            </a-form-item>
          </a-col>

          <a-col :md="12" :span="24" :style="{ marginTop: '10px' }">
            <a-form-item 
              :label="t('workflow.step1.language')" 
              name="article_language"
              :required="true"
            >
              <a-select
                v-model:value="formData.article_language"
                :placeholder="t('workflow.step1.language_placeholder')"
                size="large"
                show-search
                :filter-option="(input, option) => option.label.toLowerCase().includes(input.toLowerCase())"
              >
                <a-select-option 
                  v-for="option in languageOptions" 
                  :key="option.value" 
                  :value="option.value"
                  :label="option.label"
                >
                  <div class="language-option">
                    <span :class="`fi fi-${option.flag}`" class="flag-icon"></span>
                    <span class="language-name">{{ option.label }}</span>
                  </div>
                </a-select-option>
              </a-select>
              <div class="field-hint">
                <a-typography-text type="secondary">
                  {{ t('workflow.step1.language_hint') }}
                </a-typography-text>
              </div>
            </a-form-item>
          </a-col>
        </a-row>

        <div class="step-actions">
          <button 
            type="submit"
            class="glass-button primary-action-btn"
            :disabled="props.loading || isButtonDisabled"
          >
            <div class="btn-content">
              <span v-if="!props.loading && !isButtonDisabled">{{ t('workflow.step1.generate_topics') }}</span>
              <span v-else-if="props.loading">{{ t('workflow.step1.generating') }}</span>
              <span v-else-if="isButtonDisabled">{{ t('workflow.step1.please_wait') }}</span>
            </div>
          </button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { FormInstance } from 'ant-design-vue'
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
  keyword: '',
  target_market: 'us', // 默认选择美国
  article_language: 'English (US)' // 默认选择英语(美国)
})

// Form validation rules - 使用响应式翻译
const rules = computed(() => ({
  keyword: [
    { required: true, message: t('workflow.step1.validation.keyword_required'), trigger: 'blur' },
    { min: 1, max: 50, message: t('workflow.step1.validation.keyword_length'), trigger: 'blur' }
  ],
  target_market: [
    { required: true, message: t('workflow.step1.validation.target_market_required'), trigger: 'change' }
  ],
  article_language: [
    { required: true, message: t('workflow.step1.validation.language_required'), trigger: 'change' }
  ]
}))

// Options - 使用ISO 3166-1 alpha-2国家代码
const targetMarketOptions = [
  // 主要英语市场
  { label: 'United States', value: 'us' },
  { label: 'United Kingdom', value: 'gb' },
  { label: 'Australia', value: 'au' },
  { label: 'Canada', value: 'ca' },
  { label: 'Ireland', value: 'ie' },
  { label: 'New Zealand', value: 'nz' },
  { label: 'South Africa', value: 'za' },
  
  // 主要欧洲市场
  { label: 'Germany', value: 'de' },
  { label: 'France', value: 'fr' },
  { label: 'Italy', value: 'it' },
  { label: 'Spain', value: 'es' },
  { label: 'Netherlands', value: 'nl' },
  { label: 'Poland', value: 'pl' },
  { label: 'Portugal', value: 'pt' },
  { label: 'Belgium', value: 'be' },
  { label: 'Austria', value: 'at' },
  { label: 'Switzerland', value: 'ch' },
  { label: 'Sweden', value: 'se' },
  { label: 'Norway', value: 'no' },
  { label: 'Denmark', value: 'dk' },
  { label: 'Finland', value: 'fi' },
  { label: 'Czech Republic', value: 'cz' },
  { label: 'Hungary', value: 'hu' },
  { label: 'Greece', value: 'gr' },
  { label: 'Romania', value: 'ro' },
  { label: 'Bulgaria', value: 'bg' },
  { label: 'Croatia', value: 'hr' },
  { label: 'Slovakia', value: 'sk' },
  { label: 'Slovenia', value: 'si' },
  { label: 'Estonia', value: 'ee' },
  { label: 'Latvia', value: 'lv' },
  { label: 'Lithuania', value: 'lt' },
  
  // 主要亚洲市场
  { label: 'China', value: 'cn' },
  { label: 'Japan', value: 'jp' },
  { label: 'South Korea', value: 'kr' },
  { label: 'India', value: 'in' },
  { label: 'Indonesia', value: 'id' },
  { label: 'Thailand', value: 'th' },
  { label: 'Vietnam', value: 'vn' },
  { label: 'Malaysia', value: 'my' },
  { label: 'Singapore', value: 'sg' },
  { label: 'Philippines', value: 'ph' },
  { label: 'Pakistan', value: 'pk' },
  { label: 'Bangladesh', value: 'bd' },
  { label: 'Sri Lanka', value: 'lk' },
  { label: 'Taiwan', value: 'tw' },
  { label: 'Hong Kong', value: 'hk' },
  
  // 中东地区
  { label: 'Saudi Arabia', value: 'sa' },
  { label: 'United Arab Emirates', value: 'ae' },
  { label: 'Israel', value: 'il' },
  { label: 'Turkey', value: 'tr' },
  { label: 'Iran', value: 'ir' },
  { label: 'Jordan', value: 'jo' },
  { label: 'Kuwait', value: 'kw' },
  { label: 'Qatar', value: 'qa' },
  { label: 'Bahrain', value: 'bh' },
  { label: 'Oman', value: 'om' },
  { label: 'Lebanon', value: 'lb' },
  
  // 美洲
  { label: 'Brazil', value: 'br' },
  { label: 'Mexico', value: 'mx' },
  { label: 'Argentina', value: 'ar' },
  { label: 'Chile', value: 'cl' },
  { label: 'Colombia', value: 'co' },
  { label: 'Peru', value: 'pe' },
  { label: 'Venezuela', value: 've' },
  { label: 'Uruguay', value: 'uy' },
  { label: 'Ecuador', value: 'ec' },
  { label: 'Bolivia', value: 'bo' },
  { label: 'Paraguay', value: 'py' },
  
  // 非洲
  { label: 'Nigeria', value: 'ng' },
  { label: 'Egypt', value: 'eg' },
  { label: 'Kenya', value: 'ke' },
  { label: 'Ghana', value: 'gh' },
  { label: 'Morocco', value: 'ma' },
  { label: 'Algeria', value: 'dz' },
  { label: 'Tunisia', value: 'tn' },
  { label: 'Ethiopia', value: 'et' },
  { label: 'Tanzania', value: 'tz' },
  { label: 'Uganda', value: 'ug' },
  
  // 俄罗斯及独联体
  { label: 'Russia', value: 'ru' },
  { label: 'Ukraine', value: 'ua' },
  { label: 'Belarus', value: 'by' },
  { label: 'Kazakhstan', value: 'kz' },
  { label: 'Uzbekistan', value: 'uz' },
  { label: 'Georgia', value: 'ge' },
  { label: 'Armenia', value: 'am' },
  { label: 'Azerbaijan', value: 'az' },
  { label: 'Kyrgyzstan', value: 'kg' },
  { label: 'Tajikistan', value: 'tj' },
  { label: 'Turkmenistan', value: 'tm' },
  { label: 'Moldova', value: 'md' }
]

const languageOptions = [
  { label: 'English (US)', value: 'English (US)', flag: 'us' },
  { label: 'English (UK)', value: 'English (UK)', flag: 'gb' },
  { label: 'English (Australia)', value: 'English (Australia)', flag: 'au' },
  { label: 'English (Canada)', value: 'English (Canada)', flag: 'ca' },
  { label: 'Afrikaans', value: 'Afrikaans', flag: 'za' },
  { label: 'Albanian', value: 'Albanian', flag: 'al' },
  { label: 'Arabic', value: 'Arabic', flag: 'sa' },
  { label: 'Armenian', value: 'Armenian', flag: 'am' },
  { label: 'Azerbaijani', value: 'Azerbaijani', flag: 'az' },
  { label: 'Bengali', value: 'Bengali', flag: 'bd' },
  { label: 'Bulgarian', value: 'Bulgarian', flag: 'bg' },
  { label: 'Chinese (Simplified)', value: 'Chinese (Simplified)', flag: 'cn' },
  { label: 'Chinese (Traditional)', value: 'Chinese (Traditional)', flag: 'cn' },
  { label: 'Croatian', value: 'Croatian', flag: 'hr' },
  { label: 'Czech', value: 'Czech', flag: 'cz' },
  { label: 'Danish', value: 'Danish', flag: 'dk' },
  { label: 'Dutch', value: 'Dutch', flag: 'nl' },
  { label: 'Estonian', value: 'Estonian', flag: 'ee' },
  { label: 'Filipino', value: 'Filipino', flag: 'ph' },
  { label: 'Finnish', value: 'Finnish', flag: 'fi' },
  { label: 'French', value: 'French', flag: 'fr' },
  { label: 'Georgian', value: 'Georgian', flag: 'ge' },
  { label: 'German', value: 'German', flag: 'de' },
  { label: 'Greek', value: 'Greek', flag: 'gr' },
  { label: 'Hebrew', value: 'Hebrew', flag: 'il' },
  { label: 'Hindi', value: 'Hindi', flag: 'in' },
  { label: 'Hungarian', value: 'Hungarian', flag: 'hu' },
  { label: 'Indonesian', value: 'Indonesian', flag: 'id' },
  { label: 'Italian', value: 'Italian', flag: 'it' },
  { label: 'Japanese', value: 'Japanese', flag: 'jp' },
  { label: 'Kazakh', value: 'Kazakh', flag: 'kz' },
  { label: 'Korean', value: 'Korean', flag: 'kr' },
  { label: 'Kyrgyz', value: 'Kyrgyz', flag: 'kg' },
  { label: 'Latvian', value: 'Latvian', flag: 'lv' },
  { label: 'Lithuanian', value: 'Lithuanian', flag: 'lt' },
  { label: 'Macedonian', value: 'Macedonian', flag: 'mk' },
  { label: 'Malay', value: 'Malay', flag: 'my' },
  { label: 'Norwegian', value: 'Norwegian', flag: 'no' },
  { label: 'Persian', value: 'Persian', flag: 'ir' },
  { label: 'Polish', value: 'Polish', flag: 'pl' },
  { label: 'Portuguese (Brazilian)', value: 'Portuguese (Brazilian)', flag: 'br' },
  { label: 'Portuguese (European)', value: 'Portuguese (European)', flag: 'pt' },
  { label: 'Romanian', value: 'Romanian', flag: 'ro' },
  { label: 'Russian', value: 'Russian', flag: 'ru' },
  { label: 'Serbian', value: 'Serbian', flag: 'rs' },
  { label: 'Sinhala', value: 'Sinhala', flag: 'lk' },
  { label: 'Slovak', value: 'Slovak', flag: 'sk' },
  { label: 'Slovenian', value: 'Slovenian', flag: 'si' },
  { label: 'Spanish', value: 'Spanish', flag: 'es' },
  { label: 'Swahili', value: 'Swahili', flag: 'ke' },
  { label: 'Swedish', value: 'Swedish', flag: 'se' },
  { label: 'Tajik', value: 'Tajik', flag: 'tj' },
  { label: 'Thai', value: 'Thai', flag: 'th' },
  { label: 'Turkish', value: 'Turkish', flag: 'tr' },
  { label: 'Turkmen', value: 'Turkmen', flag: 'tm' },
  { label: 'Ukrainian', value: 'Ukrainian', flag: 'ua' },
  { label: 'Urdu', value: 'Urdu', flag: 'pk' },
  { label: 'Uzbek', value: 'Uzbek', flag: 'uz' },
  { label: 'Vietnamese', value: 'Vietnamese', flag: 'vn' }
]

// Methods
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

// Initialize form data if editing existing workflow
if (props.data) {
  formData.keyword = props.data.keyword || ''
  formData.target_market = props.data.target_market || ''
  formData.article_language = props.data.article_language || ''
}
</script>

<style scoped>
.workflow-step {
  max-width: 800px;
  margin: 0 auto;
}

.step-content {
  background: transparent;
  border-radius: 8px;
  padding: 32px;
}

.field-hint {
  margin-top: 4px;
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
  min-height: 56px; /* 根据Ant Design默认按钮高度调整 */
  min-width: 200px; /* 设置最小宽度确保按钮不会太小 */
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
  padding: 16px 32px; /* 调整padding以适应高度 */
  font-size: 16px; /* 稍微调小字体以适合表单 */
  font-weight: 600;
  color: white;
  z-index: 2;
  position: relative;
  min-height: 24px; /* 确保内容区域有合适的高度 */
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

/* 语言选项样式 */
.language-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}

.flag-icon {
  width: 20px;
  height: 15px;
  border-radius: 2px;
  flex-shrink: 0;
  background-size: cover;
  background-position: center;
  border: 1px solid #e8e8e8;
}

.language-name {
  flex: 1;
  font-size: 14px;
  color: #333;
}

/* 选中项样式 */
:deep(.ant-select-selection-item) {
  display: flex !important;
  align-items: center !important;
  height: 100% !important;
}

:deep(.ant-select-selection-item) .language-option {
  gap: 8px;
  display: flex;
  align-items: center;
  width: 100%;
}

:deep(.ant-select-selection-item) .flag-icon {
  width: 16px;
  height: 12px;
}

:deep(.ant-select-selection-item) .language-name {
  font-size: 13px;
  line-height: 1;
}

/* 确保选择框的内容垂直居中 */
:deep(.ant-select-selector) {
  display: flex !important;
  align-items: center !important;
}

:deep(.ant-select-selection-search) {
  display: flex !important;
  align-items: center !important;
}

:deep(.ant-select-selection-placeholder) {
  display: flex !important;
  align-items: center !important;
}

/* 表单标签加粗 */
:deep(.ant-form-item-label) > label {
  font-weight: 600 !important;
}

@media (max-width: 768px) {
  .step-content {
    padding: 20px;
  }
}
</style>