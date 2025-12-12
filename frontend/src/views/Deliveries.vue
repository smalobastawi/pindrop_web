<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Deliveries</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <div class="btn-group me-2">
        <router-link to="/deliveries/new" class="btn btn-sm btn-outline-secondary">
          New Delivery
        </router-link>
      </div>
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-striped table-sm">
      <thead>
        <tr>
          <th>Tracking #</th>
          <th>Customer</th>
          <th>Status</th>
          <th>Pickup Address</th>
          <th>Delivery Address</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="delivery in deliveries" :key="delivery.id">
          <td>{{ delivery.tracking_number }}</td>
          <td>{{ delivery.customer?.name }}</td>
          <td>
            <span class="badge" :class="getStatusClass(delivery.status)">
              {{ delivery.status }}
            </span>
          </td>
          <td>{{ delivery.pickup_address }}</td>
          <td>{{ delivery.delivery_address }}</td>
          <td>{{ formatDate(delivery.created_at) }}</td>
          <td>
            <router-link :to="`/deliveries/${delivery.id}`" class="btn btn-sm btn-outline-primary">
              View
            </router-link>
          </td>
        </tr>
        <tr v-if="deliveries.length === 0">
          <td colspan="7" class="text-center">No deliveries found</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Mock data for demonstration
const deliveries = ref([
  {
    id: 1,
    tracking_number: 'PKG123456789ABC',
    customer: { name: 'John Doe' },
    status: 'pending',
    pickup_address: 'Westlands, Nairobi',
    delivery_address: 'Karen, Nairobi',
    created_at: '2025-12-12T10:00:00Z'
  },
  {
    id: 2,
    tracking_number: 'PKG987654321DEF',
    customer: { name: 'Jane Smith' },
    status: 'in_transit',
    pickup_address: 'CBD, Nairobi',
    delivery_address: 'Eastlands, Nairobi',
    created_at: '2025-12-11T15:30:00Z'
  }
])

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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// In a real app, you would fetch data from your API here
onMounted(() => {
  // API call to fetch deliveries
  console.log('Fetching deliveries...')
})
</script>

<style scoped>
.table-responsive {
  margin-top: 2rem;
}

.badge {
  font-size: 0.75em;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>