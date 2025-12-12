<!-- frontend/src/components/TrackOrder.vue -->
<template>
  <div class="track-order">
    <!-- Search Form -->
    <div v-if="!trackingData" class="mb-4">
      <div class="input-group">
        <input
          type="text"
          class="form-control"
          placeholder="Enter tracking number (e.g., PKG123456789ABC)"
          v-model="trackingNumber"
        />
        <button class="btn btn-primary" @click="handleTrack" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Track
        </button>
      </div>
      <div v-if="error" class="alert alert-danger mt-2">
        {{ error }}
      </div>
    </div>

    <!-- Tracking Results -->
    <div v-if="trackingData" class="tracking-results">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5>Order Tracking Results</h5>
        <button class="btn btn-sm btn-outline-secondary" @click="reset">
          Track Another Order
        </button>
      </div>

      <!-- Order Summary -->
      <div class="card mb-3">
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <h6>Tracking Number</h6>
              <p class="h5 text-primary">{{ trackingData.tracking_number }}</p>
            </div>
            <div class="col-md-6">
              <h6>Status</h6>
              <span :class="`badge bg-${getStatusColor(trackingData.status)} fs-6`">
                {{ trackingData.status.replace('_', ' ').toUpperCase() }}
              </span>
            </div>
          </div>
          <hr>
          <div class="row">
            <div class="col-md-6">
              <h6>Package</h6>
              <p>{{ trackingData.package?.description }}</p>
              <small class="text-muted">
                Weight: {{ trackingData.package?.weight }}kg | 
                Type: {{ trackingData.package?.package_type }}
              </small>
            </div>
            <div class="col-md-6">
              <h6>Delivery Address</h6>
              <p>{{ trackingData.delivery_address }}</p>
              <small class="text-muted">
                Pickup: {{ formatDate(trackingData.estimated_pickup) }}<br>
                Delivery: {{ formatDate(trackingData.estimated_delivery) }}
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Information -->
      <div v-if="trackingData.payment" class="card mb-3">
        <div class="card-body">
          <h6>Payment Information</h6>
          <div class="row">
            <div class="col-md-4">
              <strong>Amount:</strong> ${{ trackingData.payment.amount }}
            </div>
            <div class="col-md-4">
              <strong>Method:</strong> {{ trackingData.payment.payment_method.toUpperCase() }}
            </div>
            <div class="col-md-4">
              <strong>Status:</strong> 
              <span :class="`badge bg-${getPaymentStatusColor(trackingData.payment.status)}`">
                {{ trackingData.payment.status.toUpperCase() }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Status Timeline -->
      <div class="card">
        <div class="card-header">
          <h6 class="mb-0">Delivery Timeline</h6>
        </div>
        <div class="card-body">
          <div v-if="!trackingData.status_updates || trackingData.status_updates.length === 0">
            <p class="text-muted">No status updates available yet.</p>
          </div>
          <div v-else>
            <div class="timeline">
              <div 
                v-for="(update, index) in trackingData.status_updates" 
                :key="index"
                class="timeline-item"
                :class="{ 'active': index === 0 }"
              >
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                  <h6>{{ update.status.replace('_', ' ').toUpperCase() }}</h6>
                  <p class="text-muted mb-1">{{ formatDate(update.created_at) }}</p>
                  <p v-if="update.location" class="mb-1">
                    <i class="bi bi-geo-alt"></i> {{ update.location }}
                  </p>
                  <p v-if="update.notes" class="mb-0">
                    <i class="bi bi-chat-text"></i> {{ update.notes }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'

const trackingNumber = ref('')
const trackingData = ref(null)
const loading = ref(false)
const error = ref('')

const emit = defineEmits(['close'])

const handleTrack = async () => {
  if (!trackingNumber.value.trim()) {
    error.value = 'Please enter a tracking number'
    return
  }

  error.value = ''
  loading.value = true

  try {
    const response = await customerAPI.trackOrder(trackingNumber.value.trim())
    trackingData.value = response.data
    toast.success('Order found!')
  } catch (err) {
    error.value = err.response?.data?.error || 'Tracking number not found'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const reset = () => {
  trackingData.value = null
  trackingNumber.value = ''
  error.value = ''
}

const getStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'assigned': 'info',
    'picked_up': 'primary',
    'in_transit': 'primary',
    'delivered': 'success',
    'failed': 'danger',
    'cancelled': 'secondary'
  }
  return colors[status] || 'secondary'
}

const getPaymentStatusColor = (status) => {
  const colors = {
    'pending': 'warning',
    'paid': 'success',
    'failed': 'danger',
    'refunded': 'info'
  }
  return colors[status] || 'secondary'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}
</script>

<style scoped>
.timeline {
  position: relative;
  padding-left: 20px;
}

.timeline-item {
  position: relative;
  padding-bottom: 20px;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 8px;
  top: 20px;
  bottom: -20px;
  width: 2px;
  background: #dee2e6;
}

.timeline-marker {
  position: absolute;
  left: -12px;
  top: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #dee2e6;
  border: 2px solid #fff;
}

.timeline-item.active .timeline-marker {
  background: #0d6efd;
}

.timeline-content {
  margin-left: 20px;
}
</style>