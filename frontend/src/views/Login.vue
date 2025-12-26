<template>
  <div>
    <!-- Common Header -->
    <CommonHeader />
    
    <div class="container" style="margin-top: 100px;">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3 class="text-center">Admin Login</h3>
            </div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  v-model="credentials.username"
                  type="text"
                  class="form-control"
                  id="username"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  v-model="credentials.password"
                  type="password"
                  class="form-control"
                  id="password"
                  required
                />
              </div>
              <div class="mb-3 form-check">
                <input
                  v-model="credentials.remember"
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
            <div v-if="error" class="alert alert-danger mt-3">
              {{ error }}
            </div>
            <div class="mt-3 text-center">
              <router-link to="/customer-login" class="text-decoration-none">
                Customer Login
              </router-link>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '@/stores/adminAuth'
import CommonHeader from '@/components/layout/CommonHeader.vue'
import CommonFooter from '@/components/layout/CommonFooter.vue'

const router = useRouter()
const adminAuthStore = useAdminAuthStore()

const credentials = ref({
  username: '',
  password: '',
  remember: false
})

const loading = ref(false)
const error = ref('')

const login = async () => {
  try {
    loading.value = true
    error.value = ''

    await adminAuthStore.login({
      username: credentials.value.username,
      password: credentials.value.password
    })

    router.push('/admin')
  } catch (err) {
    error.value = adminAuthStore.error || 'Login failed. Please try again.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
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