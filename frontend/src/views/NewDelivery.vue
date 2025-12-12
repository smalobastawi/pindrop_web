<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">New Delivery</h1>
    <router-link to="/deliveries" class="btn btn-outline-secondary">
      Back to Deliveries
    </router-link>
  </div>

  <div class="row">
    <div class="col-md-8">
      <div class="card">
        <div class="card-header">
          <h5>Create New Delivery</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="createDelivery">
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Customer</label>
                <select v-model="form.customer_id" class="form-select" required>
                  <option value="">Select Customer</option>
                  <option value="1">John Doe</option>
                  <option value="2">Jane Smith</option>
                </select>
              </div>
              <div class="col-md-6">
                <label class="form-label">Driver</label>
                <select v-model="form.driver_id" class="form-select">
                  <option value="">Unassigned</option>
                  <option value="1">Driver A</option>
                  <option value="2">Driver B</option>
                </select>
              </div>
            </div>

            <div class="mb-3">
              <h6>Package Details</h6>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-8">
                <label class="form-label">Description</label>
                <input v-model="form.package.description" type="text" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Type</label>
                <select v-model="form.package.package_type" class="form-select" required>
                  <option value="">Select Type</option>
                  <option value="document">Document</option>
                  <option value="parcel">Parcel</option>
                  <option value="fragile">Fragile</option>
                  <option value="perishable">Perishable</option>
                </select>
              </div>
            </div>

            <div class="row mb-3">
              <div class="col-md-4">
                <label class="form-label">Weight (kg)</label>
                <input v-model.number="form.package.weight" type="number" step="0.1" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Dimensions</label>
                <input v-model="form.package.dimensions" type="text" class="form-control" placeholder="LxWxH" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Value</label>
                <input v-model.number="form.package.value" type="number" class="form-control" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Special Instructions</label>
              <textarea v-model="form.package.special_instructions" class="form-control" rows="2"></textarea>
            </div>

            <div class="mb-3">
              <h6>Delivery Details</h6>
            </div>

            <div class="mb-3">
              <label class="form-label">Pickup Address</label>
              <textarea v-model="form.delivery.pickup_address" class="form-control" rows="2" required></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Delivery Address</label>
              <textarea v-model="form.delivery.delivery_address" class="form-control" rows="2" required></textarea>
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Estimated Pickup</label>
                <input v-model="form.delivery.estimated_pickup" type="datetime-local" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Estimated Delivery</label>
                <input v-model="form.delivery.estimated_delivery" type="datetime-local" class="form-control" required />
              </div>
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Priority</label>
                <select v-model="form.delivery.priority" class="form-select">
                  <option value="1">Normal</option>
                  <option value="2">Express</option>
                  <option value="3">Urgent</option>
                </select>
              </div>
              <div class="col-md-6">
                <label class="form-label">Delivery Fee</label>
                <input v-model.number="form.delivery.delivery_fee" type="number" step="0.01" class="form-control" />
              </div>
            </div>

            <div class="mb-3">
              <h6>Payment Details</h6>
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Amount</label>
                <input v-model.number="form.payment.amount" type="number" step="0.01" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Payment Method</label>
                <select v-model="form.payment.payment_method" class="form-select">
                  <option value="cash">Cash</option>
                  <option value="card">Card</option>
                  <option value="bank">Bank Transfer</option>
                  <option value="mobile">Mobile Money</option>
                </select>
              </div>
            </div>

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <router-link to="/deliveries" class="btn btn-outline-secondary me-md-2">
                Cancel
              </router-link>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                Create Delivery
              </button>
            </div>
          </form>

          <div v-if="error" class="alert alert-danger mt-3">
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  customer_id: '',
  driver_id: '',
  package: {
    description: '',
    weight: '',
    dimensions: '',
    package_type: '',
    value: '',
    special_instructions: ''
  },
  delivery: {
    pickup_address: '',
    delivery_address: '',
    estimated_pickup: '',
    estimated_delivery: '',
    priority: 1,
    delivery_fee: ''
  },
  payment: {
    amount: '',
    payment_method: 'cash'
  }
})

const loading = ref(false)
const error = ref('')

const createDelivery = async () => {
  try {
    loading.value = true
    error.value = ''

    // Simulate API call
    console.log('Creating delivery:', form.value)
    
    // In a real app, you would make an API call here
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    alert('Delivery created successfully!')
    router.push('/deliveries')
  } catch (err) {
    error.value = 'Failed to create delivery. Please try again.'
    console.error('Create delivery error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

h6 {
  color: #495057;
  font-weight: 600;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
}
</style>