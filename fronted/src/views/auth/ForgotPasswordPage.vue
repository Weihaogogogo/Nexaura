<template>
  <div class="forgot-password-page">
    <div class="forgot-container">
      <div class="forgot-form-wrapper">
        <div class="forgot-header">
          <div class="logo">
            <img src="/logo.ico" alt="Nexaura" class="logo-img" />
            <h1 class="logo-text">Nexaura</h1>
          </div>
          <h2 class="forgot-title">{{ $t('auth.forgot.title') }}</h2>
          <p class="forgot-subtitle">{{ $t('auth.forgot.subtitle') }}</p>
        </div>
        
        <a-form
          :model="form"
          :rules="rules"
          @finish="handleSubmit"
          layout="vertical"
          class="forgot-form"
        >
          <a-form-item name="email" :label="$t('auth.forgot.email')">
            <a-input
              v-model:value="form.email"
              :placeholder="$t('auth.forgot.email_placeholder')"
              size="large"
              type="email"
            >
              <template #prefix>
                <UserOutlined />
              </template>
            </a-input>
          </a-form-item>
          
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              :loading="loading"
              block
            >
              {{ $t('auth.forgot.submit') }}
            </a-button>
          </a-form-item>
        </a-form>
        
        <div class="forgot-footer">
          <router-link to="/login" class="back-link">
            {{ $t('auth.forgot.back') }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { UserOutlined } from '@ant-design/icons-vue'

const { t } = useI18n()
const loading = ref(false)

const form = reactive({
  email: ''
})

const rules = {
  email: [
    { required: true, message: t('auth.validation.email_required') },
    { type: 'email', message: t('auth.validation.email_invalid') }
  ]
}

const handleSubmit = async (values: typeof form) => {
  loading.value = true
  try {
    // TODO: Implement forgot password API call
    message.success(t('auth.forgot.success'))
  } catch (error) {
    message.error(t('auth.forgot.error'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.forgot-container {
  width: 100%;
  max-width: 400px;
}

.forgot-form-wrapper {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.forgot-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.logo-img {
  height: 40px;
  width: 40px;
  object-fit: contain;
}

.logo-text {
  font-size: 24px;
  font-weight: 600;
  color: #1890ff;
  margin: 0;
}

.forgot-title {
  font-size: 28px;
  font-weight: 600;
  color: #262626;
  margin: 0 0 8px 0;
}

.forgot-subtitle {
  color: #8c8c8c;
  font-size: 14px;
  margin: 0;
}

.forgot-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.back-link {
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}
</style>