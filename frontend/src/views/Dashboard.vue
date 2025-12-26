<!-- frontend/src/views/Dashboard.vue -->
<template>
  <div class="dashboard">
    <h1 class="h2 mb-4">Dashboard</h1>

    <!-- Status Alert for Pending Approval -->
    <div v-if="userStatus === 'pending_approval'" class="alert alert-warning alert-dismissible fade show" role="alert">
      <strong>Account Pending Approval</strong> Your rider account is currently under review. You will be notified once approved.
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h5 class="card-title">Total Deliveries</h5>
            <p class="card-text display-6">{{ stats.total || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h5 class="card-title">Delivered</h5>
            <p class="card-text display-6">{{ stats.delivered || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <h5 class="card-title">In Transit</h5>
            <p class="card-text display-6">{{ stats.in_transit || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-info">
          <div class="card-body">
            <h5 class="card-title">Pending</h5>
            <p class="card-text display-6">{{ stats.pending || 0 }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Deliveries -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">Recent Deliveries</h5>
      </div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Tracking #</th>
              <th>Customer</th>
              <th>Status</th>
              <th>Estimated Delivery</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="delivery in deliveries" :key="delivery.id">
              <td>{{ delivery.tracking_number }}</td>
              <td>{{ delivery.customer?.name }}</td>
              <td>
                <span :class="`badge bg-${getStatusColor(delivery.status)}`">
                  {{ delivery.status }}
                </span>
              </td>
              <td>{{ formatDate(delivery.estimated_delivery) }}</td>
              <td>
                <router-link :to="`/deliveries/${delivery.id}`" class="btn btn-sm btn-outline-primary">
                  View
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const router = useRouter()
const stats = ref({})
const deliveries = ref([])
const userStatus = ref('')
const userType = ref('')

const fetchDashboardData = async () => {
  try {
    const [statsRes, deliveriesRes, userRes] = await Promise.all([
      axios.get('/api/dashboard/'),
      axios.get('/deliveries/?limit=5'),
      axios.get('/api/mobile/profile/')
    ])

    stats.value = statsRes.data
    deliveries.value = deliveriesRes.data.results
    userStatus.value = userRes.data.profile?.status || ''
    userType.value = userRes.data.profile?.user_type || 'customer'

    // Dashboard content is role-based, no redirect needed
  } catch (error) {
    toast.error('Failed to fetch dashboard data')
    console.error('Dashboard error:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const getStatusColor = (status) => {
  const colorMap = {
    'pending': 'secondary',
    'assigned': 'info',
    'picked_up': 'primary',
    'in_transit': 'warning',
    'delivered': 'success',
    'failed': 'danger',
    'cancelled': 'dark'
  }
  return colorMap[status] || 'secondary'
}

onMounted(() => {
  fetchDashboardData()
})
</script>