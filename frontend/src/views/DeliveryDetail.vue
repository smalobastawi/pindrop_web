<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Delivery Details</h1>
    <router-link to="/deliveries" class="btn btn-outline-secondary">
      Back to Deliveries
    </router-link>
  </div>

  <div class="row">
    <div class="col-md-8">
      <div class="card mb-3">
        <div class="card-header">
          <h5>Delivery Information</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Tracking Number:</strong>
              <p>{{ delivery.tracking_number }}</p>
            </div>
            <div class="col-md-6">
              <strong>Status:</strong>
              <span class="badge" :class="getStatusClass(delivery.status)">
                {{ delivery.status }}
              </span>
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Customer:</strong>
              <p>{{ delivery.customer?.name }}</p>
              <small class="text-muted">{{ delivery.customer?.email }}</small>
            </div>
            <div class="col-md-6">
              <strong>Driver:</strong>
              <p>{{ delivery.driver?.name || 'Unassigned' }}</p>
            </div>
          </div>

          <div class="mb-3">
            <strong>Pickup Address:</strong>
            <p>{{ delivery.pickup_address }}</p>
          </div>

          <div class="mb-3">
            <strong>Delivery Address:</strong>
            <p>{{ delivery.delivery_address }}</p>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Estimated Pickup:</strong>
              <p>{{ formatDateTime(delivery.estimated_pickup) }}</p>
            </div>
            <div class="col-md-6">
              <strong>Estimated Delivery:</strong>
              <p>{{ formatDateTime(delivery.estimated_delivery) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-header">
          <h5>Package Details</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-8">
              <strong>Description:</strong>
              <p>{{ delivery.package?.description }}</p>
            </div>
            <div class="col-md-4">
              <strong>Type:</strong>
              <span class="badge bg-secondary">{{ delivery.package?.package_type }}</span>
            </div>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-4">
              <strong>Weight:</strong>
              <p>{{ delivery.package?.weight }} kg</p>
            </div>
            <div class="col-md-4">
              <strong>Dimensions:</strong>
              <p>{{ delivery.package?.dimensions || 'N/A' }}</p>
            </div>
            <div class="col-md-4">
              <strong>Value:</strong>
              <p>{{ formatCurrency(delivery.package?.value) }}</p>
            </div>
          </div>

          <div v-if="delivery.package?.special_instructions" class="mb-3">
            <strong>Special Instructions:</strong>
            <p>{{ delivery.package.special_instructions }}</p>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-header">
          <h5>Status Updates</h5>
        </div>
        <div class="card-body">
          <div v-if="delivery.status_updates && delivery.status_updates.length > 0">
            <div v-for="update in delivery.status_updates" :key="update.id" class="mb-3">
              <div class="d-flex justify-content-between">
                <span class="badge" :class="getStatusClass(update.status)">{{ update.status }}</span>
                <small class="text-muted">{{ formatDateTime(update.created_at) }}</small>
              </div>
              <p class="mb-1">{{ update.notes }}</p>
              <small v-if="update.location" class="text-muted">
                📍 {{ update.location }}
              </small>
              <hr>
            </div>
          </div>
          <p v-else class="text-muted">No status updates yet.</p>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card mb-3">
        <div class="card-header">
          <h5>Payment</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-6">
              <strong>Amount:</strong>
              <p>{{ formatCurrency(delivery.payment?.amount) }}</p>
            </div>
            <div class="col-6">
              <strong>Method:</strong>
              <p>{{ delivery.payment?.payment_method || 'N/A' }}</p>
            </div>
          </div>
          <div class="mb-3">
            <strong>Status:</strong>
            <span class="badge" :class="getPaymentStatusClass(delivery.payment?.status)">
              {{ delivery.payment?.status || 'pending' }}
            </span>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-header">
          <h5>Actions</h5>
        </div>
        <div class="card-body">
          <button @click="showStatusUpdateModal = true" class="btn btn-primary w-100 mb-2">
            Update Status
          </button>
          <button class="btn btn-outline-secondary w-100 mb-2">
            Print Receipt
          </button>
          <button class="btn btn-outline-danger w-100">
            Cancel Delivery
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Status Update Modal -->
  <div v-if="showStatusUpdateModal" class="modal show d-block" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Update Delivery Status</h5>
          <button type="button" class="btn-close" @click="showStatusUpdateModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Status</label>
            <select v-model="statusUpdate.status" class="form-select">
              <option value="assigned">Assigned</option>
              <option value="picked_up">Picked Up</option>
              <option value="in_transit">In Transit</option>
              <option value="delivered">Delivered</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Location</label>
            <input v-model="statusUpdate.location" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Notes</label>
            <textarea v-model="statusUpdate.notes" class="form-control" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showStatusUpdateModal = false">
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="updateStatus">
            Update Status
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const deliveryId = route.params.id

const delivery = ref({
  tracking_number: 'PKG123456789ABC',
  status: 'pending',
  customer: {
    name: 'John Doe',
    email: 'john@example.com'
  },
  driver: null,
  pickup_address: 'Westlands, Nairobi',
  delivery_address: 'Karen, Nairobi',
  estimated_pickup: '2025-12-13T10:00:00Z',
  estimated_delivery: '2025-12-13T16:00:00Z',
  package: {
    description: 'Laptop Computer',
    package_type: 'fragile',
    weight: 2.5,
    dimensions: '35x25x5',
    value: 50000,
    special_instructions: 'Handle with care'
  },
  payment: {
    amount: 250.00,
    payment_method: 'cash',
    status: 'pending'
  },
  status_updates: []
})

const showStatusUpdateModal = ref(false)
const statusUpdate = ref({
  status: '',
  location: '',
  notes: ''
})

const getStatusClass = (status) => {
  const classes = {
    'pending': 'bg-warning',
    'assigned': 'bg-info',
    'picked_up': 'bg-primary',
    'in_transit': 'bg-primary',
    'delivered': 'bg-success',
    'failed': 'bg-danger',
    'cancelled': 'bg-secondary'
  }
  return classes[status] || 'bg-secondary'
}

const getPaymentStatusClass = (status) => {
  const classes = {
    'pending': 'bg-warning',
    'paid': 'bg-success',
    'failed': 'bg-danger',
    'refunded': 'bg-info'
  }
  return classes[status] || 'bg-secondary'
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const updateStatus = () => {
  console.log('Updating status:', statusUpdate.value)
  showStatusUpdateModal.value = false
  // In a real app, you would make an API call here
}

onMounted(() => {
  console.log('Loading delivery:', deliveryId)
})
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

.badge {
  font-size: 0.75em;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>