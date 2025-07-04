export interface LoginForm {
  email: string
  password: string
  remember: boolean
}

export interface RegisterForm {
  email: string
  password: string
  confirmPassword: string
  terms: boolean
}

export interface ForgotPasswordForm {
  email: string
}

export interface ResetPasswordForm {
  token: string
  password: string
  confirmPassword: string
}

export interface User {
  id: string
  email: string
  name?: string
  avatar?: string
  role: 'user' | 'admin'
  status: 'active' | 'inactive' | 'pending'
  total_quota: number
  used_quota: number
  created_at: string
  updated_at: string
}

export interface AuthResponse {
  user: User
  token: string
  refresh_token?: string
}

export interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
}