<template>
  <div class="register-page">
    <div class="register-container">
      <!-- Background Elements -->
      <div class="bg-gradient"></div>
      <div class="bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      
      <div class="register-form-wrapper">
        <!-- Header -->
        <div class="register-header">
          <div class="logo-section">
            <div class="logo-icon">
              <img src="/logo.ico" alt="Logo" class="logo-image" />
            </div>
            <h1 class="logo-text">Nexaura</h1>
          </div>
          <div class="welcome-section">
            <h2 class="welcome-title">Create your account</h2>
            <p class="welcome-subtitle">Start generating SEO content with AI</p>
          </div>
        </div>
        
        <!-- Register Form -->
        <a-form
          :model="form"
          :rules="rules"
          @finish="handleRegister"
          layout="vertical"
          class="register-form"
        >
          <a-form-item name="email" class="form-item">
            <label class="field-label">Email address</label>
            <a-input
              v-model:value="form.email"
              placeholder="Enter your email"
              size="large"
              type="email"
              class="custom-input"
            >
              <template #prefix>
                <MailOutlined class="input-icon" />
              </template>
            </a-input>
          </a-form-item>
          
          <a-form-item name="code" class="form-item">
            <label class="field-label">Verification Code</label>
            <a-input-group compact class="code-input-group">
              <a-input
                v-model:value="form.code"
                placeholder="Enter 6-digit code"
                size="large"
                class="custom-input code-input"
              >
                <template #prefix>
                  <SafetyCertificateOutlined class="input-icon" />
                </template>
              </a-input>
              <a-button
                size="large"
                :loading="sendingCode"
                :disabled="!isValidEmail || countdown > 0"
                @click="handleSendCode"
                class="code-button"
              >
                <span v-if="countdown > 0">{{ countdown }}s</span>
                <span v-else>Send Code</span>
              </a-button>
            </a-input-group>
          </a-form-item>
          
          <a-form-item name="password" class="form-item">
            <label class="field-label">Password</label>
            <a-input-password
              v-model:value="form.password"
              placeholder="Create a password"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <LockOutlined class="input-icon" />
              </template>
            </a-input-password>
          </a-form-item>
          
          <a-form-item name="confirmPassword" class="form-item">
            <label class="field-label">Confirm Password</label>
            <a-input-password
              v-model:value="form.confirmPassword"
              placeholder="Confirm your password"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <LockOutlined class="input-icon" />
              </template>
            </a-input-password>
          </a-form-item>
          
          <a-form-item name="terms" class="form-item terms-item">
            <a-checkbox 
              v-model:checked="form.terms"
              class="terms-checkbox"
            >
              I agree to the 
              <a href="/terms" target="_blank" class="terms-link">Terms of Service</a>
              and 
              <a href="/privacy" target="_blank" class="terms-link">Privacy Policy</a>
            </a-checkbox>
          </a-form-item>
          
          <a-form-item class="submit-section">
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              :loading="loading"
              block
              class="register-btn"
            >
              Create Account
              <ArrowRightOutlined class="btn-icon" />
            </a-button>
          </a-form-item>
        </a-form>
        
        <!-- Footer -->
        <div class="register-footer">
          <p class="footer-text">
            Already have an account?
            <router-link to="/login" class="login-link">
              Sign in
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { 
  MailOutlined, 
  LockOutlined, 
  SafetyCertificateOutlined,
  ArrowRightOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/modules/user'
import type { RegisterForm } from '@/types/auth'

const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()

const loading = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)
let countdownTimer: any = null

const form = reactive<RegisterForm & { code: string }>({
  email: '',
  password: '',
  confirmPassword: '',
  code: '',
  terms: false
})

// Email validation
const isValidEmail = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(form.email)
})

const validateConfirmPassword = (_rule: any, value: string) => {
  if (value && value !== form.password) {
    return Promise.reject('The two passwords do not match')
  }
  return Promise.resolve()
}

const rules = {
  email: [
    { required: true, message: 'Please enter your email address' },
    { type: 'email', message: 'Please enter a valid email address' }
  ],
  code: [
    { required: true, message: 'Please enter the verification code' },
    { pattern: /^\d{6}$/, message: 'Verification code must be 6 digits' }
  ],
  password: [
    { required: true, message: 'Please enter your password' },
    { min: 6, message: 'Password must be at least 6 characters' }
  ],
  confirmPassword: [
    { required: true, message: 'Please confirm your password' },
    { validator: validateConfirmPassword }
  ],
  terms: [
    { required: true, message: 'Please accept the terms and conditions', type: 'boolean' }
  ]
}

const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer!)
      countdownTimer = null
    }
  }, 1000)
}

const handleSendCode = async () => {
  if (!isValidEmail.value) {
    message.error('Please enter a valid email address')
    return
  }
  
  sendingCode.value = true
  try {
    await userStore.getVerificationCode(form.email)
    message.success('Verification code sent to your email')
    startCountdown()
  } catch (error: any) {
    message.error(error.message || 'Failed to send verification code')
  } finally {
    sendingCode.value = false
  }
}

const handleRegister = async (values: typeof form) => {
  loading.value = true
  try {
    await userStore.register(values)
    message.success('Account created successfully!')
    router.push('/login')
  } catch (error: any) {
    console.log('Registration error:', error)
    
    // 处理特定的账号已存在错误
    const errorMsg = error.message || ''
    
    if (errorMsg.includes('该帐号已存在') || errorMsg.includes('重复注册')) {
      message.error('该邮箱已被注册，请使用其他邮箱或前往登录页面')
    } else if (errorMsg.includes('验证码') || errorMsg.includes('captcha')) {
      message.error('验证码错误或已过期，请重新获取')
    } else if (errorMsg.includes('密码') || errorMsg.includes('password')) {
      message.error('密码格式不正确，请检查后重试')
    } else if (errorMsg.includes('邮箱') || errorMsg.includes('email')) {
      message.error('邮箱格式不正确，请检查后重试')
    } else {
      // 对于其他错误，显示具体的错误消息或通用消息
      message.error(errorMsg || '注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  opacity: 0.9;
  border-radius: 24px;
}

.bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  border-radius: 24px;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  animation: float 8s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  right: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  bottom: 60%;
  left: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  top: 20%;
  right: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.register-container {
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 10;
}

.register-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 48px;
  border-radius: 24px;
  box-shadow: 
    0 32px 64px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);

.logo-image {
  width: 48px;
  height: 48px;
  object-fit: contain;
}}

.logo-image {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-section {
  margin-bottom: 8px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.register-form {
  margin-bottom: 24px;
}

.form-item {
  margin-bottom: 24px;
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.custom-input {
  height: 56px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.custom-input:hover {
  border-color: #d1d5db;
}

.custom-input:focus,
.custom-input.ant-input-focused {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-icon {
  color: #9ca3af;
  font-size: 16px;
}

.code-input-group {
  display: flex;
  gap: 12px;
}

.code-input {
  flex: 1;
}

.code-button {
  width: 120px;
  height: 56px;
  border-radius: 12px;
  border: 2px solid #4f46e5;
  background: #4f46e5;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.code-button:hover:not(:disabled) {
  background: #3730a3;
  border-color: #3730a3;
  transform: translateY(-1px);
}

.code-button:disabled {
  background: #e5e7eb;
  border-color: #e5e7eb;
  color: #9ca3af;
}

.terms-item {
  margin-bottom: 32px;
}

.terms-checkbox {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.terms-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.terms-link:hover {
  color: #3730a3;
  text-decoration: underline;
}

.submit-section {
  margin-bottom: 0;
}

.register-btn {
  height: 56px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  transition: all 0.3s ease;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4);
}

.register-btn:active {
  transform: translateY(0);
}

.btn-icon {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.register-btn:hover .btn-icon {
  transform: translateX(4px);
}

.register-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.footer-text {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.login-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
  margin-left: 8px;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #3730a3;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .register-form-wrapper {
    padding: 32px 24px;
    border-radius: 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .custom-input,
  .register-btn,
  .code-button {
    height: 52px;
  }
  
  .code-input-group {
    flex-direction: column;
    gap: 12px;
  }
  
  .code-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .register-page {
    padding: 16px;
  }
  
  .register-form-wrapper {
    padding: 24px 20px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
}
</style>