<template>
  <el-dropdown 
    @command="handleLanguageChange"
    trigger="click"
    class="language-selector"
  >
    <el-button 
      text 
      class="language-button"
      :class="{ 'in-header': inHeader }"
    >
      {{ currentLocale.name }}
      <el-icon class="el-icon--right">
        <ArrowDown />
      </el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item 
          v-for="locale in supportedLocales" 
          :key="locale.code"
          :command="locale.code"
          :class="{ 'is-active': locale.code === currentLanguage }"
        >
          <div class="language-option">
            <span class="name">{{ locale.name }}</span>
          </div>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton, ElIcon } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { supportedLocales, setLocale } from '@/plugins/i18n'

interface Props {
  inHeader?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  inHeader: false
})

const { locale } = useI18n()

const currentLanguage = computed(() => locale.value)

const currentLocale = computed(() => {
  return supportedLocales.find(l => l.code === currentLanguage.value) || supportedLocales[0]
})

const handleLanguageChange = (command: string) => {
  setLocale(command)
}
</script>

<style scoped>
.language-selector {
  margin-left: 12px;
}

.language-button {
  color: var(--el-text-color-primary);
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.language-button:hover {
  background-color: var(--el-fill-color-light);
}

.language-button.in-header {
  color: rgba(255, 255, 255, 0.9);
}

.language-button.in-header:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name {
  font-size: 14px;
}

.is-active {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.el-dropdown-menu__item.is-active:hover {
  background-color: var(--el-color-primary-light-8);
}
</style> 