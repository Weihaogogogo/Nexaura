<template>
  <div class="workflow-step">
    <!-- Word Count Display -->
    <div v-if="articleContent" class="word-count-display">
      {{ t('workflow.step6.word_count', { count: formatNumber(wordCount) }) }}
    </div>
    
    <div class="step-content">
      <!-- Article Content -->
      <div class="article-container">
        <div class="article-header">
          <h1 class="article-title">{{ articleTitle || t('workflow.step6.article_title_fallback') }}</h1>
        </div>

        <!-- Debug Info (开发时显示) -->
        <div v-if="!articleContent" class="debug-info" style="padding: 16px; background: #f0f0f0; margin: 16px; border-radius: 4px; font-family: monospace; font-size: 12px;">
          <p><strong>Debug Info:</strong></p>
          <p>Data exists: {{ !!props.data }}</p>
          <p>Markdown content exists: {{ !!markdownContent }}</p>
          <p>Available keys: {{ props.data ? Object.keys(props.data).join(', ') : 'None' }}</p>
          <div v-if="props.data" style="margin-top: 8px;">
            <p><strong>Markdown content fields (优先级顺序):</strong></p>
            <p>gen_final_article_content: {{ props.data.gen_final_article_content ? 'EXISTS' : 'MISSING' }}</p>
            <p>final_article_content: {{ props.data.final_article_content ? 'EXISTS' : 'MISSING' }}</p>
            <p>gen_article_content: {{ props.data.gen_article_content ? 'EXISTS' : 'MISSING' }}</p>
            <p>article_content: {{ props.data.article_content ? 'EXISTS' : 'MISSING' }}</p>
            <p>gen_optimized_article_content: {{ props.data.gen_optimized_article_content ? 'EXISTS' : 'MISSING' }}</p>
          </div>
          <div v-if="markdownContent" style="margin-top: 8px; padding: 8px; background: #e0e0e0; border-radius: 4px;">
            <p><strong>Markdown 内容预览 (前200字符):</strong></p>
            <pre style="white-space: pre-wrap; word-wrap: break-word;">{{ markdownContent.substring(0, 200) }}{{ markdownContent.length > 200 ? '...' : '' }}</pre>
          </div>
        </div>

        <!-- Content Display -->
        <div class="article-content" v-if="articleContent">
          <div 
            class="content-html"
            v-html="articleContent"
          ></div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-content">
          <a-empty 
            :description="t('workflow.step6.content_generating')"
            :image="h(FileTextOutlined)"
          />
        </div>
        </div>
      </div>

    <!-- Fixed Action Buttons -->
    <div class="fixed-actions">
      <div class="actions-container">
        <a-button 
          size="large"
          @click="createNewWorkflow"
        >
          {{ t('workflow.step6.create_new_article') }}
        </a-button>
        <a-button 
          type="primary"
          size="large"
          @click="goToLibrary"
        >
          {{ t('workflow.step6.enter_article_editor') }}
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { marked } from 'marked'
import { FileTextOutlined, FileWordOutlined } from '@ant-design/icons-vue'
import type { WorkflowState } from '@/types/workflow'

// 字数统计函数
const countWords = (text: string, locale: string): number => {
  if (!text) return 0
  
  // 移除HTML标签和实体
  const cleanText = text
    .replace(/<[^>]*>/g, ' ') // 移除HTML标签
    .replace(/&[^;]+;/g, ' ') // 移除HTML实体
    .replace(/\s+/g, ' ') // 合并多个空格
    .trim()
  
  if (!cleanText) return 0
  
  if (locale === 'zh') {
    // 中文字数统计：统计汉字、数字、字母数量
    // 汉字
    const chineseChars = cleanText.match(/[\u4e00-\u9fff]/g) || []
    // 英文单词和数字
    const englishWords = cleanText.replace(/[\u4e00-\u9fff]/g, ' ')
      .split(/\s+/)
      .filter(word => word.trim().length > 0)
    
    return chineseChars.length + englishWords.length
  } else {
    // 英文单词统计：按空格分割，忽略中文字符
    const words = cleanText.split(/\s+/).filter(word => word.trim().length > 0)
    return words.length
  }
}

interface Props {
  data?: WorkflowState | null
}

const props = defineProps<Props>()
const router = useRouter()
const { t, locale } = useI18n()

// Computed
// 获取文章标题
const articleTitle = computed(() => {
  return props.data?.article_title || ''
})

// 原始Markdown内容
const markdownContent = computed(() => {
  if (!props.data) {
    console.log('Step6: No data provided')
    return ''
  }
  
  console.log('Step6: Data received:', props.data)
  console.log('Step6: All data keys:', Object.keys(props.data))
  
  // 优先查找Markdown格式的内容
  const possibleMarkdownFields = [
    'gen_final_article_content',
    'final_article_content',
    'gen_article_content', 
    'article_content',
    'gen_optimized_article_content'
  ]
  
  for (const field of possibleMarkdownFields) {
    let value = props.data[field as keyof WorkflowState] as string
    console.log(`Step6: ${field}:`, value ? `Content length: ${value.length}` : 'MISSING')
    if (value) {
      // 移除 H1 标题（# 开头的行）
      value = value.split('\n').filter(line => {
        const trimmed = line.trim()
        return !trimmed.startsWith('# ') && trimmed !== '#'
      }).join('\n')
      
      return value
  }
}

  console.log('Step6: No markdown content found in any field')
  return ''
})

// 解析后的HTML内容
const articleContent = computed(() => {
  if (!markdownContent.value) {
    return ''
  }
  
  try {
    // 配置marked选项
    marked.setOptions({
      breaks: true, // 支持换行
      gfm: true, // 支持GitHub风格markdown
    })
    
    const html = marked.parse(markdownContent.value) as string
    console.log('Step6: Markdown parsed successfully, HTML length:', html.length)
    return html
  } catch (error) {
    console.error('Step6: Error parsing markdown:', error)
    return `<div class="error-message">
      <h3>${t('workflow.step6.markdown_parse_error')}</h3>
      <p>${error}</p>
      <details>
        <summary>${t('workflow.step6.original_content')}</summary>
        <pre>${markdownContent.value}</pre>
      </details>
    </div>`
  }
})

// 字数统计
const wordCount = computed(() => {
  if (!articleContent.value) return 0
  return countWords(articleContent.value, locale.value)
})

// 格式化数字（添加千位分隔符）
const formatNumber = (num: number): string => {
  return num.toLocaleString()
}

// Methods
const createNewWorkflow = () => {
  router.push('/app/workflow/new')
}

const goToLibrary = () => {
  // 如果有session_id，直接跳转到该文章的详情页，并设置为编辑模式
  if (props.data?.session_id) {
    router.push({
      path: `/app/articles/${props.data.session_id}`,
      query: { mode: 'edit' }
    })
  } else {
    // 否则跳转到文章列表页
  router.push('/app/articles')
  }
}
</script>

<style scoped>
.workflow-step {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
}

/* Word Count Display */
.word-count-display {
  position: absolute;
  top: 0;
  left: 0;
  padding: 8px 0;
  font-size: 14px;
  font-weight: normal;
  color: #666;
  z-index: 10;
  display: flex;
  align-items: center;
}

.step-content {
  background: transparent;
  border-radius: 8px;
  padding: 32px;
  padding-bottom: 100px; /* 为固定按钮留出空间 */
}

.article-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 24px;
}

.article-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
}

.article-title {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.3;
}

.article-content {
  padding: 24px;
  min-height: 400px;
  /* 移除max-height限制，允许全量显示 */
}

.content-html {
  line-height: 1.8;
  font-size: 16px;
  color: #333;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 错误信息样式 */
:deep(.error-message) {
  padding: 20px;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 6px;
  color: #a8071a;
}

:deep(.error-message h3) {
  color: #cf1322;
  margin-top: 0;
}

:deep(.error-message details) {
  margin-top: 16px;
}

:deep(.error-message pre) {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}



.empty-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}



/* 固定在底部的按钮容器 */
.fixed-actions {
  position: fixed;
  bottom: 0;
  left: 240px; /* sidebar宽度240px + 边框1px = 241px */
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid #e8e8e8;
  padding: 16px 0;
  z-index: 1000;
}

.actions-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 0 32px;
}

/* 创建新文章按钮 - glass效果 */
.actions-container .ant-btn:not(.ant-btn-primary) {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 12px;
  font-weight: 600;
  min-height: 48px;
  min-width: 140px;
  position: relative;
  overflow: hidden;
  transition: all 0.2s ease;
}

.actions-container .ant-btn:not(.ant-btn-primary):hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 进入文章编辑器按钮 - 紫色主题glass效果 */
.actions-container .ant-btn-primary {
  background: linear-gradient(135deg, #5b5ff1, #7c3aed);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  min-height: 48px;
  min-width: 160px;
  position: relative;
  overflow: hidden;
  transition: all 0.2s ease;
}

.actions-container .ant-btn-primary:hover {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

/* 光效动画 */
.actions-container .ant-btn-primary::before {
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

.actions-container .ant-btn-primary:hover::before {
  left: 100%;
}

/* Article content styling */
:deep(.content-html h1),
:deep(.content-html h2),
:deep(.content-html h3),
:deep(.content-html h4),
:deep(.content-html h5),
:deep(.content-html h6) {
  color: #1a1a1a;
  margin: 24px 0 16px 0;
  font-weight: 600;
}

:deep(.content-html h1) {
  font-size: 32px;
  border-bottom: 2px solid #e8e8e8;
  padding-bottom: 8px;
}

:deep(.content-html h2) {
  font-size: 24px;
}

:deep(.content-html h3) {
  font-size: 20px;
}

:deep(.content-html p) {
  margin: 16px 0;
  line-height: 1.8;
}

:deep(.content-html ul),
:deep(.content-html ol) {
  margin: 16px 0;
  padding-left: 24px;
}

:deep(.content-html li) {
  margin: 8px 0;
  line-height: 1.6;
}

:deep(.content-html blockquote) {
  border-left: 4px solid #1890ff;
  background: #f6f8fa;
  padding: 16px 20px;
  margin: 16px 0;
  border-radius: 0 6px 6px 0;
}

:deep(.content-html code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
}

:deep(.content-html img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
    flex-direction: column;
    padding: 0 20px;
  }
  
  .actions-container .ant-btn {
    width: 100%;
  }
  
  .article-title {
    font-size: 24px; /* 移动端调小字体 */
  }
  
  /* 移动端字数统计样式 */
  .word-count-display {
    position: static;
    margin-bottom: 16px;
    text-align: center;
  }
}
</style>