<!-- frontend/src/views/CustomerRegister.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">Customer Registration</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister" v-if="!registered">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <label for="name" class="form-label">Full Name *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="name"
                    v-model="form.name"
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
                  Register
                </button>
              </div>
            </form>
            
            <div v-else class="text-center">
              <div class="alert alert-success">
                <h5>Registration Successful!</h5>
                <p>Your account has been created. You can now log in to access your customer portal.</p>
              </div>
              <router-link to="/customer-login" class="btn btn-primary">
                Go to Login
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'

const router = useRouter()
const loading = ref(false)
const registered = ref(false)
const error = ref('')

const form = reactive({
  name: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  confirmPassword: ''
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
      name: form.name,
      email: form.email,
      phone: form.phone,
      address: form.address,
      password: form.password
    })
    
    if (response.data.message) {
      registered.value = true
      toast.success('Registration successful!')
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
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