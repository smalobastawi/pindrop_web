// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

// Configure axios
axios.defaults.baseURL = 'http://localhost:8000/api'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Add token to requests if exists
axios.interceptors.request.use(
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
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post('/token/refresh/', {
          refresh: refreshToken
        })
        
        localStorage.setItem('access_token', response.data.access)
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`
        
        return axios(originalRequest)
      } catch (refreshError) {
        // Redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.use(Vue3Toastify, {
  autoClose: 3000,
  position: 'top-right',
  theme: 'colored'
})

app.mount('#app')