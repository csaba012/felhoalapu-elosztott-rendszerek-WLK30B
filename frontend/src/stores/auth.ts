import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import type { User, LoginRequest, RegisterRequest, LoginResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    } else {
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }

  const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', credentials)
    setToken(response.data.access_token)
    user.value = response.data.user
    return response.data
  }

  const register = async (credentials: RegisterRequest): Promise<void> => {
    await api.post('/auth/register', credentials)
  }

  const logout = () => {
    setToken(null)
    user.value = null
  }

  const checkAuth = async (): Promise<void> => {
    if (token.value) {
      try {
        const response = await api.get<User>('/auth/me')
        user.value = response.data
      } catch (error) {
        logout()
      }
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth
  }
})
