<template>
  <div class="article-detail-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-section">
      <a-spin size="large" :tip="t('articles.detail.loading')" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-section">
      <a-result
        status="error"
        :title="t('articles.detail.load_failed')"
        :sub-title="error"
      >
        <template #extra>
          <a-button type="primary" @click="goBack">{{ t('articles.detail.back_list') }}</a-button>
          <a-button @click="loadArticle">{{ t('articles.detail.retry') }}</a-button>
        </template>
      </a-result>
    </div>

    <!-- Article Content -->
    <div v-else-if="article" class="article-layout">
      <!-- Header Navigation -->
      <div class="article-header">
        <a-button 
          type="text" 
          :icon="h(ArrowLeftOutlined)"
          @click="goBack"
          class="back-button"
        >
          {{ t('articles.detail.back_list') }}
        </a-button>
        
        <div class="header-actions">
          <a-button 
            type="default" 
            :icon="h(CopyOutlined)"
            @click="copyContent"
          >
            {{ t('articles.detail.copy_content') }}
          </a-button>
          <a-dropdown>
            <a-button 
              type="default" 
              :icon="h(DownloadOutlined)"
            >
              {{ t('articles.detail.download_article') }}
            </a-button>
            <template #overlay>
              <a-menu @click="handleDownloadMenuClick">
                <a-menu-item key="markdown">
                  <span>{{ t('articles.detail.download_markdown') }}</span>
                </a-menu-item>
                <a-menu-item key="html-embedded">
                  <span>{{ t('articles.detail.download_html_embedded') }}</span>
                </a-menu-item>
                <a-menu-item key="html-package">
                  <span>{{ t('articles.detail.download_html_package') }}</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>

      <!-- Main Layout -->
      <div class="main-layout">
        <!-- Left Content - Article -->
        <div class="left-content">
          <div class="article-content-section">
            <!-- Article Title -->
            <div class="article-title-section">
              <h1 class="article-title">{{ article.article_title }}</h1>
              <div class="article-meta">
                <span class="word-count">
                  {{ t('articles.detail.word_count', { count: formatNumber(wordCount) }) }}
                </span>
                <a-tag :color="getLanguageColor(article.article_language)">
                  {{ article.article_language }}
                </a-tag>
                <a-tag color="blue">{{ article.target_market.toUpperCase() }}</a-tag>
                <a-tag color="green">{{ article.keyword }}</a-tag>
                <span class="timestamp">
                  <ClockCircleOutlined />
                  {{ formatDate(article.updated_time) }}
                </span>
              </div>
            </div>

            <!-- Article Content -->
            <div class="article-content">
              <!-- Display Mode Toggle -->
              <div class="display-controls">
                <a-radio-group 
                  v-model:value="displayMode" 
                  size="small"
                  button-style="solid"
                  @change="handleModeChange"
                >
                  <a-radio-button value="preview">{{ t('articles.detail.mode.preview') }}</a-radio-button>
                  <a-radio-button value="edit">{{ t('articles.detail.mode.edit') }}</a-radio-button>
                </a-radio-group>
              </div>

              <!-- Preview Mode -->
              <div 
                v-if="displayMode === 'preview'"
                class="content-html"
                v-html="previewHtmlContent"
              ></div>
              
              <!-- Edit Mode -->
              <div 
                v-else-if="displayMode === 'edit'"
                class="content-editor"
              >
                <WysiwygEditor
                  v-model="editableContent"
                  height="600px"
                  placeholder="请输入文章内容..."
                  :show-save-button="true"
                  :has-unsaved-changes="hasUnsavedChanges"
                  :saving="saving"
                  @save="saveArticle"
                />
              </div>
              
              <!-- Fallback Content -->
              <div v-else class="content-empty">
                <a-empty :description="t('articles.detail.no_content')" />
              </div>
            </div>
          </div>
        </div>

        <!-- Right Sidebar - SEO Info -->
        <div class="right-sidebar">
          <div class="sidebar-content">
            <h3 class="sidebar-title">{{ t('articles.detail.seo.title') }}</h3>
            
            <!-- SEO Title Card -->
            <div v-if="article.seo_title || article.article_title" class="info-card">
              <div class="card-header">
                <h4 class="card-title">{{ t('articles.detail.seo.seo_title') }}</h4>
                <a-button 
                  type="text" 
                  size="small"
                  @click="copyField(t('articles.detail.seo.seo_title'), seoTitle)"
                  :icon="h(CopyOutlined)"
                  class="copy-btn"
                >
                  {{ t('articles.detail.seo.copy') }}
                </a-button>
              </div>
              <div class="card-content">
                <p class="field-value">{{ seoTitle }}</p>
                <span class="field-hint">{{ seoTitle.length }}/70 {{ t('articles.detail.seo.characters') }}</span>
              </div>
            </div>

            <!-- Article Description Card -->
            <div v-if="article.article_description" class="info-card">
              <div class="card-header">
                <h4 class="card-title">{{ t('articles.detail.seo.description') }}</h4>
                <a-button 
                  type="text" 
                  size="small"
                  @click="copyField(t('articles.detail.seo.description'), article.article_description)"
                  :icon="h(CopyOutlined)"
                  class="copy-btn"
                >
                  {{ t('articles.detail.seo.copy') }}
                </a-button>
              </div>
              <div class="card-content">
                <p class="field-value">{{ article.article_description }}</p>
              </div>
            </div>

            <!-- URL Example Card -->
            <div v-if="article.url_example" class="info-card">
              <div class="card-header">
                <h4 class="card-title">{{ t('articles.detail.seo.url_example') }}</h4>
                <a-button 
                  type="text" 
                  size="small"
                  @click="copyField(t('articles.detail.seo.url_example'), article.url_example)"
                  :icon="h(CopyOutlined)"
                  class="copy-btn"
                >
                  {{ t('articles.detail.seo.copy') }}
                </a-button>
              </div>
              <div class="card-content">
                <p class="field-value url-value">{{ article.url_example }}</p>
              </div>
            </div>

            <!-- Additional Info -->
            <div class="additional-info">
              <div class="info-item">
                <span class="label">{{ t('articles.detail.seo.created_time') }}:</span>
                <span class="value">{{ formatDate(article.created_time) }}</span>
              </div>
              <div class="info-item">
                <span class="label">{{ t('articles.detail.seo.updated_time') }}:</span>
                <span class="value">{{ formatDate(article.updated_time) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { 
  ArrowLeftOutlined,
  CopyOutlined,
  DownloadOutlined,
  ClockCircleOutlined
} from '@ant-design/icons-vue'
import { marked } from 'marked'
import { generationApi } from '@/services/api/generation'
import type { ArticleDetailResponse } from '@/services/api/generation'
import WysiwygEditor from '@/components/editors/WysiwygEditor.vue'
import JSZip from 'jszip'
import { saveAs } from 'file-saver'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

// 字数统计函数 (与 WorkflowStep6 相同)
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

// State
const article = ref<ArticleDetailResponse | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const displayMode = ref<'preview' | 'edit'>('preview')
const editableContent = ref('')
const hasUnsavedChanges = ref(false)
const saving = ref(false)
const originalContent = ref('')

// Computed
const seoTitle = computed(() => {
  if (!article.value) return ''
  return article.value.seo_title || article.value.article_title || ''
})

// Function to remove the first h1 from markdown content
const removeFirstH1FromMarkdown = (markdownContent: string): string => {
  if (!markdownContent) return ''
  
  const lines = markdownContent.split('\n')
  const firstLineIndex = lines.findIndex(line => line.trim().startsWith('# '))
  
  if (firstLineIndex !== -1) {
    // Remove the first h1 line
    lines.splice(firstLineIndex, 1)
    // Also remove any immediately following empty lines
    while (firstLineIndex < lines.length && lines[firstLineIndex].trim() === '') {
      lines.splice(firstLineIndex, 1)
    }
  }
  
  return lines.join('\n').trim()
}

// Parse markdown to HTML
const parseMarkdownToHtml = (markdownContent: string): string => {
  if (!markdownContent) return ''
  
  try {
    // Configure marked options
    marked.setOptions({
      breaks: true, // 支持换行
      gfm: true, // 支持GitHub风格markdown
    })
    
    return marked.parse(markdownContent) as string
  } catch (error) {
    console.error('Error parsing markdown:', error)
    return markdownContent
  }
}

// Get clean markdown content (from API, without H1)
const cleanMarkdownContent = computed(() => {
  if (!article.value?.final_article_content) return ''
  return removeFirstH1FromMarkdown(article.value.final_article_content)
})

// Preview HTML content (generated from current edited content)
const previewHtmlContent = computed(() => {
  const contentToRender = editableContent.value || cleanMarkdownContent.value
  return parseMarkdownToHtml(contentToRender)
})

// Original content for copy/download (with H1)
const originalMarkdownContent = computed(() => {
  return article.value?.final_article_content || ''
})

// 字数统计
const wordCount = computed(() => {
  if (!previewHtmlContent.value) return 0
  return countWords(previewHtmlContent.value, locale.value)
})

// 格式化数字（添加千位分隔符）
const formatNumber = (num: number): string => {
  return num.toLocaleString()
}

// Methods
const loadArticle = async () => {
  try {
    loading.value = true
    error.value = null
    
    const sessionId = parseInt(route.params.id as string)
    if (isNaN(sessionId)) {
      throw new Error(t('articles.detail.invalid_id'))
    }
    
    const response = await generationApi.getArticleDetail(sessionId)
    article.value = response
    
    // Initialize editable content
    const cleanContent = removeFirstH1FromMarkdown(response.final_article_content || '')
    editableContent.value = cleanContent
    originalContent.value = cleanContent
    hasUnsavedChanges.value = false
    
  } catch (err: any) {
    console.error('Failed to load article:', err)
    error.value = err.message || t('articles.detail.load_error')
  } finally {
    loading.value = false
  }
}

const handleModeChange = () => {
  // When switching to edit mode, ensure content is loaded
  if (displayMode.value === 'edit' && !editableContent.value && article.value) {
    const cleanContent = removeFirstH1FromMarkdown(article.value.final_article_content || '')
    editableContent.value = cleanContent
    originalContent.value = cleanContent
  }
}

const handleContentChange = () => {
  hasUnsavedChanges.value = editableContent.value !== originalContent.value
}

const saveArticle = async () => {
  if (!article.value || !hasUnsavedChanges.value) return
  
  try {
    saving.value = true
    
    // Add H1 title back for saving
    const titleLine = `# ${article.value.article_title}\n\n`
    const fullContent = titleLine + editableContent.value
    
    await generationApi.modifyArticle(article.value.session_id.toString(), fullContent)
    
    // Update local state
    originalContent.value = editableContent.value
    hasUnsavedChanges.value = false
    
    message.success(t('articles.detail.save_success'))
    
    // Switch to preview mode to show saved content
    displayMode.value = 'preview'
    
  } catch (error: any) {
    console.error('Failed to save article:', error)
    message.error(error.message || t('articles.detail.save_failed'))
  } finally {
    saving.value = false
  }
}

const copyField = async (fieldName: string, value: string) => {
  try {
    await navigator.clipboard.writeText(value)
    message.success(t('articles.detail.seo.copy_field_success', { field: fieldName }))
  } catch (error) {
    message.error(t('articles.detail.copy_failed'))
  }
}

const copyContent = async () => {
  if (!article.value) return
  
  try {
    // Always copy the complete content (including h1)
    const content = originalMarkdownContent.value
    
    await navigator.clipboard.writeText(content)
    message.success(t('articles.detail.copy_success'))
  } catch (error) {
    message.error(t('articles.detail.copy_failed'))
  }
}

// 将图片URL转换为base64编码
const convertImageToBase64 = async (imageUrl: string): Promise<string> => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      
      if (!ctx) {
        reject(new Error('Cannot get canvas context'))
        return
      }
      
      canvas.width = img.width
      canvas.height = img.height
      ctx.drawImage(img, 0, 0)
      
      try {
        const dataURL = canvas.toDataURL('image/jpeg', 0.8)
        resolve(dataURL)
      } catch (error) {
        reject(error)
      }
    }
    
    img.onerror = () => {
      reject(new Error(`Failed to load image: ${imageUrl}`))
    }
    
    img.src = imageUrl
  })
}

// 提取HTML中的图片URLs
const extractImageUrls = (html: string): string[] => {
  const imgRegex = /<img[^>]+src="([^"]+)"/g
  const urls: string[] = []
  let match
  
  while ((match = imgRegex.exec(html)) !== null) {
    urls.push(match[1])
  }
  
  return urls
}

// 下载图片并返回blob
const downloadImageAsBlob = async (imageUrl: string): Promise<Blob> => {
  const response = await fetch(imageUrl)
  if (!response.ok) {
    throw new Error(`Failed to download image: ${imageUrl}`)
  }
  return response.blob()
}

// 获取图片文件名
const getImageFileName = (imageUrl: string): string => {
  const url = new URL(imageUrl)
  const pathname = url.pathname
  const fileName = pathname.split('/').pop() || 'image'
  
  // 如果没有扩展名，默认添加.jpg
  if (!fileName.includes('.')) {
    return `${fileName}.jpg`
  }
  
  return fileName
}

const handleDownloadMenuClick = (e: any) => {
  if (!article.value) return
  
  const key = e.key
  if (key === 'markdown') {
    downloadContent('markdown')
  } else if (key === 'html-embedded') {
    downloadContent('html-embedded')
  } else if (key === 'html-package') {
    downloadContent('html-package')
  }
}

const downloadContent = async (format: string) => {
  if (!article.value) return
  
  try {
    if (format === 'markdown') {
      // Download current content (if edited, use edited content)
      let content = originalMarkdownContent.value
      if (hasUnsavedChanges.value) {
        // If there are unsaved changes, include them in download
        const titleLine = `# ${article.value.article_title}\n\n`
        content = titleLine + editableContent.value
      }
      
      const title = article.value.article_title || 'article'
      const filename = `${title.replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')}.md`
      
      const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      message.success(t('articles.detail.download_success', { format: 'MARKDOWN' }))
      
    } else if (format === 'html-embedded') {
      // Convert markdown to HTML with embedded base64 images
      message.loading(t('articles.detail.processing_images'), 0)
      
      let markdownContent = originalMarkdownContent.value
      if (hasUnsavedChanges.value) {
        const titleLine = `# ${article.value.article_title}\n\n`
        markdownContent = titleLine + editableContent.value
      }
      
      // Parse markdown to HTML
      let htmlContent = parseMarkdownToHtml(markdownContent)
      
      // Extract image URLs
      const imageUrls = extractImageUrls(htmlContent)
      
      if (imageUrls.length > 0) {
        // Convert images to base64
        const imagePromises = imageUrls.map(async (imageUrl) => {
          try {
            const base64Data = await convertImageToBase64(imageUrl)
            return { url: imageUrl, base64: base64Data }
          } catch (error) {
            console.warn(`Failed to convert image to base64: ${imageUrl}`, error)
            return { url: imageUrl, base64: null }
          }
        })
        
        const imageResults = await Promise.all(imagePromises)
        
        // Replace image URLs with base64 data
        imageResults.forEach(({ url, base64 }) => {
          if (base64) {
            htmlContent = htmlContent.replace(new RegExp(`src="${url}"`, 'g'), `src="${base64}"`)
          }
        })
      }
      
      // Create a complete HTML document
      const content = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${article.value.article_title}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1a1a1a;
            margin: 24px 0 16px 0;
            font-weight: 600;
        }
        h1 {
            font-size: 32px;
            border-bottom: 2px solid #e8e8e8;
            padding-bottom: 8px;
        }
        h2 { font-size: 24px; }
        h3 { font-size: 20px; }
        p { margin: 16px 0; line-height: 1.8; }
        blockquote {
            border-left: 4px solid #1890ff;
            background: #f6f8fa;
            padding: 16px 20px;
            margin: 16px 0;
            border-radius: 0 6px 6px 0;
        }
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 16px 0;
        }
    </style>
</head>
<body>
${htmlContent}
</body>
</html>`
      
      message.destroy()
      
      const title = article.value.article_title || 'article'
      const filename = `${title.replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')}-embedded.html`
      
      const blob = new Blob([content], { type: 'text/html;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      message.success(t('articles.detail.download_success', { format: 'HTML (嵌入图片)' }))
      
    } else if (format === 'html-package') {
      // Create ZIP package with HTML and images
      message.loading(t('articles.detail.creating_package'), 0)
      
      let markdownContent = originalMarkdownContent.value
      if (hasUnsavedChanges.value) {
        const titleLine = `# ${article.value.article_title}\n\n`
        markdownContent = titleLine + editableContent.value
      }
      
      // Parse markdown to HTML
      let htmlContent = parseMarkdownToHtml(markdownContent)
      
      // Extract image URLs
      const imageUrls = extractImageUrls(htmlContent)
      
      // Create ZIP archive
      const zip = new JSZip()
      const imageFolder = zip.folder('images')
      
      if (!imageFolder) {
        throw new Error('Failed to create images folder in ZIP')
      }
      
      if (imageUrls.length > 0) {
        // Download images and add to ZIP
        const imagePromises = imageUrls.map(async (imageUrl, index) => {
          try {
            const imageBlob = await downloadImageAsBlob(imageUrl)
            const fileName = getImageFileName(imageUrl)
            const uniqueFileName = `image_${index + 1}_${fileName}`
            
            imageFolder.file(uniqueFileName, imageBlob)
            
            // Update HTML to use relative path
            htmlContent = htmlContent.replace(
              new RegExp(`src="${imageUrl}"`, 'g'), 
              `src="images/${uniqueFileName}"`
            )
            
            return uniqueFileName
          } catch (error) {
            console.warn(`Failed to download image: ${imageUrl}`, error)
            return null
          }
        })
        
        await Promise.all(imagePromises)
      }
      
      // Create HTML content with relative image paths
      const htmlWithRelativePaths = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${article.value.article_title}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1a1a1a;
            margin: 24px 0 16px 0;
            font-weight: 600;
        }
        h1 {
            font-size: 32px;
            border-bottom: 2px solid #e8e8e8;
            padding-bottom: 8px;
        }
        h2 { font-size: 24px; }
        h3 { font-size: 20px; }
        p { margin: 16px 0; line-height: 1.8; }
        blockquote {
            border-left: 4px solid #1890ff;
            background: #f6f8fa;
            padding: 16px 20px;
            margin: 16px 0;
            border-radius: 0 6px 6px 0;
        }
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 16px 0;
        }
    </style>
</head>
<body>
${htmlContent}
</body>
</html>`
      
      // Add HTML file to ZIP
      zip.file('article.html', htmlWithRelativePaths)
      
      // Add README file
      const readmeContent = `文章包说明
==================

这个包包含以下文件：
- article.html: 文章的HTML文件
- images/: 图片文件夹，包含文章中使用的所有图片

使用方法：
1. 解压这个ZIP文件到一个文件夹
2. 打开 article.html 文件即可在浏览器中查看完整的文章

注意：请保持 images 文件夹和 article.html 文件在同一个目录下，否则图片可能无法正常显示。

文章标题：${article.value.article_title}
生成时间：${new Date().toLocaleString('zh-CN')}
`
      
      zip.file('README.txt', readmeContent)
      
      // Generate ZIP and download
      const zipBlob = await zip.generateAsync({ type: 'blob' })
      
      message.destroy()
      
      const title = article.value.article_title || 'article'
      const filename = `${title.replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')}-package.zip`
      
      saveAs(zipBlob, filename)
      
      message.success(t('articles.detail.download_success', { format: 'HTML+图片包' }))
    }
    
  } catch (error) {
    message.destroy()
    console.error('Download error:', error)
    message.error(t('articles.detail.download_failed'))
  }
}

const goBack = () => {
  router.push('/app/articles')
}

const getLanguageColor = (language: string): string => {
  const colors: Record<string, string> = {
    'english': 'blue',
    'chinese': 'red',
    'spanish': 'orange',
    'french': 'purple',
    'german': 'green'
  }
  return colors[language.toLowerCase()] || 'default'
}

const formatDate = (dateString: string): string => {
  try {
    // Handle YYYY-MM-DD HH:MM:SS format
    if (dateString && dateString.includes(' ')) {
      const [datePart, timePart] = dateString.split(' ')
      const [year, month, day] = datePart.split('-')
      const [hour, minute] = timePart.split(':')
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute))
      
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Fallback for other formats
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

// Watch for content changes to detect unsaved changes
watch(editableContent, () => {
  hasUnsavedChanges.value = editableContent.value !== originalContent.value
}, { deep: true })

// Lifecycle
onMounted(() => {
  loadArticle()
  
  // 检查URL查询参数，如果mode=edit则自动切换到编辑模式
  if (route.query.mode === 'edit') {
    displayMode.value = 'edit'
  }
})
</script>

<style scoped>
.article-detail-page {
  min-height: calc(100vh - 64px);
  background: #f5f5f5;
}

.loading-section,
.error-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.article-layout {
  max-width: 1600px;
  margin: 0 auto;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  margin: 0 24px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
  position: sticky;
  top: 0;
  z-index: 10;
  border-radius: 12px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.main-layout {
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
}

.left-content {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.article-content-section {
  padding: 32px;
}

.article-title-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.article-title {
  font-size: 36px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.3;
  margin: 0 0 16px 0;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.word-count {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #999;
  margin-right: 12px;
}

.timestamp {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #999;
}

.article-content {
  position: relative;
}

.display-controls {
  position: absolute;
  top: -60px;
  right: 0;
  z-index: 5;
}

.content-html {
  line-height: 1.8;
  font-size: 16px;
  color: #333;
  min-height: 400px;
}

.content-editor {
  /* WysiwygEditor has its own styling */
}

.content-empty {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.right-sidebar {
  width: 380px;
  flex-shrink: 0;
}

.sidebar-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 24px;
  position: sticky;
  top: 100px;
}

.sidebar-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.info-card {
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  margin-bottom: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.card-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.copy-btn {
  padding: 4px 8px;
  height: auto;
  font-size: 12px;
  color: rgb(128, 96, 244);
  border-radius: 4px;
}

.copy-btn:hover {
  background: rgba(128, 96, 244, 0.1);
  color: rgba(128, 96, 244, 0.8);
}

.card-content {
  padding: 12px 16px;
}

.field-value {
  margin: 0 0 8px 0;
  color: #333;
  line-height: 1.5;
  word-wrap: break-word;
  word-break: break-word;
}

.field-hint {
  font-size: 12px;
  color: #999;
}

.url-value {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  color: #333;
}

.additional-info {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
}

.info-item .label {
  color: #666;
  font-weight: 500;
}

.info-item .value {
  color: #333;
}

/* Article content styling */
:deep(.content-html h1),
:deep(.content-html h2),
:deep(.content-html h3),
:deep(.content-html h4),
:deep(.content-html h5),
:deep(.content-html h6) {
  color: #1a1a1a;
  margin: 32px 0 16px 0;
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

/* Responsive Design */
@media (max-width: 1200px) {
  .main-layout {
    flex-direction: column;
    gap: 20px;
  }
  
  .right-sidebar {
    width: 100%;
  }
  
  .sidebar-content {
    position: static;
  }
}

@media (max-width: 768px) {
  .article-layout {
    padding: 0;
  }
  
  .article-header {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .main-layout {
    padding: 16px;
    gap: 16px;
  }
  
  .article-content-section {
    padding: 20px;
  }
  
  .article-title {
    font-size: 28px;
  }
  
  .display-controls {
    position: static;
    margin-bottom: 16px;
    text-align: center;
  }
  
  .sidebar-content {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .article-title {
    font-size: 24px;
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}

/* 自定义预览/编辑模式按钮的激活状态颜色 */
:deep(.ant-radio-group) .ant-radio-button-wrapper-checked {
  background: rgb(128, 96, 244) !important;
  border-color: rgb(128, 96, 244) !important;
  color: white !important;
}

:deep(.ant-radio-group) .ant-radio-button-wrapper-checked:hover {
  background: rgba(128, 96, 244, 0.8) !important;
  border-color: rgba(128, 96, 244, 0.8) !important;
}

:deep(.ant-radio-group) .ant-radio-button-wrapper-checked:before {
  background-color: rgb(128, 96, 244) !important;
}

:deep(.ant-radio-group) .ant-radio-button-wrapper:hover {
  color: rgb(128, 96, 244) !important;
}

</style>