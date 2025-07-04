<template>
  <div class="rich-text-editor">
    <div v-if="showToolbar" class="editor-toolbar">
      <div class="toolbar-section">
        <!-- Text Formatting -->
        <a-button-group size="small">
          <a-button 
            @click="editor?.chain().focus().toggleBold().run()"
            :class="{ 'is-active': editor?.isActive('bold') }"
            :disabled="!editor"
          >
            <BoldOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleItalic().run()"
            :class="{ 'is-active': editor?.isActive('italic') }"
            :disabled="!editor"
          >
            <ItalicOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleUnderline().run()"
            :class="{ 'is-active': editor?.isActive('underline') }"
            :disabled="!editor"
          >
            <UnderlineOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleStrike().run()"
            :class="{ 'is-active': editor?.isActive('strike') }"
            :disabled="!editor"
          >
            <StrikethroughOutlined />
          </a-button>
        </a-button-group>
      </div>

      <div class="toolbar-section">
        <!-- Headings -->
        <a-select
          :value="getActiveHeading()"
          @change="setHeading"
          size="small"
          style="width: 120px"
          :disabled="!editor"
        >
          <a-select-option value="paragraph">{{ $t('editor.toolbar.paragraph') }}</a-select-option>
          <a-select-option value="h1">{{ $t('editor.toolbar.heading1') }}</a-select-option>
          <a-select-option value="h2">{{ $t('editor.toolbar.heading2') }}</a-select-option>
          <a-select-option value="h3">{{ $t('editor.toolbar.heading3') }}</a-select-option>
          <a-select-option value="h4">{{ $t('editor.toolbar.heading4') }}</a-select-option>
        </a-select>
      </div>

      <div class="toolbar-section">
        <!-- Lists -->
        <a-button-group size="small">
          <a-button 
            @click="editor?.chain().focus().toggleBulletList().run()"
            :class="{ 'is-active': editor?.isActive('bulletList') }"
            :disabled="!editor"
          >
            <UnorderedListOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleOrderedList().run()"
            :class="{ 'is-active': editor?.isActive('orderedList') }"
            :disabled="!editor"
          >
            <OrderedListOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleTaskList().run()"
            :class="{ 'is-active': editor?.isActive('taskList') }"
            :disabled="!editor"
          >
            <CheckSquareOutlined />
          </a-button>
        </a-button-group>
      </div>

      <div class="toolbar-section">
        <!-- Alignment -->
        <a-button-group size="small">
          <a-button 
            @click="editor?.chain().focus().setTextAlign('left').run()"
            :class="{ 'is-active': editor?.isActive({ textAlign: 'left' }) }"
            :disabled="!editor"
          >
            <AlignLeftOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().setTextAlign('center').run()"
            :class="{ 'is-active': editor?.isActive({ textAlign: 'center' }) }"
            :disabled="!editor"
          >
            <AlignCenterOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().setTextAlign('right').run()"
            :class="{ 'is-active': editor?.isActive({ textAlign: 'right' }) }"
            :disabled="!editor"
          >
            <AlignRightOutlined />
          </a-button>
        </a-button-group>
      </div>

      <div class="toolbar-section">
        <!-- Insert Elements -->
        <a-button-group size="small">
          <a-button 
            @click="showLinkDialog = true"
            :disabled="!editor"
          >
            <LinkOutlined />
          </a-button>
          <a-button 
            @click="insertImage"
            :disabled="!editor"
          >
            <PictureOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleBlockquote().run()"
            :class="{ 'is-active': editor?.isActive('blockquote') }"
            :disabled="!editor"
          >
            <CommentOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().toggleCodeBlock().run()"
            :class="{ 'is-active': editor?.isActive('codeBlock') }"
            :disabled="!editor"
          >
            <CodeOutlined />
          </a-button>
        </a-button-group>
      </div>

      <div class="toolbar-section">
        <!-- Actions -->
        <a-button-group size="small">
          <a-button 
            @click="editor?.chain().focus().undo().run()"
            :disabled="!editor?.can().undo()"
          >
            <UndoOutlined />
          </a-button>
          <a-button 
            @click="editor?.chain().focus().redo().run()"
            :disabled="!editor?.can().redo()"
          >
            <RedoOutlined />
          </a-button>
        </a-button-group>
      </div>
    </div>

    <!-- Editor Content -->
    <div class="editor-wrapper" :class="{ 'readonly': readonly }">
      <EditorContent v-if="editor" :editor="(editor as any)" class="editor-content" />
      
      <div v-if="placeholder && isEmpty" class="editor-placeholder">
        {{ placeholder }}
      </div>
    </div>

    <!-- Status Bar -->
    <div v-if="showStatusBar" class="editor-status-bar">
      <div class="status-left">
        <span class="word-count">
          {{ $t('editor.status.words') }}: {{ wordCount }}
        </span>
        <span class="char-count">
          {{ $t('editor.status.characters') }}: {{ characterCount }}
        </span>
      </div>
      <div class="status-right">
        <span v-if="lastSaved" class="last-saved">
          {{ $t('editor.status.last_saved') }}: {{ formatTime(lastSaved) }}
        </span>
      </div>
    </div>

    <!-- Link Dialog -->
    <a-modal
      v-model:open="showLinkDialog"
      :title="$t('editor.dialogs.insert_link')"
      @ok="insertLink"
      @cancel="linkUrl = ''"
    >
      <a-form layout="vertical">
        <a-form-item :label="$t('editor.dialogs.link_url')">
          <a-input
            v-model:value="linkUrl"
            :placeholder="$t('editor.dialogs.link_url_placeholder')"
            @keyup.enter="insertLink"
          />
        </a-form-item>
        <a-form-item :label="$t('editor.dialogs.link_text')">
          <a-input
            v-model:value="linkText"
            :placeholder="$t('editor.dialogs.link_text_placeholder')"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Placeholder from '@tiptap/extension-placeholder'
import TaskList from '@tiptap/extension-task-list'
import TaskItem from '@tiptap/extension-task-item'
import TextAlign from '@tiptap/extension-text-align'
import Underline from '@tiptap/extension-underline'
import {
  BoldOutlined,
  ItalicOutlined,
  UnderlineOutlined,
  StrikethroughOutlined,
  UnorderedListOutlined,
  OrderedListOutlined,
  CheckSquareOutlined,
  AlignLeftOutlined,
  AlignCenterOutlined,
  AlignRightOutlined,
  LinkOutlined,
  PictureOutlined,
  CommentOutlined,
  CodeOutlined,
  UndoOutlined,
  RedoOutlined
} from '@ant-design/icons-vue'

interface Props {
  modelValue?: string
  placeholder?: string
  readonly?: boolean
  showToolbar?: boolean
  showStatusBar?: boolean
  autoSave?: boolean
  autoSaveInterval?: number
  minHeight?: string
  maxHeight?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '',
  readonly: false,
  showToolbar: true,
  showStatusBar: true,
  autoSave: false,
  autoSaveInterval: 5000,
  minHeight: '200px',
  maxHeight: '500px'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'save': [content: string]
  'change': [content: string]
}>()

const { t } = useI18n()

// Editor instance
const editor = ref<Editor | null>(null)

// UI state
const showLinkDialog = ref(false)
const linkUrl = ref('')
const linkText = ref('')
const lastSaved = ref<Date | null>(null)

// Auto-save
let autoSaveTimer: ReturnType<typeof setInterval> | null = null

// Computed properties
const isEmpty = computed(() => {
  if (!editor.value) return true
  return editor.value.isEmpty
})

const wordCount = computed(() => {
  if (!editor.value) return 0
  const text = editor.value.getText()
  return text.trim() ? text.trim().split(/\s+/).length : 0
})

const characterCount = computed(() => {
  if (!editor.value) return 0
  return editor.value.getCharacterCount()
})

// Toolbar helpers
const getActiveHeading = () => {
  if (!editor.value) return 'paragraph'
  
  if (editor.value.isActive('heading', { level: 1 })) return 'h1'
  if (editor.value.isActive('heading', { level: 2 })) return 'h2'
  if (editor.value.isActive('heading', { level: 3 })) return 'h3'
  if (editor.value.isActive('heading', { level: 4 })) return 'h4'
  
  return 'paragraph'
}

const setHeading = (value: string) => {
  if (!editor.value) return
  
  if (value === 'paragraph') {
    editor.value.chain().focus().setParagraph().run()
  } else {
    const level = parseInt(value.replace('h', '')) as 1 | 2 | 3 | 4 | 5 | 6
    editor.value.chain().focus().toggleHeading({ level }).run()
  }
}

// Link functions
const insertLink = () => {
  if (!editor.value || !linkUrl.value) return
  
  const selection = editor.value.state.selection
  const hasSelection = !selection.empty
  
  if (hasSelection) {
    // Use selected text
    editor.value.chain().focus().setLink({ href: linkUrl.value }).run()
  } else {
    // Insert new link with text
    const text = linkText.value || linkUrl.value
    editor.value.chain().focus().insertContent(`<a href="${linkUrl.value}">${text}</a>`).run()
  }
  
  showLinkDialog.value = false
  linkUrl.value = ''
  linkText.value = ''
}

// Image functions
const insertImage = () => {
  const url = prompt(t('editor.dialogs.image_url_prompt'))
  if (url && editor.value) {
    editor.value.chain().focus().setImage({ src: url }).run()
  }
}

// Auto-save functions
const startAutoSave = () => {
  if (!props.autoSave) return
  
  autoSaveTimer = setInterval(() => {
    if (editor.value) {
      const content = editor.value.getHTML()
      emit('save', content)
      lastSaved.value = new Date()
    }
  }, props.autoSaveInterval)
}

const stopAutoSave = () => {
  if (autoSaveTimer) {
    clearInterval(autoSaveTimer)
    autoSaveTimer = null
  }
}

// Utility functions
const formatTime = (date: Date) => {
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const seconds = date.getSeconds().toString().padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

// Watch for external content changes
watch(() => props.modelValue, (newValue) => {
  if (editor.value && newValue !== editor.value.getHTML()) {
    editor.value.commands.setContent(newValue, false)
  }
})

// Initialize editor
onMounted(() => {
  editor.value = new Editor({
    content: props.modelValue,
    editable: !props.readonly,
    extensions: [
      StarterKit,
      Image.configure({
        HTMLAttributes: {
          class: 'editor-image'
        }
      }),
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'editor-link'
        }
      }),
      Placeholder.configure({
        placeholder: props.placeholder
      }),
      TaskList.configure({
        HTMLAttributes: {
          class: 'task-list'
        }
      }),
      TaskItem.configure({
        nested: true,
        HTMLAttributes: {
          class: 'task-item'
        }
      }),
      TextAlign.configure({
        types: ['heading', 'paragraph']
      }),
      Underline
    ],
    onUpdate: ({ editor }) => {
      const content = editor.getHTML()
      emit('update:modelValue', content)
      emit('change', content)
    },
    editorProps: {
      attributes: {
        style: `min-height: ${props.minHeight}; max-height: ${props.maxHeight};`
      }
    }
  })
  
  if (props.autoSave) {
    startAutoSave()
  }
})

// Cleanup
onUnmounted(() => {
  stopAutoSave()
  if (editor.value) {
    editor.value.destroy()
  }
})

// Expose editor instance for parent components
defineExpose({
  editor,
  focus: () => editor.value?.commands.focus(),
  blur: () => editor.value?.commands.blur(),
  clear: () => editor.value?.commands.clearContent(),
  getHTML: () => editor.value?.getHTML() || '',
  getText: () => editor.value?.getText() || '',
  getJSON: () => editor.value?.getJSON(),
  setContent: (content: string) => editor.value?.commands.setContent(content),
  insertContent: (content: string) => editor.value?.commands.insertContent(content),
  wordCount,
  characterCount
})
</script>

<style scoped>
.rich-text-editor {
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  background: white;
  overflow: hidden;
}

.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-section:not(:last-child)::after {
  content: '';
  width: 1px;
  height: 20px;
  background: #d9d9d9;
  margin-left: 8px;
}

.editor-wrapper {
  position: relative;
  min-height: 200px;
}

.editor-wrapper.readonly {
  background: #f5f5f5;
}

.editor-content {
  padding: 16px;
  outline: none;
}

.editor-placeholder {
  position: absolute;
  top: 16px;
  left: 16px;
  color: #bfbfbf;
  pointer-events: none;
  font-size: 14px;
}

.editor-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #fafafa;
  border-top: 1px solid #f0f0f0;
  font-size: 12px;
  color: #8c8c8c;
}

.status-left,
.status-right {
  display: flex;
  gap: 16px;
}

.is-active {
  background: #e6f7ff !important;
  border-color: #91d5ff !important;
  color: #1890ff !important;
}

/* Editor content styles */
.editor-content :deep(.ProseMirror) {
  outline: none;
  line-height: 1.6;
}

.editor-content :deep(.ProseMirror h1) {
  font-size: 28px;
  font-weight: 600;
  margin: 24px 0 16px 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror h2) {
  font-size: 24px;
  font-weight: 600;
  margin: 20px 0 12px 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror h3) {
  font-size: 20px;
  font-weight: 600;
  margin: 16px 0 8px 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror h4) {
  font-size: 18px;
  font-weight: 600;
  margin: 12px 0 8px 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror p) {
  margin: 8px 0;
}

.editor-content :deep(.ProseMirror ul),
.editor-content :deep(.ProseMirror ol) {
  margin: 12px 0;
  padding-left: 24px;
}

.editor-content :deep(.ProseMirror li) {
  margin: 4px 0;
}

.editor-content :deep(.ProseMirror blockquote) {
  border-left: 3px solid #d9d9d9;
  margin: 16px 0;
  padding-left: 16px;
  color: #8c8c8c;
  font-style: italic;
}

.editor-content :deep(.ProseMirror code) {
  background: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.editor-content :deep(.ProseMirror pre) {
  background: #f5f5f5;
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  overflow-x: auto;
}

.editor-content :deep(.ProseMirror pre code) {
  background: none;
  padding: 0;
}

.editor-content :deep(.editor-image) {
  max-width: 100%;
  height: auto;
  margin: 16px 0;
  border-radius: 6px;
}

.editor-content :deep(.editor-link) {
  color: #1890ff;
  text-decoration: none;
}

.editor-content :deep(.editor-link:hover) {
  text-decoration: underline;
}

.editor-content :deep(.task-list) {
  list-style: none;
  padding-left: 0;
}

.editor-content :deep(.task-item) {
  display: flex;
  align-items: center;
  margin: 4px 0;
}

.editor-content :deep(.task-item input) {
  margin-right: 8px;
}

@media (max-width: 768px) {
  .editor-toolbar {
    padding: 8px;
    gap: 4px;
  }
  
  .toolbar-section {
    gap: 2px;
  }
  
  .editor-content {
    padding: 12px;
  }
  
  .status-left,
  .status-right {
    gap: 8px;
  }
}
</style>