import axios from 'axios'
import type { AxiosRequestConfig } from 'axios'
import { message } from 'ant-design-vue'
import { getToken, removeToken, shouldRefreshToken, isTokenExpired } from '@/utils/auth'

// 扩展AxiosRequestConfig类型以包含自定义属性
declare module 'axios' {
  interface AxiosRequestConfig {
    _isTokenRefresh?: boolean;
    skipGlobalErrorHandling?: boolean;
  }
}

// Create axios instance
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? 'https://nexauraseo.com' : 'http://127.0.0.1:5000'),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 存储等待令牌刷新的请求
let refreshSubscribers: Array<(token: string) => void> = []

// 添加订阅者到队列
const subscribeTokenRefresh = (cb: (token: string) => void) => {
  refreshSubscribers.push(cb)
}

// 执行队列中的订阅者
const onTokenRefreshed = (token: string) => {
  refreshSubscribers.forEach(cb => cb(token))
  refreshSubscribers = []
}



// Request interceptor
http.interceptors.request.use(
  (config: any) => {
    // 如果请求是刷新令牌，并且已经设置了Authorization头，则不修改
    if (config.url?.includes('/auth/refresh-token') && config.headers.Authorization) {
      return config
    }
    
    // Add Authorization header if token exists
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error: any) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
http.interceptors.response.use(
  (response: any) => {
    return response
  },
  async (error: any) => {
    console.error('Response error:', error.config?.url, {
      status: error.response?.status,
      statusText: error.response?.statusText,
      message: error.message,
      data: error.response?.data
    })
    
    const originalRequest = error.config as any & { _retry?: boolean }
    
    // 如果是刷新令牌请求本身失败，直接登出
    if (error.response?.status === 401 && originalRequest.url?.includes('/auth/refresh-token')) {
      const userStore = await import('@/stores/modules/user').then(m => m.useUserStore())
      await userStore.logout()
      
      // 重定向到登录页面
      const router = await import('@/router').then(m => m.default)
      router.push('/login')
      
      return Promise.reject(error)
    }
    
    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const token = getToken()
      if (token && (isTokenExpired(token) || shouldRefreshToken(token))) {
        try {
          // 使用令牌刷新服务
          const { tokenRefreshService } = await import('@/services/tokenRefresh')
          
          // 如果已经在刷新中，等待完成
          if (tokenRefreshService.isCurrentlyRefreshing()) {
          return new Promise(resolve => {
            subscribeTokenRefresh(token => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              resolve(http(originalRequest))
            })
          })
        }
        
          // 执行令牌刷新
          const newToken = await tokenRefreshService.refreshToken()
          
          if (newToken) {
            originalRequest.headers.Authorization = `Bearer ${newToken}`
            
            // 通知所有等待的请求
            onTokenRefreshed(newToken)
            
            return http(originalRequest)
          } else {
            throw new Error('Token refresh returned null')
          }
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError)
          
          // Token refresh failed, logout user
          const userStore = await import('@/stores/modules/user').then(m => m.useUserStore())
          await userStore.logout()
          
          // Redirect to login page
          const router = await import('@/router').then(m => m.default)
          router.push('/login')
        }
      } else {
        // No token or token shouldn't be refreshed, logout
        const userStore = await import('@/stores/modules/user').then(m => m.useUserStore())
        await userStore.logout()
        
        // Redirect to login page
        const router = await import('@/router').then(m => m.default)
        router.push('/login')
      }
      
      return Promise.reject(error)
    }
    
    // Check if global error handling should be skipped
    if (originalRequest.skipGlobalErrorHandling) {
      return Promise.reject(error)
    }
    
    // Handle different error status codes
    const status = error.response?.status
    const errorMessage = error.response?.data?.message || error.message
    
    switch (status) {
      case 400:
        message.error(`Bad Request: ${errorMessage}`)
        break
      case 401:
        message.error('Authentication failed. Please login again.')
        break
      case 403:
        message.error('Access denied. You do not have permission.')
        break
      case 404:
        message.error('Resource not found.')
        break
      case 422:
        // Validation errors - don't show global message, let components handle
        break
      case 429:
        message.error('Too many requests. Please try again later.')
        break
      case 500:
        message.error('Internal server error. Please try again later.')
        break
      case 502:
        message.error('Service unavailable. Please try again later.')
        break
      case 503:
        message.error('Service temporarily unavailable.')
        break
      default:
        if (status && status >= 500) {
          message.error('Server error. Please try again later.')
        } else if (status && status >= 400) {
          message.error(`Error: ${errorMessage}`)
        } else {
          console.error('Network error details:', error)
          console.error('Error config:', error.config)
          console.error('Error request:', error.request)
          message.error('Network error. Please check your connection.')
        }
    }
    
    return Promise.reject(error)
  }
)

// Helper functions for common HTTP methods
export const httpHelpers = {
  get: <T = any>(url: string, config?: any): Promise<any> => {
    return http.get<T>(url, config)
  },
  
  post: <T = any>(url: string, data?: any, config?: any): Promise<any> => {
    return http.post<T>(url, data, config)
  },
  
  put: <T = any>(url: string, data?: any, config?: any): Promise<any> => {
    return http.put<T>(url, data, config)
  },
  
  patch: <T = any>(url: string, data?: any, config?: any): Promise<any> => {
    return http.patch<T>(url, data, config)
  },
  
  delete: <T = any>(url: string, config?: any): Promise<any> => {
    return http.delete<T>(url, config)
  }
}

export { http }
export default http