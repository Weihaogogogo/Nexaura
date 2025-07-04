<template>
  <div class="not-found-page">
    <a-result
      status="404"
      :title="$t('error.404.title')"
      :sub-title="$t('error.404.subtitle')"
    >
      <template #extra>
        <a-button type="primary" @click="$router.push('/home')">
          {{ $t('common.back_home') }}
        </a-button>
      </template>
    </a-result>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f5f5;
}
</style>