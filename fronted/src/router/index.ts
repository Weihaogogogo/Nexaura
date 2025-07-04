import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'HomeRoot',
    component: () => import('@/views/home/HomePage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/home/HomePage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/home/AboutPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('@/views/home/PricingPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/home/ContactPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterPage.vue'),
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/auth/ForgotPasswordPage.vue'),
    meta: { requiresAuth: false, hideForAuth: true }
  },
  {
    path: '/app',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: false },
    children: [
      {
        path: '',
        redirect: '/app/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/app/DashboardPage.vue')
      },
      {
        path: 'workflow/records',
        name: 'WorkflowRecords',
        component: () => import('@/views/app/workflow/WorkflowRecordsPage.vue')
      },
      {
        path: 'workflow/:sessionId',
        name: 'Workflow',
        component: () => import('@/views/app/workflow/WorkflowPage.vue')
      },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('@/views/app/articles/ArticleListPage.vue')
      },
      {
        path: 'articles/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/app/articles/ArticleDetailPage.vue')
      },
      {
        path: 'articles/:id/edit',
        name: 'ArticleEdit',
        component: () => import('@/views/app/articles/ArticleEditPage.vue')
      }
    ]
  },
  {
    path: '/help',
    name: 'Help',
    component: () => import('@/views/help/HelpPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: () => import('@/views/help/FAQPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('@/views/help/PrivacyPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/terms',
    name: 'Terms',
    component: () => import('@/views/help/TermsPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('@/views/TestPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/test-loading',
    name: 'TestLoading',
    component: () => import('@/views/TestLoadingPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/element-plus-demo',
    name: 'ElementPlusDemo',
    component: () => import('@/components/ElementPlusDemo.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {

  
  const userStore = useUserStore()
  
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  const hideForAuth = to.matched.some(record => record.meta.hideForAuth)
  
  // 如果用户已认证
  if (userStore.isAuthenticated) {
    // 如果页面对已认证用户隐藏(如登录页)，重定向到首页
    if (hideForAuth) {
      next('/app/dashboard')
      return
    }
    next()
    return
  }
  
  // 用户未认证，但尝试访问需要认证的页面
  if (requiresAuth) {
    try {
      // 尝试验证会话
      const isSessionValid = await userStore.validateSession()
      if (isSessionValid) {
        next() // 会话有效，允许访问
        return
      }
      
      // 会话无效，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } catch (error) {
      console.error('Authentication error:', error)
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    // 不需要认证的页面，直接访问
    next()
  }
})

export default router