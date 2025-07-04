import { http } from '@/services/http'
import type { LoginForm, RegisterForm, User } from '@/types/auth'
import { setToken, removeToken, setRefreshToken, removeRefreshToken, getRefreshToken } from '@/utils/auth'

// Backend response format
interface BackendResponse<T = any> {
  code: number
  message: string
  data?: T
  token?: string // JWT token from backend
  refresh_token?: string // Refresh token from backend
}

export const authApi = {
  // Get verification code for registration
  getVerificationCode: async (email: string): Promise<void> => {
    const response = await http.get<string>(`/auth/mail/captcha?email=${email}`)
    if (response.status !== 200) {
      throw new Error('Failed to send verification code')
    }
  },

  // Register
  register: async (data: RegisterForm & { code: string }): Promise<void> => {
    const formData = new FormData()
    formData.append('username', data.email.split('@')[0]) // Use email prefix as username
    formData.append('email', data.email)
    formData.append('password', data.password)
    formData.append('password_confirm', data.password) // Backend expects password confirmation
    formData.append('code', data.code) // Backend expects 'code' not 'captcha'
    
    const response = await http.post<BackendResponse>('/auth/register', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      skipGlobalErrorHandling: true
    })
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
  },

  // Login
  login: async (data: LoginForm): Promise<{ user: User }> => {
    const formData = new FormData()
    formData.append('email', data.email)
    formData.append('password', data.password)
    
    
    
    const response = await http.post<BackendResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    // Save JWT token if provided
    if (response.data.token) {
      setToken(response.data.token)
      
      // 保存refresh token
      if (response.data.refresh_token) {
        setRefreshToken(response.data.refresh_token)
      } else {
        // 如果后端没有提供单独的refresh token，使用相同的token
        // 注意：根据后端实现，可能需要不同类型的token
        setRefreshToken(response.data.token)
      }
    } else {
      console.warn('⚠️ No token received from backend')
    }
    
    // 从后端响应中获取用户数据
    const backendUser = response.data.data
    
    // 创建符合前端User类型的用户对象
    const user: User = {
      id: backendUser.email,
      email: backendUser.email,
      name: backendUser.username,
      role: 'user' as const,
      status: 'active' as const,
      total_quota: backendUser.available_uses + backendUser.used_quota, // 总额度 = 剩余 + 已用
      used_quota: backendUser.used_quota,
      created_at: backendUser.join_time,
      updated_at: backendUser.join_time
    }
    
    return { user }
  },

  // Logout
  logout: async (): Promise<void> => {
    try {
      // Call backend logout endpoint if needed
      const response = await http.get<BackendResponse>('/auth/logout')
      
      if (response.data.code !== 200) {
        console.warn('Backend logout failed:', response.data.message)
      }
    } catch (error) {
      console.warn('Backend logout request failed:', error)
    } finally {
      // Always remove tokens locally
      removeToken()
    }
  },

  // Get user profile - updated to work with JWT
  getProfile: async (): Promise<User> => {
    const response = await http.get<BackendResponse>('/auth/me')
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    const backendUser = response.data.data
    
    // 创建符合前端User类型的用户对象
    const user: User = {
      id: backendUser.email,
      email: backendUser.email,
      name: backendUser.username,
      role: 'user' as const,
      status: 'active' as const,
      total_quota: backendUser.available_uses + backendUser.used_quota, // 总额度 = 剩余 + 已用
      used_quota: backendUser.used_quota,
      created_at: backendUser.join_time,
      updated_at: backendUser.join_time
    }
    
    return user
  },

  // Update user profile (mock implementation)
  updateProfile: async (data: Partial<User>): Promise<User> => {
    // Mock implementation
    const updatedUser: User = {
      id: 'current_user',
      email: 'current_user@example.com',
      name: data.name || 'Current User',
      role: 'user' as const,
      status: 'active' as const,
      total_quota: 100,
      used_quota: 10,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    return updatedUser
  },

  // Refresh JWT token
  refreshToken: async (): Promise<{ token: string }> => {
    try {
      // 获取refresh token
      const refreshToken = getRefreshToken()
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }
      
      // 使用refresh token作为Authorization头
      const response = await http.post<BackendResponse>('/auth/refresh-token', {}, {
        headers: {
          'Authorization': `Bearer ${refreshToken}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data.code === 200 && response.data.token) {
        setToken(response.data.token)
        return { token: response.data.token }
      } else {
        throw new Error(response.data.message || 'Token refresh failed')
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      removeToken()
      throw error
    }
  },

  // 验证当前用户会话 - 使用JWT token
  validateSession: async (): Promise<User> => {
    const response = await http.get<BackendResponse>('/auth/me')
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    const backendUser = response.data.data
    
    // 创建符合前端User类型的用户对象
    const user: User = {
      id: backendUser.email,
      email: backendUser.email,
      name: backendUser.username,
      role: 'user' as const,
      status: 'active' as const,
      total_quota: backendUser.available_uses + backendUser.used_quota, // 总额度 = 剩余 + 已用
      used_quota: backendUser.used_quota,
      created_at: backendUser.join_time,
      updated_at: backendUser.join_time
    }
    
    return user
  }
}