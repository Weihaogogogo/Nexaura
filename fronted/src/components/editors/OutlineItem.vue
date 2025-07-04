<template>
  <div class="outline-item">
    <!-- H2 标题部分 -->
    <div class="h2-section">
      <div class="h2-title">
        <span class="title-tag h2-tag">H2</span>
        <a-input
          v-model:value="localH2Title"
          class="h2-input"
          :placeholder="$t('editor.placeholder.h2_title')"
          @blur="updateH2Title"
          @pressEnter="updateH2Title"
        />
      </div>
    </div>
    
    <!-- H3 标题部分 -->
    <div class="h3-section">
      <Draggable
        v-if="localH3Items.length > 0"
        :list="localH3Items"
        :group="{ name: 'h3-items' }"
        item-key="id"
        class="h3-list"
        ghost-class="h3-ghost"
        chosen-class="h3-chosen"
        drag-class="h3-drag"
        handle=".drag-handle"
        @end="onH3Reorder"
      >
        <template #item="{ element, index }">
          <div 
            class="h3-item" 
            :key="element.id"
            @mouseenter="setHoverH3Index(index)"
            @mouseleave="setHoverH3Index(-1)"
          >
            <!-- 拖拽手柄 -->
            <div class="drag-handle">
              <HolderOutlined />
            </div>
            
            <!-- H3 标题 -->
            <div class="h3-title">
              <span class="title-tag h3-tag">H3</span>
              <a-input
                v-model:value="element.title"
                class="h3-input"
                :placeholder="$t('editor.placeholder.h3_title')"
                @blur="updateH3Title(index, element.title)"
                @pressEnter="updateH3Title(index, element.title)"
              />
            </div>
            
            <!-- H3 操作按钮 -->
            <div class="h3-actions" :class="{ visible: hoverH3Index === index }">
              <a-button 
                type="text" 
                size="small" 
                @click="addH3Below(index)"
                class="action-btn"
              >
                <PlusOutlined />
              </a-button>
              <a-popconfirm
                :title="$t('editor.outline.delete_confirm')"
                :ok-text="$t('common.confirm')"
                :cancel-text="$t('common.cancel')"
                @confirm="deleteH3(index)"
              >
                <a-button 
                  type="text" 
                  size="small" 
                  danger
                  class="action-btn"
                >
                  <DeleteOutlined />
                </a-button>
              </a-popconfirm>
            </div>
          </div>
        </template>
      </Draggable>

      <!-- 添加H3按钮 -->
      <div class="add-h3-container">
        <a-button 
          type="text" 
          size="small"
          @click="addH3"
          class="add-h3-btn"
        >
          <PlusOutlined />
          {{ $t('editor.outline.add_h3') }}
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  HolderOutlined, 
  PlusOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'
import Draggable from 'vuedraggable'

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
  h2Data: H2Section
}

interface Emits {
  (e: 'update-h2', title: string): void
  (e: 'update-h3', data: { h3Index: number, title: string }): void
  (e: 'add-h3'): void
  (e: 'add-h3-at-position', position: number): void
  (e: 'delete-h3', h3Index: number): void
  (e: 'reorder-h3', data: { oldIndex: number, newIndex: number }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { t } = useI18n()

// 本地数据
const localH2Title = ref(props.h2Data.title)
const localH3Items = reactive([...props.h2Data.h3Items])
const hoverH3Index = ref<number>(-1)

// 监听外部数据变化
watch(() => props.h2Data, (newData) => {
  localH2Title.value = newData.title
  localH3Items.splice(0, localH3Items.length, ...newData.h3Items)
}, { deep: true })

// H2 标题更新
const updateH2Title = () => {
  emit('update-h2', localH2Title.value)
}

// H3 标题更新
const updateH3Title = (index: number, title: string) => {
  emit('update-h3', { h3Index: index, title })
}

// 添加H3
const addH3 = () => {
  emit('add-h3')
}

// 在指定位置下方添加H3
const addH3Below = (index: number) => {
  emit('add-h3-at-position', index + 1)
}

// 删除H3
const deleteH3 = (index: number) => {
  emit('delete-h3', index)
}

// H3 重新排序
const onH3Reorder = (evt: any) => {
  if (evt.oldIndex !== evt.newIndex) {
    emit('reorder-h3', {
      oldIndex: evt.oldIndex,
      newIndex: evt.newIndex
    })
  }
}

// H3 悬浮状态管理
const setHoverH3Index = (index: number) => {
  hoverH3Index.value = index
}
</script>

<style scoped>
.outline-item {
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  overflow: hidden;
  flex: 1;
}

.h2-section {
  padding: 12px 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e8e8e8;
}

.h2-title {
  display: flex;
  align-items: center;
  gap: 10px;
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
  flex-shrink: 0;
}

.h2-tag {
  background: #8b5cf6;
}

.h3-tag {
  background: #10b981;
}

.h2-input, .h3-input {
  flex: 1;
  font-weight: 500;
}

.h2-input {
  font-size: 16px;
}

.h3-input {
  font-size: 14px;
}

.h3-section {
  padding: 4px 12px 8px 12px;
}

.h3-list {
  min-height: 0;
}

.h3-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  margin-bottom: 6px;
  background: white;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.h3-item:hover {
  background: #f9fafb;
}

.drag-handle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  color: #9ca3af;
  cursor: grab;
  flex-shrink: 0;
}

.drag-handle:hover {
  color: #6b7280;
}

.drag-handle:active {
  cursor: grabbing;
}

.h3-title {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.h3-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.h3-actions.visible {
  opacity: 1;
}

.action-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 4px;
}

.action-btn:hover {
  background: #f3f4f6;
}

.add-h3-container {
  margin-top: 4px;
  text-align: center;
}

.add-h3-btn {
  height: 24px;
  padding: 0 8px;
  color: #9ca3af;
  font-size: 11px;
  border: none;
  transition: all 0.2s ease;
}

.add-h3-btn:hover {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}



/* 拖拽状态样式 */
.h3-ghost {
  opacity: 0.5;
  background: #e0e7ff;
  border: 2px dashed #8b5cf6;
}

.h3-chosen {
  background: #f3f4f6;
  transform: scale(1.02);
}

.h3-drag {
  transform: rotate(2deg);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 输入框样式优化 */
:deep(.ant-input) {
  border: 1px solid transparent;
  background: transparent;
  transition: all 0.2s ease;
}

:deep(.ant-input:hover) {
  border-color: #d1d5db;
  background: white;
}

:deep(.ant-input:focus) {
  border-color: #8b5cf6;
  background: white;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1);
}

/* H2 输入框特殊样式 */
.h2-input :deep(.ant-input) {
  font-weight: 600;
  font-size: 16px;
}

/* H3 输入框特殊样式 */
.h3-input :deep(.ant-input) {
  font-size: 14px;
}
</style>