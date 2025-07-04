<template>
  <footer class="footer-container relative z-30 w-full">
    <div class="footer-content max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <!-- Main Footer Content -->
      <div class="footer-grid grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
        <!-- Brand Section -->
        <div class="brand-section">
          <div class="flex items-center gap-3 mb-6">
            <img src="/logo.ico" alt="Nexaura" class="w-8 h-8" />
            <span class="brand-name text-xl font-bold text-white">Nexaura</span>
          </div>
          <p class="brand-description text-gray-400 text-sm leading-relaxed">
            {{ t('home.footer.brand.description') }}
          </p>
          <!-- Social Icons -->
          <div class="social-icons flex gap-3 mt-6">
            <a href="#" class="social-icon">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
            <a href="#" class="social-icon">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
              </svg>
            </a>
            <a href="#" class="social-icon">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
            <a href="#" class="social-icon">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a href="#" class="social-icon">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 2.567-1.645 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Product Column -->
        <div class="footer-column">
          <h3 class="footer-heading text-white font-semibold mb-4">{{ t('home.footer.products.title') }}</h3>
          <ul class="footer-links space-y-3">
            <li><a href="#" class="footer-link">{{ t('home.footer.products.ai_writer') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.products.seo_tools') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.products.content_planner') }}</a></li>
          </ul>
        </div>

        <!-- Tools Column -->
        <div class="footer-column">
          <h3 class="footer-heading text-white font-semibold mb-4">{{ t('home.footer.tools.title') }}</h3>
          <ul class="footer-links space-y-3">
            <li><a href="#" class="footer-link">{{ t('home.footer.tools.keyword_research') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.tools.topic_generator') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.tools.outline_builder') }}</a></li>
          </ul>
        </div>

        <!-- Resources & Support Column -->
        <div class="footer-column">
          <h3 class="footer-heading text-white font-semibold mb-4">{{ t('home.footer.support.title') }}</h3>
          <ul class="footer-links space-y-3">
            <li><a href="#" class="footer-link">{{ t('home.footer.support.help_center') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.support.documentation') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.support.community') }}</a></li>
            <li><a href="#" class="footer-link">{{ t('home.footer.support.contact') }}</a></li>
          </ul>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom pt-8 border-t border-gray-800">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="footer-copyright text-gray-400 text-sm">
            {{ t('home.footer.copyright') }}
          </div>
          <div class="footer-legal flex gap-6">
            <a href="#" class="footer-link text-sm">{{ t('nav.privacy') }}</a>
            <a href="#" class="footer-link text-sm">{{ t('nav.terms') }}</a>
          </div>
          <div class="back-to-top">
            <button class="back-to-top-btn" @click="scrollToTop">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
              </svg>
              {{ t('home.footer.back_to_top') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
/* Footer Styles */
.footer-container {
  margin-top: 50px;
  background: rgb(19, 10, 46);
  border-top: 1px solid rgba(147, 51, 234, 0.2);
  backdrop-filter: blur(10px);
}

.footer-content {
  font-family: 'Poppins', sans-serif;
}

.brand-name {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

.brand-description {
  max-width: 300px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.social-icon:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}

.footer-heading {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.1rem;
  color: #fff;
}

.footer-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.9rem;
}

.footer-link:hover {
  color: #fff;
}

.footer-copyright {
  font-family: 'Poppins', sans-serif;
  color: rgba(255, 255, 255, 0.7);
}

.footer-bottom {
  border-color: rgba(255, 255, 255, 0.2);
}

.back-to-top-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
  backdrop-filter: blur(10px);
}

.back-to-top-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}

/* Responsive Footer */
@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-bottom {
    text-align: center;
  }
  
  .footer-bottom > div {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>