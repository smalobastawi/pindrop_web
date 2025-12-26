<!-- frontend/src/views/CustomerRegister.vue -->
<template>
   <CommonHeader />
    <br>
    <br>
    <br>
  <div class="registration-page">
  
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">Customer Registration</h4>
            </div>
            <div class="card-body">
            
            <form @submit.prevent="handleRegister">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="first_name" class="form-label">First Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="first_name"
                    v-model="form.first_name"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="last_name" class="form-label">Last Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="last_name"
                    v-model="form.last_name"
                    required
                  />
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email *</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="form.email"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="phone" class="form-label">Phone *</label>
                  <input
                    type="tel"
                    class="form-control"
                    id="phone"
                    v-model="form.phone"
                    required
                  />
                </div>
              </div>
              
              <div class="mb-3">
                <label for="address" class="form-label">Address *</label>
                <textarea
                  class="form-control"
                  id="address"
                  rows="3"
                  v-model="form.address"
                  required
                ></textarea>
              </div>
              
              
              <div class="mb-3">
                <label for="password" class="form-label">Password *</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password *</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  required
                />
              </div>
              
              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              
              <div class="d-grid">
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  Register as Customer
                </button>
              </div>
            </form>

            <div class="mt-3 text-center">
              <p>Or</p>
              <GoogleSignInButton @success="handleGoogleSignUp" @error="handleGoogleError" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Common Footer -->
    <CommonFooter />
  </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'
import axios from 'axios'
import { GoogleSignInButton } from 'vue3-google-signin'
import CommonHeader from '@/components/layout/CommonHeader.vue'
import CommonFooter from '@/components/layout/CommonFooter.vue'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  confirmPassword: '',
  preferred_language: 'en',
  push_enabled: true
})

const handleRegister = async () => {
  error.value = ''

  // Validate passwords match
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }

  // Validate password strength
  if (form.password.length < 6) {
    error.value = 'Password must be at least 6 characters long'
    return
  }

  loading.value = true

  try {
    const response = await customerAPI.register({
      first_name: form.first_name,
      last_name: form.last_name,
      email: form.email,
      phone: form.phone,
      address: form.address,
      password: form.password
    })

    if (response.data.message) {
      // Auto-login after successful registration
      try {
        const loginResponse = await axios.post('/api/token/', {
          username: form.email,
          password: form.password
        })

        // Store tokens
        localStorage.setItem('access_token', loginResponse.data.access)
        localStorage.setItem('refresh_token', loginResponse.data.refresh)

        toast.success('Registration and login successful!')
        router.push('/customer-portal')
      } catch (loginErr) {
        // If auto-login fails, redirect to login page
        toast.success('Registration successful! Please log in.')
        router.push('/customer-portal/login')
      }
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleGoogleSignUp = async (response) => {
  try {
    // Send credential to backend for authentication
    const loginResponse = await axios.post('/api/google-login/', {
      credential: response.credential
    })

    // Store tokens
    localStorage.setItem('access_token', loginResponse.data.access)
    localStorage.setItem('refresh_token', loginResponse.data.refresh)

    toast.success('Google sign-in successful! Redirecting to dashboard...')
    router.push('/customer-portal')
  } catch (err) {
    console.error('Google sign-up error:', err)
    toast.error('Google sign-in failed. Please try again.')
  }
}

const handleGoogleError = (error) => {
  console.error('Google sign-up error:', error)
  toast.error('Google sign-up failed.')
}
</script>

<style scoped>
.card {
  border-radius: 10px;
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
}
</style>