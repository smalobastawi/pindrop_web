<!-- frontend/src/views/CustomerRegister.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">User Registration</h4>
          </div>
          <div class="card-body">
            <!-- User Type Selection -->
            <div class="mb-4">
              <h6>Select Registration Type</h6>
              <div class="row">
                <div class="col-md-6">
                  <div class="card h-100" :class="{ 'border-primary': form.user_type === 'customer', 'border-2': form.user_type === 'customer' }">
                    <div class="card-body text-center">
                      <input 
                        type="radio" 
                        class="form-check-input" 
                        id="customer" 
                        value="customer" 
                        v-model="form.user_type"
                      >
                      <label for="customer" class="form-check-label w-100">
                        <i class="bi bi-person-fill fs-2 d-block mb-2"></i>
                        <strong>Customer</strong>
                        <p class="text-muted small mt-2">Place orders and track deliveries</p>
                      </label>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card h-100" :class="{ 'border-primary': form.user_type === 'rider', 'border-2': form.user_type === 'rider' }">
                    <div class="card-body text-center">
                      <input 
                        type="radio" 
                        class="form-check-input" 
                        id="rider" 
                        value="rider" 
                        v-model="form.user_type"
                      >
                      <label for="rider" class="form-check-label w-100">
                        <i class="bi bi-truck fs-2 d-block mb-2"></i>
                        <strong>Rider</strong>
                        <p class="text-muted small mt-2">Deliver packages and earn income</p>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
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
              
              <!-- Rider-specific fields -->
              <div v-if="form.user_type === 'rider'" class="rider-fields">
                <hr class="my-4">
                <h6 class="text-primary">Rider Information</h6>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="license_number" class="form-label">License Number *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="license_number"
                      v-model="form.license_number"
                      required
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="vehicle_type" class="form-label">Vehicle Type *</label>
                    <select class="form-control" id="vehicle_type" v-model="form.vehicle_type" required>
                      <option value="">Select Vehicle</option>
                      <option value="bicycle">Bicycle</option>
                      <option value="motorcycle">Motorcycle</option>
                      <option value="car">Car</option>
                      <option value="van">Van</option>
                      <option value="truck">Truck</option>
                    </select>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="vehicle_plate" class="form-label">Vehicle Plate *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="vehicle_plate"
                      v-model="form.vehicle_plate"
                      required
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="vehicle_model" class="form-label">Vehicle Model</label>
                    <input
                      type="text"
                      class="form-control"
                      id="vehicle_model"
                      v-model="form.vehicle_model"
                    />
                  </div>
                </div>
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
                  {{ form.user_type === 'rider' ? 'Register as Rider' : 'Register as Customer' }}
                </button>
              </div>
            </form>
            
            <div v-else class="text-center">
              <div class="alert alert-success">
                <h5>Registration Successful!</h5>
                <p v-if="form.user_type === 'rider'">
                  Your rider application has been submitted. You will receive approval notification after review.
                </p>
                <p v-else>
                  Your account has been created. You can now log in to access your customer portal.
                </p>
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
  user_type: 'customer',
  password: '',
  confirmPassword: '',
  // Rider-specific fields
  license_number: '',
  vehicle_type: '',
  vehicle_plate: '',
  vehicle_model: ''
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
  
  // Validate rider fields if user type is rider
  if (form.user_type === 'rider') {
    if (!form.license_number || !form.vehicle_type || !form.vehicle_plate) {
      error.value = 'Please fill in all required rider information'
      return
    }
  }
  
  loading.value = true
  
  try {
    let response
    if (form.user_type === 'rider') {
      response = await customerAPI.registerRider({
        name: form.name,
        email: form.email,
        phone: form.phone,
        address: form.address,
        license_number: form.license_number,
        vehicle_type: form.vehicle_type,
        vehicle_plate: form.vehicle_plate,
        vehicle_model: form.vehicle_model,
        password: form.password
      })
    } else {
      response = await customerAPI.register({
        name: form.name,
        email: form.email,
        phone: form.phone,
        address: form.address,
        user_type: form.user_type,
        password: form.password
      })
    }
    
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