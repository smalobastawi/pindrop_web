<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Customers</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <div class="btn-group me-2">
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="exportCustomers">
          Export
        </button>
      </div>
      <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addCustomerModal">
        Add Customer
      </button>
    </div>
  </div>

  <div class="row mb-3">
    <div class="col-md-4">
      <input v-model="searchQuery" type="text" class="form-control" placeholder="Search customers..." />
    </div>
    <div class="col-md-3">
      <select v-model="statusFilter" class="form-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-striped table-sm">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Address</th>
          <th>Total Orders</th>
          <th>Joined</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in filteredCustomers" :key="customer.id">
          <td>{{ customer.id }}</td>
          <td>{{ customer.name }}</td>
          <td>{{ customer.email }}</td>
          <td>{{ customer.phone }}</td>
          <td>{{ customer.address.substring(0, 30) }}{{ customer.address.length > 30 ? '...' : '' }}</td>
          <td>
            <span class="badge bg-info">{{ customer.total_orders }}</span>
          </td>
          <td>{{ formatDate(customer.created_at) }}</td>
          <td>
            <div class="btn-group btn-group-sm">
              <button class="btn btn-outline-primary" @click="viewCustomer(customer.id)">
                View
              </button>
              <button class="btn btn-outline-secondary" @click="editCustomer(customer.id)">
                Edit
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="filteredCustomers.length === 0">
          <td colspan="8" class="text-center">No customers found</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Customer Detail Modal -->
  <div class="modal fade" id="customerModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Customer Details</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body" v-if="selectedCustomer">
          <div class="row">
            <div class="col-md-6">
              <h6>Personal Information</h6>
              <p><strong>Name:</strong> {{ selectedCustomer.name }}</p>
              <p><strong>Email:</strong> {{ selectedCustomer.email }}</p>
              <p><strong>Phone:</strong> {{ selectedCustomer.phone }}</p>
              <p><strong>Address:</strong> {{ selectedCustomer.address }}</p>
            </div>
            <div class="col-md-6">
              <h6>Statistics</h6>
              <p><strong>Total Orders:</strong> {{ selectedCustomer.total_orders }}</p>
              <p><strong>Total Spent:</strong> {{ formatCurrency(selectedCustomer.total_spent) }}</p>
              <p><strong>Joined:</strong> {{ formatDate(selectedCustomer.created_at) }}</p>
            </div>
          </div>
          
          <h6>Recent Orders</h6>
          <div class="table-responsive">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Tracking #</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in selectedCustomer.recent_orders" :key="order.id">
                  <td>{{ order.tracking_number }}</td>
                  <td>
                    <span class="badge" :class="getStatusClass(order.status)">
                      {{ order.status }}
                    </span>
                  </td>
                  <td>{{ formatDate(order.created_at) }}</td>
                  <td>{{ formatCurrency(order.amount) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Customer Modal -->
  <div class="modal fade" id="addCustomerModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add New Customer</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addCustomer">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="newCustomer.name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="newCustomer.email" type="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Phone</label>
              <input v-model="newCustomer.phone" type="tel" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Address</label>
              <textarea v-model="newCustomer.address" class="form-control" rows="3" required></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="addCustomer" data-bs-dismiss="modal">
            Add Customer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const searchQuery = ref('')
const statusFilter = ref('')
const selectedCustomer = ref(null)

const customers = ref([
  {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+254712345678',
    address: '123 Main Street, Westlands, Nairobi, Kenya',
    total_orders: 15,
    total_spent: 3750.00,
    created_at: '2024-01-15T10:00:00Z',
    recent_orders: [
      {
        id: 1,
        tracking_number: 'PKG123456789',
        status: 'delivered',
        created_at: '2025-12-10T14:30:00Z',
        amount: 250.00
      },
      {
        id: 2,
        tracking_number: 'PKG987654321',
        status: 'in_transit',
        created_at: '2025-12-12T09:15:00Z',
        amount: 180.00
      }
    ]
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane@example.com',
    phone: '+254798765432',
    address: '456 Uhuru Highway, CBD, Nairobi, Kenya',
    total_orders: 8,
    total_spent: 1200.00,
    created_at: '2024-03-22T15:30:00Z',
    recent_orders: []
  }
])

const newCustomer = ref({
  name: '',
  email: '',
  phone: '',
  address: ''
})

const filteredCustomers = computed(() => {
  let filtered = customers.value

  if (searchQuery.value) {
    filtered = filtered.filter(customer => 
      customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      customer.phone.includes(searchQuery.value)
    )
  }

  return filtered
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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: import.meta.env.VITE_CURRENCY || 'KES'
  }).format(amount)
}

const viewCustomer = (customerId) => {
  selectedCustomer.value = customers.value.find(c => c.id === customerId)
  // In a real app, you would use Bootstrap's modal or similar
  alert(`Viewing customer: ${selectedCustomer.value.name}`)
}

const editCustomer = (customerId) => {
  alert(`Editing customer: ${customerId}`)
}

const addCustomer = () => {
  const customer = {
    id: customers.value.length + 1,
    ...newCustomer.value,
    total_orders: 0,
    total_spent: 0,
    created_at: new Date().toISOString(),
    recent_orders: []
  }
  
  customers.value.unshift(customer)
  newCustomer.value = { name: '', email: '', phone: '', address: '' }
  alert('Customer added successfully!')
}

const exportCustomers = () => {
  alert('Exporting customers to CSV...')
}

onMounted(() => {
  console.log('Loading customers...')
})
</script>

<style scoped>
.table-responsive {
  margin-top: 1rem;
}

.badge {
  font-size: 0.75em;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.modal-lg {
  max-width: 800px;
}
</style>