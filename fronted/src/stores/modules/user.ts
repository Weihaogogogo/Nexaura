import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginForm, RegisterForm, AuthResponse, AuthState } from '@/types/auth'
import { authApi } from '@/services/api/auth'
import { removeToken, setToken, getToken, hasToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(getToken())
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)

  // Getters
  const isAuthenticated = computed(() => {
    // Check if we have a token and user data
    const hasValidToken = hasToken()
    const hasUserData = !!user.value
    
    // If we have a token but no user data, try to restore from localStorage
    if (hasValidToken && !hasUserData) {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
          return true
        } catch (error) {
          console.error('Failed to restore user from localStorage:', error)
          return false
        }
      }
    }
    
    return hasValidToken && hasUserData
  })
  const userRole = computed(() => user.value?.role || 'user')
  const quotaPercentage = computed(() => {
    if (!user.value) return 0
    return Math.round((user.value.used_quota / user.value.total_quota) * 100)
  })

  // Actions
  const login = async (loginForm: LoginForm): Promise<void> => {
    try {
      isLoading.value = true
      
      // Check for developer account quick login
      if (loginForm.email === 'dev@test.com' && loginForm.password === 'dev123456') {
        // Mock developer user
        const devUser: User = {
          id: 'dev-001',
          email: 'dev@test.com',
          name: 'Developer',
          role: 'user' as const,
          status: 'active' as const,
          total_quota: 999,
          used_quota: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        
        user.value = devUser
        // Create a mock JWT token for dev
        const mockToken = btoa(JSON.stringify({
          sub: 'dev@test.com',
          name: 'Developer',
          exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
        }))
        token.value = mockToken
        setToken(mockToken)
        
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(devUser))
        return
      }
      
      // Normal login flow using JWT
      const response = await authApi.login(loginForm)
      
      user.value = response.user
      token.value = getToken() // Token is set by authApi.login()
      
      // Store user data in localStorage
      localStorage.setItem('user', JSON.stringify(response.user))
      
      // 启动令牌刷新服务
      try {
        const { tokenRefreshService } = await import('@/services/tokenRefresh')
      } catch (error) {
        console.error('Failed to start token refresh service:', error)
      }
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (registerForm: RegisterForm & { code: string }): Promise<void> => {
    try {
      isLoading.value = true
      await authApi.register(registerForm)
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const getVerificationCode = async (email: string): Promise<void> => {
    try {
      isLoading.value = true
      await authApi.getVerificationCode(email)
    } catch (error) {
      console.error('Get verification code failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      if (hasToken()) {
        await authApi.logout()
      }
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      // Clear state regardless of API call success
      user.value = null
      token.value = null
      refreshToken.value = null
      
      removeToken()
      localStorage.removeItem('user')
      localStorage.removeItem('refresh_token')
      
      // 停止令牌刷新服务
      try {
        const { tokenRefreshService } = await import('@/services/tokenRefresh')
        tokenRefreshService.stopAutoRefresh()
      } catch (error) {
        console.error('Failed to stop token refresh service:', error)
      }
    }
  }

  const fetchUser = async (): Promise<void> => {
    try {
      if (!hasToken()) return
      
      isLoading.value = true
      const userData = await authApi.getProfile()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (error) {
      console.error('Fetch user failed:', error)
      // If token is invalid, logout
      await logout()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 验证当前JWT token状态
  const validateSession = async (): Promise<boolean> => {
    try {
      if (!hasToken()) {
        return false
      }
      
      isLoading.value = true
      const userData = await authApi.validateSession()
      user.value = userData
      token.value = getToken()
      localStorage.setItem('user', JSON.stringify(userData))
      return true
    } catch (error) {
      console.error('JWT token validation failed:', error)
      // 如果token无效，清除本地状态
      user.value = null
      token.value = null
      removeToken()
      localStorage.removeItem('user')
      return false
    } finally {
      isLoading.value = false
    }
  }

  const updateProfile = async (profileData: Partial<User>): Promise<void> => {
    try {
      isLoading.value = true
      const updatedUser = await authApi.updateProfile(profileData)
      user.value = updatedUser
      localStorage.setItem('user', JSON.stringify(updatedUser))
    } catch (error) {
      console.error('Update profile failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const refreshUserToken = async (): Promise<void> => {
    try {
      const response = await authApi.refreshToken()
      token.value = response.token
    } catch (error) {
      console.error('JWT token refresh failed:', error)
      await logout()
      throw error
    }
  }

  const initializeAuth = async (): Promise<void> => {
    // 首先尝试从本地存储恢复用户信息，避免状态闪烁
    const savedToken = getToken()
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      try {
        // 立即恢复用户状态，避免UI闪烁
        token.value = savedToken
        user.value = JSON.parse(savedUser)
        
        // 然后在后台验证token是否仍然有效
        try {
          const isValid = await validateSession()
        } catch (error) {
          console.error('JWT token validation failed during background check:', error)
          // Token无效时才清除状态
          await logout()
        }
      } catch (error) {
        console.error('Failed to parse saved user data:', error)
        await logout()
      }
    } else {
      // 确保状态被清除
      user.value = null
      token.value = null
    }
  }

  return {
    // State
    user,
    token,
    refreshToken,
    isLoading,
    // Getters
    isAuthenticated,
    userRole,
    quotaPercentage,
    // Actions
    login,
    register,
    logout,
    fetchUser,
    updateProfile,
    refreshUserToken,
    initializeAuth,
    validateSession,
    getVerificationCode
  }
})