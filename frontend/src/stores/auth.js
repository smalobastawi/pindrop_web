// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)

  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/token/', credentials)
  
      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh
  
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
  
      // Fetch user data
      await fetchUser()
  
      router.push('/dashboard')
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      }
    }
  }

  const fetchUser = async () => {
    try {
      const response = await axios.get('/user/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    router.push('/login')
  }

  // Initialize user if token exists
  if (accessToken.value) {
    fetchUser()
  }

  const registerRider = async (registrationData) => {
    try {
      const response = await axios.post('/api/register/rider/', registrationData)
      
      return {
        success: true,
        message: 'Rider registration successful',
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Registration failed',
        error: error.response?.data
      }
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    logout,
    fetchUser,
    registerRider
  }
})