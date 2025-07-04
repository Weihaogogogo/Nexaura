<template>
  <div class="outline-editor">
    <!-- H1 标题容器 -->
    <div class="h1-container">
      <div class="h1-title">
        <span class="title-tag h1-tag">H1</span>
        <span class="title-text">{{ h1Title }}</span>
      </div>
    </div>

    <!-- H2 标题容器列表 -->
    <div class="h2-containers">
      <template v-for="(h2Item, index) in h2Sections" :key="h2Item.id">
        <!-- 插入H2按钮 (在第一个H2之前) -->
        <div 
          v-if="index === 0"
          class="h2-insert-zone"
          @mouseenter="setHoverIndex(index - 0.5)"
          @mouseleave="setHoverIndex(-1)"
        >
          <div 
            class="h2-insert-btn"
            :class="{ visible: hoverIndex === index - 0.5 }"
            @click="insertH2(index)"
          >
            <PlusOutlined />
      </div>
    </div>

        <div 
          class="h2-container-wrapper"
          @mouseenter="setHoverIndex(index)"
          @mouseleave="handleMouseLeave"
        >
          <!-- H2 容器控制按钮 -->
          <div 
            class="h2-controls"
            :class="{ visible: hoverIndex === index }"
            @mouseenter="setHoverIndex(index)"
          >
            <a-button 
              type="text" 
              size="small" 
              :disabled="index === 0"
              @click="moveH2Up(index)"
              class="control-btn"
            >
              <UpOutlined />
            </a-button>
            <a-button 
              type="text" 
              size="small" 
              :disabled="index === h2Sections.length - 1"
              @click="moveH2Down(index)"
              class="control-btn"
            >
              <DownOutlined />
            </a-button>
            <a-popconfirm
              :title="$t('editor.outline.delete_h2_confirm')"
              :ok-text="$t('common.confirm')"
              :cancel-text="$t('common.cancel')"
              @confirm="deleteH2(index)"
            >
              <a-button 
                type="text" 
                size="small" 
                danger
                class="control-btn delete-btn"
              >
                <DeleteOutlined />
              </a-button>
            </a-popconfirm>
          </div>

          <!-- H2 标题容器 -->
          <OutlineItem
            :h2-data="h2Item"
            @update-h2="updateH2Title(index, $event)"
            @update-h3="updateH3Title(index, $event.h3Index, $event.title)"
            @add-h3="addH3(index)"
            @add-h3-at-position="addH3AtPosition(index, $event)"
            @delete-h3="deleteH3(index, $event)"
            @reorder-h3="reorderH3(index, $event)"
          />
    </div>

        <!-- 插入H2按钮 (在每个H2之后) -->
        <div 
          class="h2-insert-zone"
          @mouseenter="setHoverIndex(index + 0.5)"
          @mouseleave="setHoverIndex(-1)"
        >
          <div 
            class="h2-insert-btn"
            :class="{ 
              visible: hoverIndex === index + 0.5 || 
                      hoverIndex === index || 
                      (index < h2Sections.length - 1 && hoverIndex === index + 1)
            }"
            @click="insertH2(index + 1)"
          >
            <PlusOutlined />
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { 
  UpOutlined, 
  DownOutlined, 
  DeleteOutlined, 
  PlusOutlined 
} from '@ant-design/icons-vue'
import OutlineItem from './OutlineItem.vue'

const { t } = useI18n()

interface H3Item {
  id: string
  title: string
}

interface H2Section {
  id: string
  title: string
  h3Items: H3Item[]
}

interface Props {
  modelValue?: string
  h1Title?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 数据
const h1Title = ref(props.h1Title || t('editor.placeholder.h1_title', '文章标题'))
const h2Sections = reactive<H2Section[]>([])
const hoverIndex = ref<number>(-1)

// 生成唯一ID
const generateId = () => Math.random().toString(36).substr(2, 9)

// 解析markdown大纲
const parseOutline = (markdown: string) => {
  if (!markdown) return

  const lines = markdown.split('\n').filter(line => line.trim())
  h2Sections.length = 0

  let currentH2: H2Section | null = null

  lines.forEach(line => {
    const trimmed = line.trim()
    
    if (trimmed.startsWith('## ')) {
      // H2 标题
      const title = trimmed.substring(3).trim()
      currentH2 = {
        id: generateId(),
        title,
        h3Items: []
      }
      h2Sections.push(currentH2)
    } else if (trimmed.startsWith('### ') && currentH2) {
      // H3 标题
      const title = trimmed.substring(4).trim()
      currentH2.h3Items.push({
        id: generateId(),
        title
      })
    }
  })

  // 如果没有H2标题，创建一个默认的
  if (h2Sections.length === 0) {
    insertH2(0)
  }
}

// 生成markdown大纲
const generateOutline = () => {
  const lines: string[] = []
  
  h2Sections.forEach(h2 => {
    if (h2.title.trim()) {
      lines.push(`## ${h2.title.trim()}`)
      
      h2.h3Items.forEach(h3 => {
        if (h3.title.trim()) {
          lines.push(`### ${h3.title.trim()}`)
        }
      })
    }
  })
  
  return lines.join('\n')
}

// H2 标题操作
const updateH2Title = (index: number, title: string) => {
  h2Sections[index].title = title
  emitUpdate()
}

const moveH2Up = (index: number) => {
  if (index > 0) {
    const temp = h2Sections[index]
    h2Sections[index] = h2Sections[index - 1]
    h2Sections[index - 1] = temp
    emitUpdate()
  }
}

const moveH2Down = (index: number) => {
  if (index < h2Sections.length - 1) {
    const temp = h2Sections[index]
    h2Sections[index] = h2Sections[index + 1]
    h2Sections[index + 1] = temp
    emitUpdate()
  }
}

const deleteH2 = (index: number) => {
  h2Sections.splice(index, 1)
  emitUpdate()
}

const insertH2 = (index: number) => {
  h2Sections.splice(index, 0, {
    id: generateId(),
    title: t('editor.placeholder.h2_title'),
    h3Items: [
      {
        id: generateId(),
        title: t('editor.placeholder.h3_title')
      }
    ]
  })
  emitUpdate()
}

// 悬浮状态管理
let hoverTimeout: ReturnType<typeof setTimeout> | null = null

const setHoverIndex = (index: number) => {
  if (hoverTimeout) {
    clearTimeout(hoverTimeout)
    hoverTimeout = null
  }
  hoverIndex.value = index
}

const handleMouseLeave = () => {
  hoverTimeout = setTimeout(() => {
    hoverIndex.value = -1
  }, 100) // 100ms 延迟，避免在快速移动鼠标时误触发
}

// H3 标题操作
const addH3 = (h2Index: number) => {
  h2Sections[h2Index].h3Items.push({
    id: generateId(),
    title: t('editor.placeholder.h3_title')
  })
  emitUpdate()
}

const addH3AtPosition = (h2Index: number, position: number) => {
  h2Sections[h2Index].h3Items.splice(position, 0, {
    id: generateId(),
    title: t('editor.placeholder.h3_title')
  })
  emitUpdate()
}

const updateH3Title = (h2Index: number, h3Index: number, title: string) => {
  h2Sections[h2Index].h3Items[h3Index].title = title
  emitUpdate()
}

const deleteH3 = (h2Index: number, h3Index: number) => {
  h2Sections[h2Index].h3Items.splice(h3Index, 1)
  emitUpdate()
}

const reorderH3 = (h2Index: number, { oldIndex, newIndex }: { oldIndex: number, newIndex: number }) => {
  const h3Items = h2Sections[h2Index].h3Items
  const [removed] = h3Items.splice(oldIndex, 1)
  h3Items.splice(newIndex, 0, removed)
  emitUpdate()
}

// 发出更新事件
const emitUpdate = () => {
  const outline = generateOutline()
  emit('update:modelValue', outline)
}

// 监听外部值变化
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    parseOutline(newValue)
  }
}, { immediate: true })
</script>

<style scoped>
.outline-editor {
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  overflow: visible;
  max-height: none;
}

.h1-container {
  padding: 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e8e8e8;
}

.h1-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 22px;
  font-size: 10px;
  font-weight: 600;
  border-radius: 4px;
  color: white;
}

.h1-tag {
  background: #6366f1;
}

.title-text {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.h2-containers {
  padding: 16px;
  max-height: none;
  overflow: visible;
}

.h2-container-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  align-items: flex-start;
}

.h2-controls {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.h2-controls.visible {
  opacity: 1;
}

.control-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  background: transparent;
}

.control-btn:hover {
  background: #f3f4f6;
  color: #6366f1;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.delete-btn:hover {
  background: #fef2f2;
  color: #ef4444;
}

/* H2插入按钮样式 */
.h2-insert-zone {
  position: relative;
  height: 0;
  display: flex;
  align-items: center;
    justify-content: center;
  margin: 12px 0;
  width: 100%;
}

.h2-insert-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background: transparent;
  color: rgb(139, 92, 246);
  border: 1px solid rgb(139, 92, 246);
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
  font-size: 9px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
}

.h2-insert-btn:hover {
  color: rgb(124, 58, 237);
  border-color: rgb(124, 58, 237);
  background: rgba(139, 92, 246, 0.05);
}

.h2-insert-btn.visible {
  opacity: 1;
}
</style>