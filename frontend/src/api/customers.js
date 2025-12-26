// frontend/src/api/customers.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'}/token/refresh/`, {
          refresh: refreshToken
        })
        
        localStorage.setItem('access_token', response.data.access)
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`
        
        return api(originalRequest)
      } catch (refreshError) {
        // Redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/customer-login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export const customerAPI = {
  // Registration endpoints
  register(customerData) {
    return api.post('/register/customer/', customerData)
  },
  
  registerRider(riderData) {
    return api.post('/register/rider/', riderData)
  },
  
  // Unified registration
  registerUnified(userData) {
    return api.post('/register/', userData)
  },
  
  // Customer portal (login required)
  getPortal() {
    return api.get('/customer/portal/')
  },
  
  // Create new order (login required)
  createOrder(orderData) {
    return api.post('/customer/portal/', orderData)
  },
  
  // Track order by tracking number
  trackOrder(trackingNumber) {
    return api.get('/customer/track/', {
      params: { tracking_number: trackingNumber }
    })
  },
  
  // Get specific order details
  getOrder(orderId) {
    return api.get(`/deliveries/${orderId}/`)
  },
  
  // Get customer orders
  getOrders() {
    return api.get('/customer/portal/')
  },
  
  // Mobile app endpoints
  getMobileVersion() {
    return api.get('/mobile/version/')
  },
  
  getMobileProfile() {
    return api.get('/mobile/profile/')
  },
  
  updateMobileProfile(profileData) {
    return api.put('/mobile/profile/', profileData)
  },
  
  registerDeviceToken(deviceToken, userType = 'customer') {
    return api.post('/mobile/device-token/', {
      device_token: deviceToken,
      user_type: userType
    })
  }
}

export default api