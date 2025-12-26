<template>
  <AdminLayout>
    <div class="admin-new-delivery">
      <div class="page-header">
        <h1>Create New Delivery</h1>
        <p>Enter sender and recipient details to create a new delivery order</p>
      </div>

      <div class="row">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h5>Delivery Information</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="createDelivery">
                <!-- Sender Details -->
                <div class="mb-4">
                  <h6 class="section-title">Sender Details</h6>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Sender Name *</label>
                      <input v-model="form.sender_name" type="text" class="form-control" required />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Sender Phone *</label>
                      <input v-model="form.sender_phone" type="tel" class="form-control" required />
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Sender Email</label>
                      <input v-model="form.sender_email" type="email" class="form-control" />
                    </div>
                    <div class="col-md-6">
                      <AddressSelector
                        v-model="form.sender_address"
                        label="Sender Address *"
                        placeholder="Search for sender location..."
                        address-placeholder="Street, City, Country"
                        :rows="1"
                        required
                      />
                    </div>
                  </div>
                </div>

                <!-- Recipient Details -->
                <div class="mb-4">
                  <h6 class="section-title">Recipient Details</h6>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Recipient Name *</label>
                      <input v-model="form.recipient_name" type="text" class="form-control" required />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Recipient Phone *</label>
                      <input v-model="form.recipient_phone" type="tel" class="form-control" required />
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Recipient Address *</label>
                    <textarea v-model="form.recipient_address" class="form-control" rows="2" required></textarea>
                  </div>
                </div>

                <!-- Package Details -->
                <div class="mb-4">
                  <h6 class="section-title">Package Details</h6>
                  <div class="row mb-3">
                    <div class="col-md-8">
                      <label class="form-label">Description *</label>
                      <input v-model="form.package_description" type="text" class="form-control" required />
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Type *</label>
                      <select v-model="form.package_type" class="form-select" required>
                        <option value="">Select Type</option>
                        <option value="document">Document</option>
                        <option value="parcel">Parcel</option>
                        <option value="fragile">Fragile</option>
                        <option value="perishable">Perishable</option>
                        <option value="electronic">Electronic</option>
                        <option value="clothing">Clothing</option>
                        <option value="food">Food</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-4">
                      <label class="form-label">Weight (kg) *</label>
                      <input v-model.number="form.package_weight" type="number" step="0.1" class="form-control" required />
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Length (cm)</label>
                      <input v-model.number="form.package_length" type="number" step="0.1" class="form-control" />
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Width (cm)</label>
                      <input v-model.number="form.package_width" type="number" step="0.1" class="form-control" />
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-4">
                      <label class="form-label">Height (cm)</label>
                      <input v-model.number="form.package_height" type="number" step="0.1" class="form-control" />
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Declared Value</label>
                      <input v-model.number="form.declared_value" type="number" step="0.01" class="form-control" />
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Special Instructions</label>
                      <input v-model="form.special_instructions" type="text" class="form-control" />
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-4">
                      <div class="form-check">
                        <input v-model="form.is_fragile" class="form-check-input" type="checkbox" id="is_fragile" />
                        <label class="form-check-label" for="is_fragile">Fragile</label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check">
                        <input v-model="form.is_perishable" class="form-check-input" type="checkbox" id="is_perishable" />
                        <label class="form-check-label" for="is_perishable">Perishable</label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check">
                        <input v-model="form.requires_signature" class="form-check-input" type="checkbox" id="requires_signature" />
                        <label class="form-check-label" for="requires_signature">Requires Signature</label>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Delivery Details -->
                <div class="mb-4">
                  <h6 class="section-title">Delivery Details</h6>
                  <div class="mb-3">
                    <AddressSelector
                      v-model="form.pickup_address"
                      label="Pickup Address *"
                      placeholder="Search for pickup location..."
                      address-placeholder="Enter or select pickup address"
                      required
                    />
                  </div>

                  <div class="mb-3">
                    <AddressSelector
                      v-model="form.delivery_address"
                      label="Delivery Address *"
                      placeholder="Search for delivery location..."
                      address-placeholder="Enter or select delivery address"
                      required
                    />
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Estimated Pickup *</label>
                      <input v-model="form.estimated_pickup" type="datetime-local" class="form-control" required />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Estimated Delivery *</label>
                      <input v-model="form.estimated_delivery" type="datetime-local" class="form-control" required />
                    </div>
                  </div>

                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Priority *</label>
                      <select v-model="form.priority" class="form-select" required>
                        <option :value="1">Normal (24-48 hours)</option>
                        <option :value="2">Express (12-24 hours)</option>
                        <option :value="3">Urgent (2-6 hours)</option>
                        <option :value="4">Same Day (1-2 hours)</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Delivery Fee *</label>
                      <input v-model.number="form.delivery_fee" type="number" step="0.01" class="form-control" required />
                    </div>
                  </div>
                </div>

                <!-- Payment Details -->
                <div class="mb-4">
                  <h6 class="section-title">Payment Details</h6>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Payment Amount *</label>
                      <input v-model.number="form.payment_amount" type="number" step="0.01" class="form-control" required />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Payment Method *</label>
                      <select v-model="form.payment_method" class="form-select" required>
                        <option value="cash">Cash on Delivery</option>
                        <option value="card">Credit/Debit Card</option>
                        <option value="bank">Bank Transfer</option>
                        <option value="mobile">Mobile Money</option>
                        <option value="wallet">Wallet Balance</option>
                      </select>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">COD Amount</label>
                    <input v-model.number="form.cod_amount" type="number" step="0.01" class="form-control" />
                  </div>
                </div>

                <!-- Optional Rider Assignment -->
                <div class="mb-4">
                  <h6 class="section-title">Rider Assignment (Optional)</h6>
                  <div class="mb-3">
                    <label class="form-label">Assign to Rider</label>
                    <select v-model="form.rider_id" class="form-select">
                      <option value="">Unassigned</option>
                      <option v-for="rider in availableRiders" :key="rider.id" :value="rider.id">
                        {{ rider.name }} ({{ rider.vehicle_type }} - {{ rider.vehicle_plate }})
                      </option>
                    </select>
                  </div>
                </div>

                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                  <router-link to="/admin/deliveries" class="btn btn-outline-secondary me-md-2">
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
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import { useAdminAuthStore } from '@/stores/adminAuth'
import AddressSelector from '@/components/AddressSelector.vue'

const router = useRouter()
const adminAuth = useAdminAuthStore()

const form = ref({
  // Sender
  sender_name: '',
  sender_phone: '',
  sender_email: '',
  sender_address: '',

  // Recipient
  recipient_name: '',
  recipient_phone: '',
  recipient_address: '',

  // Package
  package_description: '',
  package_weight: '',
  package_length: null,
  package_width: null,
  package_height: null,
  package_type: '',
  declared_value: 0,
  special_instructions: '',
  is_fragile: false,
  is_perishable: false,
  requires_signature: false,

  // Delivery
  pickup_address: '',
  delivery_address: '',
  estimated_pickup: '',
  estimated_delivery: '',
  priority: 1,
  delivery_fee: '',

  // Payment
  payment_amount: '',
  payment_method: 'cash',
  cod_amount: 0,

  // Rider
  rider_id: null
})

const loading = ref(false)
const error = ref('')
const availableRiders = ref([])

const fetchAvailableRiders = async () => {
  try {
    const response = await fetch('/admin-api/api/riders/active_riders/', {
      headers: {
        'Authorization': `Bearer ${adminAuth.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      availableRiders.value = data.riders || []
    }
  } catch (err) {
    console.error('Error fetching riders:', err)
  }
}

const createDelivery = async () => {
  try {
    loading.value = true
    error.value = ''

    const data = { ...form.value }
    if (data.rider_id === '') {
      data.rider_id = null
    }

    const response = await fetch('/admin-api/api/deliveries/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${adminAuth.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    if (response.ok) {
      const data = await response.json()
      alert('Delivery created successfully!')
      router.push('/admin/deliveries')
    } else {
      const errorData = await response.json()
      error.value = errorData.error || 'Failed to create delivery. Please try again.'
    }
  } catch (err) {
    error.value = 'Failed to create delivery. Please try again.'
    console.error('Create delivery error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAvailableRiders()
})
</script>

<style scoped>
.admin-new-delivery {
  padding: 0;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.section-title {
  color: #495057;
  font-weight: 600;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.btn {
  border-radius: 0.375rem;
}
</style>