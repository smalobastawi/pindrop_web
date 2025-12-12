// frontend/src/api/customers.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
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
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
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
  // Customer registration
  register(customerData) {
    return api.post('/customer/register/', customerData)
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
  }
}

export default api