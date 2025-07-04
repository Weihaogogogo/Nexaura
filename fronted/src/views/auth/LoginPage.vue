<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Background Elements -->
      <div class="bg-gradient"></div>
      <div class="bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
      
      <div class="login-form-wrapper">
        <!-- Header -->
        <div class="login-header">
          <div class="logo-section">
            <div class="logo-icon">
              <img src="/logo.ico" alt="Logo" class="logo-image" />
            </div>
            <h1 class="logo-text">Nexaura</h1>
          </div>
          <div class="welcome-section">
            <h2 class="welcome-title">Welcome back</h2>
            <p class="welcome-subtitle">Sign in to your account to continue</p>
          </div>
        </div>


        
        <!-- Login Form -->
        <a-form
          :model="form"
          :rules="rules"
          @finish="handleLogin"
          layout="vertical"
          class="login-form"
        >
          <a-form-item name="email" class="form-item">
            <label class="field-label">Email address</label>
            <a-input
              v-model:value="form.email"
              placeholder="Enter your email"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <MailOutlined class="input-icon" />
              </template>
            </a-input>
          </a-form-item>
          
          <a-form-item name="password" class="form-item">
            <label class="field-label">Password</label>
            <a-input-password
              v-model:value="form.password"
              placeholder="Enter your password"
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <LockOutlined class="input-icon" />
              </template>
            </a-input-password>
          </a-form-item>
          
          <div class="form-options">
            <a-checkbox 
              v-model:checked="form.remember"
              class="remember-checkbox"
            >
              Remember me
            </a-checkbox>
            <router-link to="/forgot-password" class="forgot-link">
              Forgot password?
            </router-link>
          </div>
          
          <a-form-item class="submit-section">
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              :loading="loading"
              block
              class="login-btn"
            >
              Sign In
              <ArrowRightOutlined class="btn-icon" />
            </a-button>
          </a-form-item>
        </a-form>
        
        <!-- Footer -->
        <div class="login-footer">
          <p class="footer-text">
            Don't have an account?
            <router-link to="/register" class="register-link">
              Create account
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { message } from 'ant-design-vue'
import { 
  MailOutlined, 
  LockOutlined, 
  ArrowRightOutlined,
  ThunderboltOutlined 
} from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/modules/user'
import type { LoginForm } from '@/types/auth'

const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()

const loading = ref(false)
const devLoginLoading = ref(false)

const form = reactive<LoginForm>({
  email: '',
  password: '',
  remember: false
})

const rules = {
  email: [
    { required: true, message: 'Please enter your email address' },
    { type: 'email', message: 'Please enter a valid email address' }
  ],
  password: [
    { required: true, message: 'Please enter your password' },
    { min: 6, message: 'Password must be at least 6 characters' }
  ]
}

const handleLogin = async (values: LoginForm) => {
  loading.value = true
  try {
    await userStore.login(values)
    message.success('Welcome back!')
    
    // Redirect to intended page or dashboard
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/app/dashboard')
  } catch (error: any) {
    message.error(error.message || 'Login failed. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleDevLogin = async () => {
  devLoginLoading.value = true
  try {
    // Use developer account credentials
    const devCredentials: LoginForm = {
      email: 'dev@test.com',
      password: 'dev123456',
      remember: false
    }
    
    await userStore.login(devCredentials)
    message.success('Developer login successful!')
    
    // Redirect to dashboard
    router.push('/app/dashboard')
  } catch (error: any) {
    message.error('Developer login failed. Account may not exist yet.')
  } finally {
    devLoginLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
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
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
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

.login-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 10;
}

.login-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 48px;
  border-radius: 24px;
  box-shadow: 
    0 32px 64px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.login-header {
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
}

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

.dev-login-section {
  margin-bottom: 24px;
}

.dev-login-btn {
  height: 56px;
  border: 2px dashed #d1d5db;
  background: rgba(239, 246, 255, 0.5);
  color: #4f46e5;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.dev-login-btn:hover {
  border-color: #4f46e5;
  background: rgba(239, 246, 255, 0.8);
  transform: translateY(-1px);
}

.dev-login-note {
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
  margin: 8px 0 0 0;
}

.login-divider {
  margin: 32px 0;
  border-color: #e5e7eb;
}

.divider-text {
  color: #9ca3af;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.95);
  padding: 0 16px;
}

.login-form {
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.remember-checkbox {
  color: #6b7280;
  font-size: 14px;
}

.forgot-link {
  color: #4f46e5;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #3730a3;
  text-decoration: underline;
}

.submit-section {
  margin-bottom: 0;
}

.login-btn {
  height: 56px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4);
}

.login-btn:active {
  transform: translateY(0);
}

.btn-icon {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.login-btn:hover .btn-icon {
  transform: translateX(4px);
}

.login-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.footer-text {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.register-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
  margin-left: 8px;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: #3730a3;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-form-wrapper {
    padding: 32px 24px;
    border-radius: 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .custom-input,
  .login-btn,
  .dev-login-btn {
    height: 52px;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 16px;
  }
  
  .login-form-wrapper {
    padding: 24px 20px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .form-options {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>