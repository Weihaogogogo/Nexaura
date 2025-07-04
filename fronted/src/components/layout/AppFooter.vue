<template>
  <div class="app-footer">
    <!-- Gradient Background -->
    <div class="footer-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>
    
    <div class="footer-content">
      <div class="footer-brand">
        <div class="brand-logo">
          <div class="logo-icon">✨</div>
          <span class="brand-name">AI Article Pro</span>
        </div>
        <p class="brand-tagline">
          用AI重新定义内容创作 • 让每个想法都闪闪发光
        </p>
        <div class="social-links">
          <a href="#" class="social-link twitter">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"/>
            </svg>
          </a>
          <a href="#" class="social-link linkedin">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/>
              <circle cx="4" cy="4" r="2"/>
            </svg>
          </a>
          <a href="#" class="social-link github">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
        </div>
      </div>
      
      <div class="footer-links">
        <div class="link-group">
          <h4 class="group-title">🚀 产品功能</h4>
          <a @click="handleAIWriterClick" class="nav-link cursor-pointer">
            <span class="link-icon">⚡</span>
            极速创作
          </a>
          <router-link to="/app/articles" class="nav-link">
            <span class="link-icon">📝</span>
            内容管理
          </router-link>
          <router-link to="/app/dashboard" class="nav-link">
            <span class="link-icon">📊</span>
            数据洞察
          </router-link>
        </div>
        
        <div class="link-group">
          <h4 class="group-title">💡 帮助支持</h4>
          <router-link to="/help" class="nav-link">
            <span class="link-icon">💬</span>
            使用教程
          </router-link>
          <router-link to="/help/faq" class="nav-link">
            <span class="link-icon">❓</span>
            常见问题
          </router-link>
          <router-link to="/blog" class="nav-link">
            <span class="link-icon">📝</span>
            博客
          </router-link>
          <a href="mailto:support@seogenerator.com" class="nav-link">
            <span class="link-icon">📧</span>
            联系我们
          </a>
        </div>
        
        <div class="link-group">
          <h4 class="group-title">🛡️ 法律条款</h4>
          <router-link to="/privacy" class="nav-link">
            <span class="link-icon">🔒</span>
            隐私政策
          </router-link>
          <router-link to="/terms" class="nav-link">
            <span class="link-icon">📋</span>
            服务条款
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <div class="copyright">
        <span class="made-with">Made with ❤️ by AI Article Pro Team</span>
        <span class="year">© {{ new Date().getFullYear() }} 版权所有</span>
      </div>
      <div class="tech-badge">
        <span class="badge">⚡ Powered by AI</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

// 处理AI Writer点击事件
const handleAIWriterClick = () => {
  // 检查登录状态
  if (userStore.isAuthenticated) {
    // 如果已登录，跳转到创建工作流页面
    router.push('/app/workflow/new')
  } else {
    // 如果未登录，跳转到登录页面
    router.push('/login')
  }
}
</script>

<style scoped>
.app-footer {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow: hidden;
  padding: 60px 0 20px;
  margin-top: auto;
}

/* 动态背景装饰 */
.footer-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #ff6b6b, #4ecdc4);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, #a8edea, #fed6e3);
  top: 20%;
  right: -75px;
  animation-delay: 2s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #d299c2, #fef9d7);
  bottom: -150px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.footer-content {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 60px;
  z-index: 1;
}

/* 品牌区域 */
.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.logo-icon {
  font-size: 32px;
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.1) rotate(180deg); }
}

.brand-name {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(45deg, #fff, #f0f8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
}

.brand-tagline {
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 300;
}

/* 社交链接 */
.social-links {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.social-link {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  color: white;
}

.social-link svg {
  width: 20px;
  height: 20px;
}

.social-link:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.social-link.twitter:hover { background: rgba(29, 161, 242, 0.8); }
.social-link.linkedin:hover { background: rgba(40, 103, 178, 0.8); }
.social-link.github:hover { background: rgba(51, 51, 51, 0.8); }

/* 链接组 */
.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.group-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.link-icon {
  font-size: 16px;
  opacity: 0.9;
}

/* 底部区域 */
.footer-bottom {
  position: relative;
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 32px;
  padding-right: 32px;
  z-index: 1;
}

.copyright {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.made-with {
  font-weight: 500;
}

.year {
  font-size: 12px;
  opacity: 0.8;
}

.tech-badge .badge {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
  50% { box-shadow: 0 4px 25px rgba(255, 107, 107, 0.3); }
  100% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-footer {
    padding: 40px 0 20px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
    padding: 0 20px;
    text-align: center;
  }
  
  .footer-links {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 16px;
    text-align: center;
    padding: 24px 20px 0;
  }
  
  .brand-name {
    font-size: 24px;
  }
  
  .social-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .footer-links {
    gap: 24px;
  }
  
  .group-title {
    font-size: 16px;
  }
  
  .nav-link {
    padding: 6px 8px;
    font-size: 14px;
  }
}
</style>