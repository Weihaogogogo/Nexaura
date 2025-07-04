<template>
  <div class="wysiwyg-editor">
    <!-- Toolbar -->
    <div class="editor-toolbar" v-if="editor" ref="toolbarRef" :class="{ 'is-sticky': isToolbarSticky }">
      <div class="toolbar-group">
        <!-- 标题 -->
        <select 
          class="heading-select"
          @change="setHeading(($event.target as HTMLSelectElement).value)"
        >
          <option value="">{{ $t('editor.toolbar.paragraph') }}</option>
          <option value="1">{{ $t('editor.toolbar.heading1') }}</option>
          <option value="2">{{ $t('editor.toolbar.heading2') }}</option>
          <option value="3">{{ $t('editor.toolbar.heading3') }}</option>
          <option value="4">{{ $t('editor.toolbar.heading4') }}</option>
        </select>
      </div>
      
      <div class="toolbar-divider"></div>
      
      <div class="toolbar-group">
        <!-- 格式化 -->
        <button 
          type="button"
          @click="editor.chain().focus().toggleBold().run()"
          :class="{ 'is-active': editor.isActive('bold') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.bold')"
        >
          <strong>B</strong>
        </button>
        <button 
          type="button"
          @click="editor.chain().focus().toggleItalic().run()"
          :class="{ 'is-active': editor.isActive('italic') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.italic')"
        >
          <em>I</em>
        </button>
        <button 
          type="button"
          @click="editor.chain().focus().toggleUnderline().run()"
          :class="{ 'is-active': editor.isActive('underline') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.underline')"
        >
          <u>U</u>
        </button>
        <button 
          type="button"
          @click="editor.chain().focus().toggleStrike().run()"
          :class="{ 'is-active': editor.isActive('strike') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.strikethrough')"
        >
          <s>S</s>
        </button>
      </div>
      
      <div class="toolbar-divider"></div>
      
      <div class="toolbar-group">
        <!-- 列表 -->
        <button 
          type="button"
          @click="editor.chain().focus().toggleBulletList().run()"
          :class="{ 'is-active': editor.isActive('bulletList') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.bullet_list')"
        >
          • {{ $t('editor.toolbar.bullet_list') }}
        </button>
        <button 
          type="button"
          @click="editor.chain().focus().toggleOrderedList().run()"
          :class="{ 'is-active': editor.isActive('orderedList') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.ordered_list')"
        >
          1. {{ $t('editor.toolbar.ordered_list') }}
        </button>

      </div>
      
      <div class="toolbar-divider"></div>
      
      <div class="toolbar-group">
        <!-- 其他 -->
        <button 
          type="button"
          @click="editor.chain().focus().toggleBlockquote().run()"
          :class="{ 'is-active': editor.isActive('blockquote') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.blockquote')"
        >
          ❝ {{ $t('editor.toolbar.blockquote') }}
        </button>
        <button 
          type="button"
          @click="editor.chain().focus().toggleCodeBlock().run()"
          :class="{ 'is-active': editor.isActive('codeBlock') }"
          class="toolbar-btn"
          :title="$t('editor.toolbar.code_block')"
        >
          &lt;/&gt; {{ $t('editor.toolbar.code_block') }}
        </button>
        <button 
          type="button"
          @click="addImage"
          class="toolbar-btn"
          :title="$t('editor.toolbar.image')"
        >
          🖼 {{ $t('editor.toolbar.image') }}
        </button>
        <button 
          type="button"
          @click="addLink"
          class="toolbar-btn"
          :title="$t('editor.toolbar.link')"
        >
          🔗 {{ $t('editor.toolbar.link') }}
        </button>
      </div>
      
      <div class="toolbar-divider"></div>
      
      <div class="toolbar-group">
        <!-- 表格 -->
        <button 
          type="button"
          @click="insertTable"
          class="toolbar-btn"
          :title="$t('editor.toolbar.table')"
        >
          📊 {{ $t('editor.toolbar.table') }}
        </button>
      </div>
      
      <!-- Spacer to push save button to the right -->
      <div class="toolbar-spacer"></div>
      
      <!-- Save Button -->
      <div v-if="showSaveButton" class="toolbar-group">
        <button 
          type="button"
          @click="handleSave"
          :disabled="!hasUnsavedChanges || saving"
          class="toolbar-btn save-btn"
          :class="{ 'is-saving': saving }"
        >
          <Document style="width: 14px; height: 14px; margin-right: 4px;" />
          <span>{{ saving ? $t('editor.toolbar.saving') : $t('editor.toolbar.save') }}</span>
        </button>
      </div>
    </div>
    
    <!-- 工具栏占位元素，防止固定定位时布局跳跃 -->
    <div 
      v-if="isToolbarSticky" 
      class="toolbar-placeholder"
      :style="{ height: `${toolbarOriginalRect.height}px` }"
    ></div>
    
    <!-- Editor Content -->
    <div class="editor-content-wrapper">
      <EditorContent :editor="editor" class="editor-content" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableHeader from '@tiptap/extension-table-header'
import TableCell from '@tiptap/extension-table-cell'

import Highlight from '@tiptap/extension-highlight'
import Underline from '@tiptap/extension-underline'
import { marked } from 'marked'
import TurndownService from 'turndown'
import { Document } from '@element-plus/icons-vue'

const { t } = useI18n()

interface Props {
  modelValue: string
  placeholder?: string
  height?: string
  showSaveButton: boolean
  hasUnsavedChanges: boolean
  saving: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'save'): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  height: '400px',
  showSaveButton: false,
  hasUnsavedChanges: false,
  saving: false
})

const emit = defineEmits<Emits>()

const editor = ref<Editor>()
const isUpdatingFromProp = ref(false)
const updateTimer = ref<number | null>(null)
const toolbarRef = ref<HTMLElement>()
const isToolbarSticky = ref(false)
const toolbarOriginalTop = ref(0)
const toolbarOriginalRect = ref({
  width: 0,
  height: 0,
  left: 0
})
const navbarHeight = ref(0) // 动态获取navbar高度
const toolbarObserver = ref<ResizeObserver | null>(null)
const scrollTimer = ref<number | null>(null)

// 获取navbar的真实高度
const getNavbarHeight = () => {
  const navbar = document.querySelector('.global-navbar') as HTMLElement
  if (navbar) {
    navbarHeight.value = navbar.offsetHeight
  } else {
    // 如果找不到navbar，使用默认值
    navbarHeight.value = 56
  }
}

// 配置 Turndown 服务
const turndownService = new TurndownService({
  headingStyle: 'atx',
  bulletListMarker: '-',
  codeBlockStyle: 'fenced'
})

// Markdown 转 HTML
const markdownToHtml = (markdown: string): string => {
  if (!markdown) return ''
  
  try {
    marked.setOptions({
      breaks: true,
      gfm: true,
    })
    
    return marked.parse(markdown) as string
  } catch (error) {
    console.error('Error parsing markdown:', error)
    return markdown
  }
}

// HTML 转 Markdown
const htmlToMarkdown = (html: string): string => {
  if (!html) return ''
  
  try {
    return turndownService.turndown(html)
  } catch (error) {
    console.error('Error converting HTML to markdown:', error)
    return html
  }
}

// 设置标题级别
const setHeading = (level: string) => {
  if (!editor.value) return
  
  if (level === '') {
    editor.value.chain().focus().setParagraph().run()
  } else {
    editor.value.chain().focus().toggleHeading({ level: parseInt(level) as any }).run()
  }
}

// 添加图片
const addImage = () => {
  if (!editor.value) return
  
  const url = window.prompt(t('editor.dialogs.image_url_prompt'))
  if (url) {
    editor.value.chain().focus().setImage({ src: url }).run()
  }
}

// 添加链接
const addLink = () => {
  if (!editor.value) return
  
  const url = window.prompt(t('editor.dialogs.link_url_prompt'))
  if (url) {
    const text = window.prompt(t('editor.dialogs.link_text_prompt'), url)
    if (text) {
      editor.value
        .chain()
        .focus()
        .insertContent(`<a href="${url}">${text}</a>`)
        .run()
    }
  }
}

// 插入表格
const insertTable = () => {
  if (!editor.value) return
  
  editor.value
    .chain()
    .focus()
    .insertTable({ rows: 3, cols: 3, withHeaderRow: true })
    .run()
}

// 处理保存
const handleSave = () => {
  emit('save')
}

// 获取工具栏的原始位置和尺寸
const updateToolbarPosition = () => {
  if (!toolbarRef.value) return
  
  // 更新navbar高度
  getNavbarHeight()
  
  // 临时重置样式以获取真实位置和尺寸
  const originalStyle = toolbarRef.value.style.cssText
  toolbarRef.value.style.position = 'relative'
  toolbarRef.value.style.top = 'auto'
  toolbarRef.value.style.left = 'auto'
  toolbarRef.value.style.right = 'auto'
  toolbarRef.value.style.zIndex = 'auto'
  toolbarRef.value.style.width = 'auto'
  toolbarRef.value.style.height = 'auto' // 重置高度
  
  // 获取位置和尺寸
  const rect = toolbarRef.value.getBoundingClientRect()
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  
  toolbarOriginalTop.value = rect.top + scrollTop
  toolbarOriginalRect.value = {
    width: rect.width,
    height: rect.height,
    left: rect.left
  }
  
  // 恢复样式
  toolbarRef.value.style.cssText = originalStyle
}

// 监听滚动事件，实现工具栏粘性定位
const handleScroll = () => {
  if (!toolbarRef.value) return
  
  // 添加防抖，避免滚动时频繁计算
  if (scrollTimer.value) {
    clearTimeout(scrollTimer.value)
  }
  
  // 立即检查状态变化，但延迟位置更新
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const shouldBeSticky = scrollTop >= (toolbarOriginalTop.value - navbarHeight.value)
  
  // 状态变化时立即响应
  if (shouldBeSticky !== isToolbarSticky.value) {
    isToolbarSticky.value = shouldBeSticky
    updateToolbarStickyPosition()
  } else {
    // 非状态变化时使用防抖
    scrollTimer.value = window.setTimeout(() => {
      if (shouldBeSticky && isToolbarSticky.value) {
        updateToolbarStickyPosition()
      }
    }, 10)
  }
}

// 更新工具栏粘性位置的独立函数
const updateToolbarStickyPosition = () => {
  if (!toolbarRef.value) return
  
  if (isToolbarSticky.value) {
    // 获取父容器的当前位置和尺寸
    const parentRect = toolbarRef.value.parentElement?.getBoundingClientRect()
    if (parentRect) {
      // 设置为固定定位，使用left和right来确保宽度准确
      toolbarRef.value.style.position = 'fixed'
      toolbarRef.value.style.top = `${navbarHeight.value}px`
      toolbarRef.value.style.left = `${parentRect.left}px`
      toolbarRef.value.style.right = `${window.innerWidth - parentRect.right}px`
      toolbarRef.value.style.width = 'auto' // 让宽度自动计算
      toolbarRef.value.style.zIndex = '1000'
    }
  } else {
    // 恢复原始定位
    toolbarRef.value.style.position = 'relative'
    toolbarRef.value.style.top = 'auto'
    toolbarRef.value.style.left = 'auto'
    toolbarRef.value.style.right = 'auto'
    toolbarRef.value.style.zIndex = 'auto'
    toolbarRef.value.style.width = 'auto'
    toolbarRef.value.style.height = 'auto'
  }
}

onMounted(() => {
  // 延迟初始化，确保DOM完全渲染
  setTimeout(() => {
    editor.value = new Editor({
      extensions: [
        StarterKit,
        Image.configure({
          HTMLAttributes: {
            class: 'editor-image',
          },
        }),
        Link.configure({
          openOnClick: false,
          HTMLAttributes: {
            class: 'editor-link',
          },
        }),
        Table.configure({
          resizable: true,
        }),
        TableRow,
        TableHeader,
        TableCell,
        Highlight,
        Underline,
      ],
      content: markdownToHtml(props.modelValue),
      editorProps: {
        attributes: {
          class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none',
          style: `min-height: ${props.height}; padding: 16px;`,
        },
      },
      onUpdate: ({ editor }) => {
        if (isUpdatingFromProp.value) return
        
        // 添加防抖，避免频繁更新
        if (updateTimer.value) {
          clearTimeout(updateTimer.value)
        }
        
        updateTimer.value = window.setTimeout(() => {
          const html = editor.getHTML()
          const markdown = htmlToMarkdown(html)
          emit('update:modelValue', markdown)
        }, 300) // 300ms防抖
      },
    })
    
    // 初始化工具栏位置
    setTimeout(() => {
      updateToolbarPosition()
      handleScroll() // 初始检查
      
      // 添加ResizeObserver来监听工具栏大小变化
      if (toolbarRef.value && 'ResizeObserver' in window) {
        toolbarObserver.value = new ResizeObserver(() => {
          // 当工具栏大小变化时，重新计算位置
          setTimeout(() => {
            updateToolbarPosition()
            handleScroll()
          }, 50)
        })
        toolbarObserver.value.observe(toolbarRef.value)
      }
    }, 200)
  }, 100)
  
  // 添加滚动监听
  window.addEventListener('scroll', handleScroll)
  // 添加窗口大小变化监听，重新计算位置
  window.addEventListener('resize', updateToolbarPosition)
})

onBeforeUnmount(() => {
  if (updateTimer.value) {
    clearTimeout(updateTimer.value)
  }
  if (scrollTimer.value) {
    clearTimeout(scrollTimer.value)
  }
  if (editor.value) {
    editor.value.destroy()
  }
  // 清理ResizeObserver
  if (toolbarObserver.value) {
    toolbarObserver.value.disconnect()
    toolbarObserver.value = null
  }
  // 移除滚动监听
  window.removeEventListener('scroll', handleScroll)
  // 移除窗口大小变化监听
  window.removeEventListener('resize', updateToolbarPosition)
})

// 监听 props 变化，更新编辑器内容
watch(() => props.modelValue, (newValue) => {
  if (!editor.value || isUpdatingFromProp.value) return
  
  // 获取当前编辑器的markdown内容
  const currentHtml = editor.value.getHTML()
  const currentMarkdown = htmlToMarkdown(currentHtml)
  
  // 只有当内容真正不同时才更新
  if (currentMarkdown !== newValue) {
    const newHtml = markdownToHtml(newValue)
    
    // 保存当前光标位置
    const { from, to } = editor.value.state.selection
    
    isUpdatingFromProp.value = true
    editor.value.commands.setContent(newHtml, false, { preserveWhitespace: 'full' })
    
    // 尝试恢复光标位置
    setTimeout(() => {
      if (editor.value && from !== undefined) {
        try {
          // 确保位置在有效范围内
          const maxPos = editor.value.state.doc.content.size
          const safeFrom = Math.min(from, maxPos)
          const safeTo = Math.min(to, maxPos)
          
          editor.value.commands.setTextSelection({
            from: safeFrom,
            to: safeTo
          })
        } catch (e) {
          // 如果无法恢复位置，则保持当前位置
          console.warn('Could not restore cursor position:', e)
        }
      }
      isUpdatingFromProp.value = false
    }, 0)
  }
}, { immediate: true })
</script>

<style scoped>
.wysiwyg-editor {
  /* 移除边框，保持简洁 */
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fafafa;
  border: 1px solid #e8e8e8;
  flex-wrap: wrap;
  border-radius: 8px;
  position: relative;
  transition: box-shadow 0.2s ease;
  min-height: 48px; /* 确保有最小高度 */
  box-sizing: border-box; /* 确保padding被计算在内 */
}

.editor-toolbar.is-sticky {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-bottom: 1px solid #d9d9d9;
  border-radius: 8px; /* 固定时只保留下方圆角 */
  /* 在粘性状态下保持稳定的高度 */
  min-height: 48px;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-divider {
  width: 1px;
  height: 24px;
  background: #e8e8e8;
}

.toolbar-spacer {
  flex: 1;
}

.heading-select {
  padding: 4px 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
  font-size: 14px;
  min-width: 80px;
}

.toolbar-btn {
  padding: 6px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
  white-space: nowrap;
}

.toolbar-btn:hover {
  background: #f0f0f0;
  border-color: #1890ff;
}

.toolbar-btn.is-active {
  background: #e6f7ff;
  border-color: #1890ff;
  color: #1890ff;
}

.toolbar-btn.save-btn {
  background: rgb(128, 96, 244);
  color: white;
  border-color: rgb(128, 96, 244);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toolbar-btn.save-btn:hover:not(:disabled) {
  background: rgba(128, 96, 244, 0.8);
  border-color: rgba(128, 96, 244, 0.8);
}

.toolbar-btn.save-btn:disabled {
  background: #f5f5f5;
  color: #bfbfbf;
  border-color: #d9d9d9;
  cursor: not-allowed;
}

.toolbar-btn.save-btn.is-saving {
  background: rgb(128, 96, 244);
  border-color: rgb(128, 96, 244);
}

.editor-content-wrapper {
  min-height: 400px;
  /* 移除最大高度限制，让内容可以全部显示 */
}

.editor-content {
  width: 100%;
}

/* 编辑器内容样式 */
:deep(.ProseMirror) {
  outline: none;
  padding: 16px;
  line-height: 1.6;
  color: #333;
  min-height: 400px;
}

:deep(.ProseMirror h1) {
  font-size: 32px;
  font-weight: 700;
  margin: 24px 0 16px 0;
  color: #1a1a1a;
  border-bottom: 2px solid #e8e8e8;
  padding-bottom: 8px;
}

:deep(.ProseMirror h2) {
  font-size: 24px;
  font-weight: 600;
  margin: 20px 0 12px 0;
  color: #1a1a1a;
}

:deep(.ProseMirror h3) {
  font-size: 20px;
  font-weight: 600;
  margin: 16px 0 8px 0;
  color: #1a1a1a;
}

:deep(.ProseMirror h4) {
  font-size: 18px;
  font-weight: 600;
  margin: 12px 0 6px 0;
  color: #1a1a1a;
}

:deep(.ProseMirror p) {
  margin: 8px 0;
  line-height: 1.8;
}

:deep(.ProseMirror ul, .ProseMirror ol) {
  margin: 12px 0;
  padding-left: 24px;
}

:deep(.ProseMirror li) {
  margin: 4px 0;
  line-height: 1.6;
}

:deep(.ProseMirror blockquote) {
  border-left: 4px solid #1890ff;
  background: #f6f8fa;
  padding: 16px 20px;
  margin: 16px 0;
  border-radius: 0 6px 6px 0;
  font-style: italic;
}

:deep(.ProseMirror pre) {
  background: #f8f9fa;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
}

:deep(.ProseMirror code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
}

:deep(.ProseMirror .editor-image) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.ProseMirror .editor-link) {
  color: #1890ff;
  text-decoration: underline;
}

:deep(.ProseMirror table) {
  border-collapse: collapse;
  margin: 16px 0;
  width: 100%;
  border: 2px solid #d9d9d9; /* 表格外边框 */
  border-radius: 6px;
  overflow: hidden;
}

:deep(.ProseMirror th, .ProseMirror td) {
  border: 1px solid #d9d9d9; /* 加深边框颜色 */
  padding: 12px 16px; /* 增加内边距 */
  text-align: left;
  vertical-align: top;
  background: white;
}

:deep(.ProseMirror th) {
  background: #f8f9fa; /* 稍微调整表头背景色 */
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #d9d9d9; /* 表头底部加粗边框 */
}

:deep(.ProseMirror td) {
  min-width: 100px; /* 设置最小宽度 */
  min-height: 40px; /* 设置最小高度，让空单元格也可见 */
  position: relative;
}

/* 给空单元格添加占位符 */
:deep(.ProseMirror td:empty::before) {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  min-height: 20px;
}

/* 表格悬浮效果 */
:deep(.ProseMirror table:hover) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.ProseMirror td:hover) {
  background: #f0f7ff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .editor-toolbar {
    padding: 8px 12px;
    gap: 4px;
  }
  
  .toolbar-btn {
    padding: 4px 6px;
    font-size: 11px;
  }
  
  .heading-select {
    min-width: 60px;
    font-size: 12px;
  }
  
  :deep(.ProseMirror) {
    padding: 12px;
  }
  
  :deep(.ProseMirror h1) {
    font-size: 24px;
  }
  
  :deep(.ProseMirror h2) {
    font-size: 20px;
  }
  
  :deep(.ProseMirror h3) {
    font-size: 18px;
  }
}

.toolbar-placeholder {
  width: 100%;
  background: transparent;
}
</style> 