<!-- frontend/src/views/CustomerPortal.vue -->
<template>
  <div class="customer-portal">
    <div class="row">
      <!-- Sidebar -->
      <nav class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item">
              <a href="#" @click="handleNewOrder" class="nav-link active">
                ➕ New Order
              </a>
            </li>
            <li class="nav-item">
              <a href="#" @click="handleTrackOrder" class="nav-link">
                🔍 Track Order
              </a>
            </li>
            <li class="nav-item">
              <a href="#" @click="handlePayments" class="nav-link">
                💳 Payments
              </a>
            </li>
            <li class="nav-item">
              <a href="#" @click="handleSupportTickets" class="nav-link">
                🎫 Support Tickets
              </a>
            </li>
            <li class="nav-item">
              <a href="#" @click="handleTermsOfService" class="nav-link">
                📄 Terms of Service
              </a>
            </li>
          </ul>
        </div>
      </nav>

      <!-- Main Content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="container-fluid">
          <!-- Header -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="d-flex justify-content-between align-items-center">
                <h2>Customer Portal</h2>
                <div>
                  <span class="me-3">Welcome, {{ customerData?.name || 'Customer' }}</span>
                  <button @click="handleLogout" class="btn btn-outline-danger btn-sm">
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>

      <!-- Statistics Cards -->
      <div class="row mb-4" v-if="portalData">
        <div class="col-md-3">
          <div class="card text-white bg-primary">
            <div class="card-body">
              <h5 class="card-title">Total Orders</h5>
              <p class="card-text display-6">{{ portalData.stats.total_orders || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-warning">
            <div class="card-body">
              <h5 class="card-title">Pending Orders</h5>
              <p class="card-text display-6">{{ portalData.stats.pending_orders || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-success">
            <div class="card-body">
              <h5 class="card-title">Completed Orders</h5>
              <p class="card-text display-6">{{ portalData.stats.completed_orders || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-info">
            <div class="card-body">
              <h5 class="card-title">Total Spent</h5>
              <p class="card-text display-6">${{ portalData.stats.total_spent || 0 }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <button @click="showCreateOrder = true" class="btn btn-primary me-3">
            <i class="bi bi-plus-circle"></i> Create New Order
          </button>
          <button @click="showTrackingModal = true" class="btn btn-outline-primary">
            <i class="bi bi-search"></i> Track Order
          </button>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">My Orders</h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center">
                <div class="spinner-border"></div>
              </div>
              
              <div v-else-if="!portalData || !portalData.orders || portalData.orders.length === 0" class="text-center">
                <p>No orders found. Create your first order to get started!</p>
              </div>
              
              <div v-else>
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Tracking Number</th>
                        <th>Package</th>
                        <th>Destination</th>
                        <th>Status</th>
                        <th>Delivery Fee</th>
                        <th>Payment</th>
                        <th>Created</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in portalData.orders" :key="order.id">
                        <td>
                          <strong>{{ order.tracking_number }}</strong>
                        </td>
                        <td>{{ order.package?.description?.substring(0, 30) }}...</td>
                        <td>{{ order.delivery_address?.substring(0, 40) }}...</td>
                        <td>
                          <span :class="`badge bg-${getStatusColor(order.status)}`">
                            {{ order.status.replace('_', ' ').toUpperCase() }}
                          </span>
                        </td>
                        <td>${{ order.delivery_fee }}</td>
                        <td>
                          <span v-if="order.payment" :class="`badge bg-${getPaymentStatusColor(order.payment.status)}`">
                            {{ order.payment.status.toUpperCase() }}
                          </span>
                          <span v-else class="badge bg-secondary">No Payment</span>
                        </td>
                        <td>{{ formatDate(order.created_at) }}</td>
                        <td>
                          <button 
                            @click="trackOrder(order.tracking_number)"
                            class="btn btn-sm btn-outline-primary"
                          >
                            Track
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div> <!-- close container-fluid -->
    </main>
  </div> <!-- close row -->

  <!-- Create Order Modal -->
    <div class="modal fade" :class="{ show: showCreateOrder }" style="display: block;" v-if="showCreateOrder">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Order</h5>
            <button type="button" class="btn-close" @click="showCreateOrder = false"></button>
          </div>
          <div class="modal-body">
            <CreateOrderForm @order-created="handleOrderCreated" @cancel="showCreateOrder = false" />
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateOrder"></div>

    <!-- Tracking Modal -->
    <div class="modal fade" :class="{ show: showTrackingModal }" style="display: block;" v-if="showTrackingModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Track Order</h5>
            <button type="button" class="btn-close" @click="showTrackingModal = false"></button>
          </div>
          <div class="modal-body">
            <TrackOrder @close="showTrackingModal = false" />
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showTrackingModal"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'
import CreateOrderForm from '@/components/CreateOrderForm.vue'
import TrackOrder from '@/components/TrackOrder.vue'

const router = useRouter()
const loading = ref(false)
const portalData = ref(null)
const customerData = ref(null)
const showCreateOrder = ref(false)
const showTrackingModal = ref(false)

const loadPortalData = async () => {
  loading.value = true
  try {
    const response = await customerAPI.getPortal()
    portalData.value = response.data
    customerData.value = response.data.customer
  } catch (error) {
    toast.error('Failed to load portal data')
    if (error.response?.status === 401) {
      router.push('/customer-login')
    }
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  toast.success('Logged out successfully')
  router.push('/customer-portal/login')
}

const handleOrderCreated = () => {
  showCreateOrder.value = false
  loadPortalData()
  toast.success('Order created successfully!')
}

const trackOrder = (trackingNumber) => {
  showTrackingModal.value = true
}

const handleNewOrder = () => {
  showCreateOrder.value = true
}

const handleTrackOrder = () => {
  showTrackingModal.value = true
}

const handlePayments = () => {
  toast.info('Payments feature coming soon!')
}

const handleSupportTickets = () => {
  toast.info('Support tickets feature coming soon!')
}

const handleTermsOfService = () => {
  toast.info('Terms of service will be displayed here!')
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
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadPortalData()
})
</script>

<style scoped>
.customer-portal {
  padding: 20px;
}

.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 48px 0 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.1);
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
  padding: 0.5rem 1rem;
}

.sidebar .nav-link:hover {
  color: #007bff;
}

.sidebar .nav-link.active {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  border-right: 3px solid #007bff;
}

.card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.modal.show {
  display: block !important;
}
</style>