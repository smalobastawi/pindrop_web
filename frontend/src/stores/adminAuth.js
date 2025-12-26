// adminAuth.js
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = '/admin-api'

export const useAdminAuthStore = defineStore('adminAuth', {
  state: () => ({
    user: null,
    token: null,
    permissions: [],
    isAuthenticated: false,
    loading: false,
    error: null,
    refreshInterceptor: null,
    responseInterceptor: null
  }),

  getters: {
    isAdmin: (state) => state.isAuthenticated && state.user?.role !== 'viewer',
    isSuperAdmin: (state) => state.user?.role === 'super_admin',
    canManageUsers: (state) => state.hasPermission('manage_users'),
    canManageSettings: (state) => state.hasPermission('manage_settings'),
    canManageDeliveries: (state) => state.hasPermission('manage_deliveries'),
    canViewReports: (state) => state.hasPermission('view_reports')
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null

      try {
        // For admin login, we'll use JWT token authentication
        const response = await axios.post(`${API_BASE_URL}/api/login/`, credentials)
        
        const { access, refresh } = response.data
        
        this.token = access
        this.isAuthenticated = true
        
        // Store token in localStorage
        localStorage.setItem('admin_access_token', access)
        localStorage.setItem('admin_refresh_token', refresh)
        
        // Set up axios defaults
        this.setupAxios()
        
        // Get user profile
        await this.fetchUserProfile()
        
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed'
        this.isAuthenticated = false
        this.token = null
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        // Clear state
        this.user = null
        this.token = null
        this.permissions = []
        this.isAuthenticated = false
        
        // Clear localStorage
        localStorage.removeItem('admin_access_token')
        localStorage.removeItem('admin_refresh_token')
        
        // Clear axios defaults
        delete axios.defaults.headers.common['Authorization']
        
      } catch (error) {
        console.error('Logout error:', error)
      }
    },

    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/users/me/`)
        this.user = response.data
        this.permissions = this.extractPermissions(response.data)
      } catch (error) {
        console.error('Failed to fetch user profile:', error)
        throw error
      }
    },

    async refreshToken() {
      try {
        const refresh = localStorage.getItem('admin_refresh_token')
        if (!refresh) {
          throw new Error('No refresh token available')
        }

        const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
          refresh
        })

        const { access } = response.data
        this.token = access
        localStorage.setItem('admin_access_token', access)
        
        // Update axios headers
        this.setupAxios()
        
        return access
      } catch (error) {
        console.error('Token refresh failed:', error)
        await this.logout()
        throw error
      }
    },

    setupAxios() {
      // Remove existing interceptor
      if (this.refreshInterceptor) {
        axios.interceptors.request.eject(this.refreshInterceptor)
      }

      // Add request interceptor to include auth token
      this.refreshInterceptor = axios.interceptors.request.use(
        (config) => {
          const token = this.token || localStorage.getItem('admin_access_token')
          if (token) {
            config.headers.Authorization = `Bearer ${token}`
          }
          return config
        },
        (error) => Promise.reject(error)
      )

      // Remove existing response interceptor
      if (this.responseInterceptor) {
        axios.interceptors.response.eject(this.responseInterceptor)
      }

      // Add response interceptor to handle token refresh
      this.responseInterceptor = axios.interceptors.response.use(
        (response) => response,
        async (error) => {
          const originalRequest = error.config

          if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            try {
              await this.refreshToken()
              return axios(originalRequest)
            } catch (refreshError) {
              await this.logout()
              window.location.href = '/login'
              return Promise.reject(refreshError)
            }
          }

          return Promise.reject(error)
        }
      )
    },

    extractPermissions(user) {
      const permissions = []
      
      // Super admin has all permissions
      if (user.role === 'super_admin') {
        return ['*']
      }

      // Add role-based permissions
      const rolePermissions = {
        admin: [
          'view_dashboard', 'manage_customers', 'manage_drivers',
          'manage_deliveries', 'manage_packages', 'view_reports',
          'manage_settings', 'manage_users'
        ],
        manager: [
          'view_dashboard', 'manage_customers', 'manage_drivers',
          'manage_deliveries', 'manage_packages', 'view_reports'
        ],
        operator: [
          'view_dashboard', 'manage_customers', 'manage_deliveries'
        ],
        viewer: ['view_dashboard', 'view_reports']
      }

      permissions.push(...(rolePermissions[user.role] || []))

      // Add custom role permissions
      if (user.custom_role?.permissions) {
        const customPermissions = user.custom_role.permissions
        Object.keys(customPermissions).forEach(key => {
          if (customPermissions[key]) {
            permissions.push(key)
          }
        })
      }

      return [...new Set(permissions)] // Remove duplicates
    },

    hasPermission(permission) {
      if (!this.isAuthenticated) return false
      
      // Super admin has all permissions
      if (this.permissions.includes('*')) return true
      
      return this.permissions.includes(permission)
    },

    async changePassword(passwordData) {
      try {
        await axios.post(`${API_BASE_URL}/api/users/change-password/`, passwordData)
        return { success: true }
      } catch (error) {
        throw new Error(error.response?.data?.message || 'Password change failed')
      }
    },

    async updateProfile(profileData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/api/users/${this.user.id}/update_profile/`, profileData)
        this.user = { ...this.user, ...response.data }
        return response.data
      } catch (error) {
        throw new Error(error.response?.data?.message || 'Profile update failed')
      }
    },

    // Initialize store from localStorage
    initialize() {
      try {
        const token = localStorage.getItem('admin_access_token')
        if (token) {
          this.token = token
          this.isAuthenticated = true
          this.setupAxios()
          
          // Try to fetch user profile
          this.fetchUserProfile().catch(() => {
            // If profile fetch fails, clear auth state
            this.logout()
          })
        }
      } catch (error) {
        console.error('Failed to initialize admin auth store:', error)
      }
    },

    // Method to check if store is properly initialized
    isReady() {
      return this.user !== null || this.token !== null
    }
  }
})