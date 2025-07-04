import { 
  getToken, 
  getRefreshToken, 
  setToken, 
  removeToken, 
  shouldRefreshToken, 
  isTokenExpired,
  getTimeUntilExpiry 
} from '@/utils/auth'
import { authApi } from '@/services/api/auth'

class TokenRefreshService {
  private refreshPromise: Promise<string> | null = null
  private refreshTimer: number | null = null
  private isRefreshing = false

  constructor() {
    this.startAutoRefresh()
  }

  /**
   * 开始自动刷新机制
   */
  startAutoRefresh() {
    // 立即检查一次
    this.scheduleNextRefresh()
    
    // 监听页面可见性变化，当用户回到页面时检查令牌
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        this.checkAndRefreshToken()
      }
    })

    // 监听焦点事件，当用户切回窗口时检查令牌
    window.addEventListener('focus', () => {
      this.checkAndRefreshToken()
    })
  }

  /**
   * 停止自动刷新
   */
  stopAutoRefresh() {
    if (this.refreshTimer) {
      window.clearTimeout(this.refreshTimer)
      this.refreshTimer = null
    }
  }

  /**
   * 检查并刷新令牌
   */
  async checkAndRefreshToken(): Promise<string | null> {
    const token = getToken()

    if (!token) {
      return null
    }

    // 如果令牌已过期，立即刷新
    if (isTokenExpired(token)) {
      return await this.refreshToken()
    }

    // 如果令牌即将过期，刷新
    if (shouldRefreshToken(token)) {
      return await this.refreshToken()
    }

    // 令牌还有效，安排下次检查
    this.scheduleNextRefresh()
    return token
  }

  /**
   * 刷新令牌
   */
  async refreshToken(): Promise<string | null> {
    // 如果已经在刷新中，返回现有的Promise
    if (this.refreshPromise) {
      try {
        return await this.refreshPromise
      } catch (error) {
        this.refreshPromise = null
        throw error
      }
    }

    // 检查是否有token
    const currentToken = getToken()
    if (!currentToken) {
      this.handleRefreshFailure()
      return null
    }

    this.isRefreshing = true
    this.refreshPromise = this.performRefresh()

    try {
      const newToken = await this.refreshPromise
      this.scheduleNextRefresh()
      return newToken
    } catch (error) {
      console.error('Token refresh failed:', error)
      this.handleRefreshFailure()
      throw error
    } finally {
      this.isRefreshing = false
      this.refreshPromise = null
    }
  }

  /**
   * 执行实际的刷新操作
   */
  private async performRefresh(): Promise<string> {
    try {
      const result = await authApi.refreshToken()
      return result.token
    } catch (error) {
      console.error('❌ Token refresh failed:', error)
      throw error
    }
  }

  /**
   * 处理刷新失败
   */
  private handleRefreshFailure() {
    removeToken()
    
    // 如果当前在应用页面，重定向到登录页
    if (window.location.pathname.startsWith('/app')) {
      window.location.href = '/login'
    }
  }

  /**
   * 安排下次刷新检查
   */
  private scheduleNextRefresh() {
    if (this.refreshTimer) {
      window.clearTimeout(this.refreshTimer)
    }

    const token = getToken()
    if (!token) {
      return
    }

    try {
      const timeUntilExpiry = getTimeUntilExpiry(token)
      
      if (timeUntilExpiry <= 0) {
        // 令牌已过期，立即刷新
        this.refreshToken()
        return
      }

      // 在令牌过期前10分钟进行刷新，但至少1分钟后检查
      const refreshIn = Math.max(60000, (timeUntilExpiry - 600) * 1000)
      
      this.refreshTimer = window.setTimeout(() => {
        this.checkAndRefreshToken()
      }, refreshIn)
      
    } catch (error) {
      console.error('Error scheduling next refresh:', error)
      // 如果解析失败，1分钟后重试
      this.refreshTimer = window.setTimeout(() => {
        this.checkAndRefreshToken()
      }, 60000)
    }
  }

  /**
   * 获取当前刷新状态
   */
  isCurrentlyRefreshing(): boolean {
    return this.isRefreshing
  }

  /**
   * 等待当前刷新完成
   */
  async waitForRefresh(): Promise<string | null> {
    if (this.refreshPromise) {
      try {
        return await this.refreshPromise
      } catch (error) {
        return null
      }
    }
    return getToken()
  }
}

// 创建单例实例
export const tokenRefreshService = new TokenRefreshService()

// 导出类型用于测试
export type { TokenRefreshService } 