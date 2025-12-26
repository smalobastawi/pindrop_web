<!-- frontend/src/views/CustomerLogin.vue -->
<template>
  <div>
    <!-- Common Header -->
    <CommonHeader />
    
    <div class="container" style="margin-top: 100px;">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3 class="text-center">Customer Login</h3>
            </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  v-model="form.username"
                  type="text"
                  class="form-control"
                  id="username"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  id="password"
                  required
                />
              </div>
              <div class="mb-3 form-check">
                <input
                  v-model="form.remember"
                  type="checkbox"
                  class="form-check-input"
                  id="remember"
                />
                <label class="form-check-label" for="remember">
                  Remember me
                </label>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                Login
              </button>
            </form>
            <div class="mt-3 text-center">
              <p>Or</p>
              <GoogleSignInButton @success="handleGoogleLogin" @error="handleGoogleError" />
            </div>
            <div v-if="error" class="alert alert-danger mt-3">
              {{ error }}
            </div>
            <div class="mt-3 text-center">
              <router-link to="/customer-portal/register" class="text-decoration-none">
                Don't have an account? Register as Customer
              </router-link>
            </div>
            <div class="mt-2 text-center">
              <button @click="$router.push('/rider-login')" class="btn btn-outline-primary">
                Rider Login
              </button>
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
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { GoogleSignInButton } from 'vue3-google-signin'
import CommonHeader from '@/components/layout/CommonHeader.vue'
import CommonFooter from '@/components/layout/CommonFooter.vue'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await axios.post('/api/token/', {
      username: form.username,
      password: form.password
    })

    const { access, refresh } = response.data

    // Store tokens
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    // Fetch user profile to determine role
    const userResponse = await axios.get('/api/user/', {
      headers: { Authorization: `Bearer ${access}` }
    })

    const userType = userResponse.data.user_type

    toast.success('Login successful!')

    // Redirect based on role
    if (userType === 'rider' || userType === 'both') {
      router.push('/rider-portal')
    } else if (userType === 'customer') {
      router.push('/customer-portal')
    } else {
      // Admin or other
      router.push('/dashboard')
    }

  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleGoogleLogin = async (response) => {
  error.value = ''
  loading.value = true

  try {
    const res = await axios.post('/api/google-login/', {
      credential: response.credential
    })

    const { access, refresh } = res.data

    // Store tokens
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    toast.success('Login successful!')

    // Redirect to customer portal
    router.push('/customer-portal')

  } catch (err) {
    error.value = err.response?.data?.detail || 'Google login failed.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleGoogleError = (error) => {
  console.error('Google login error:', error)
  toast.error('Google login failed.')
}
</script>

<style scoped>
.container {
  margin-top: 100px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #007bff;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}
</style>