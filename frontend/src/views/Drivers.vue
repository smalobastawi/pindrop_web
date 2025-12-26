<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Drivers</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
      <div class="btn-group me-2">
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="exportDrivers">
          Export
        </button>
      </div>
      <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addDriverModal">
        Add Driver
      </button>
    </div>
  </div>

  <div class="row mb-3">
    <div class="col-md-4">
      <input v-model="searchQuery" type="text" class="form-control" placeholder="Search drivers..." />
    </div>
    <div class="col-md-3">
      <select v-model="statusFilter" class="form-select">
        <option value="">All Status</option>
        <option value="available">Available</option>
        <option value="busy">Busy</option>
        <option value="offline">Offline</option>
      </select>
    </div>
  </div>

  <div class="row">
    <div class="col-md-3 mb-3" v-for="driver in filteredDrivers" :key="driver.id">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <h5 class="card-title">{{ driver.name }}</h5>
            <span class="badge" :class="getAvailabilityClass(driver.is_available)">
              {{ driver.is_available ? 'Available' : 'Busy' }}
            </span>
          </div>
          
          <div class="mb-2">
            <small class="text-muted">
              📞 {{ driver.phone }}
            </small>
          </div>
          
          <div class="mb-2">
            <small class="text-muted">
              📧 {{ driver.email }}
            </small>
          </div>
          
          <div class="mb-2">
            <small class="text-muted">
              🚚 {{ driver.vehicle_type }} - {{ driver.vehicle_plate }}
            </small>
          </div>
          
          <div class="mb-2">
            <small class="text-muted">
              🆔 License: {{ driver.license_number }}
            </small>
          </div>
          
          <hr>
          
          <div class="row text-center">
            <div class="col-6">
              <strong class="text-primary">{{ driver.total_deliveries }}</strong>
              <br>
              <small class="text-muted">Deliveries</small>
            </div>
            <div class="col-6">
              <strong class="text-success">{{ driver.rating }}/5</strong>
              <br>
              <small class="text-muted">Rating</small>
            </div>
          </div>
          
          <div v-if="driver.current_location" class="mt-2">
            <small class="text-muted">
              📍 {{ driver.current_location }}
            </small>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="btn-group w-100">
            <button class="btn btn-sm btn-outline-primary" @click="viewDriver(driver.id)">
              View
            </button>
            <button class="btn btn-sm btn-outline-secondary" @click="editDriver(driver.id)">
              Edit
            </button>
            <button class="btn btn-sm" :class="driver.is_available ? 'btn-outline-warning' : 'btn-outline-success'" 
                    @click="toggleAvailability(driver.id)">
              {{ driver.is_available ? 'Mark Busy' : 'Mark Available' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="filteredDrivers.length === 0" class="text-center py-5">
    <h4 class="text-muted">No drivers found</h4>
  </div>

  <!-- Driver Detail Modal -->
  <div class="modal fade" id="driverModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Driver Details</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body" v-if="selectedDriver">
          <div class="row">
            <div class="col-md-6">
              <h6>Personal Information</h6>
              <p><strong>Name:</strong> {{ selectedDriver.name }}</p>
              <p><strong>Email:</strong> {{ selectedDriver.email }}</p>
              <p><strong>Phone:</strong> {{ selectedDriver.phone }}</p>
              <p><strong>License Number:</strong> {{ selectedDriver.license_number }}</p>
            </div>
            <div class="col-md-6">
              <h6>Vehicle Information</h6>
              <p><strong>Vehicle Type:</strong> {{ selectedDriver.vehicle_type }}</p>
              <p><strong>License Plate:</strong> {{ selectedDriver.vehicle_plate }}</p>
              <p><strong>Status:</strong> 
                <span class="badge" :class="getAvailabilityClass(selectedDriver.is_available)">
                  {{ selectedDriver.is_available ? 'Available' : 'Busy' }}
                </span>
              </p>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6">
              <h6>Statistics</h6>
              <p><strong>Total Deliveries:</strong> {{ selectedDriver.total_deliveries }}</p>
              <p><strong>Completed Today:</strong> {{ selectedDriver.completed_today }}</p>
              <p><strong>Rating:</strong> {{ selectedDriver.rating }}/5</p>
            </div>
            <div class="col-md-6">
              <h6>Performance</h6>
              <p><strong>On-time Rate:</strong> {{ selectedDriver.on_time_rate }}%</p>
              <p><strong>Customer Rating:</strong> {{ selectedDriver.customer_rating }}/5</p>
              <p><strong>Total Earnings:</strong> {{ formatCurrency(selectedDriver.total_earnings) }}</p>
            </div>
          </div>
          
          <div v-if="selectedDriver.current_location">
            <h6>Current Location</h6>
            <p>{{ selectedDriver.current_location }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Driver Modal -->
  <div class="modal fade" id="addDriverModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add New Driver</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addDriver">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="newDriver.name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="newDriver.email" type="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Phone</label>
              <input v-model="newDriver.phone" type="tel" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">License Number</label>
              <input v-model="newDriver.license_number" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Vehicle Type</label>
              <input v-model="newDriver.vehicle_type" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">License Plate</label>
              <input v-model="newDriver.vehicle_plate" type="text" class="form-control" required />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="addDriver" data-bs-dismiss="modal">
            Add Driver
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
const selectedDriver = ref(null)

const drivers = ref([
  {
    id: 1,
    name: 'Mike Johnson',
    email: 'mike@example.com',
    phone: '+254723456789',
    license_number: 'DL123456789',
    vehicle_type: 'Motorcycle',
    vehicle_plate: 'KBA 123A',
    is_available: true,
    current_location: 'Westlands, Nairobi',
    total_deliveries: 156,
    completed_today: 8,
    rating: 4.8,
    customer_rating: 4.9,
    on_time_rate: 95,
    total_earnings: 12500.00
  },
  {
    id: 2,
    name: 'Sarah Wilson',
    email: 'sarah@example.com',
    phone: '+254734567890',
    license_number: 'DL987654321',
    vehicle_type: 'Van',
    vehicle_plate: 'KBB 456B',
    is_available: false,
    current_location: 'CBD, Nairobi',
    total_deliveries: 89,
    completed_today: 5,
    rating: 4.6,
    customer_rating: 4.7,
    on_time_rate: 92,
    total_earnings: 8900.00
  },
  {
    id: 3,
    name: 'David Brown',
    email: 'david@example.com',
    phone: '+254745678901',
    license_number: 'DL456789123',
    vehicle_type: 'Bicycle',
    vehicle_plate: 'KBC 789C',
    is_available: true,
    current_location: 'Eastlands, Nairobi',
    total_deliveries: 203,
    completed_today: 12,
    rating: 4.9,
    customer_rating: 4.8,
    on_time_rate: 97,
    total_earnings: 6800.00
  }
])

const newDriver = ref({
  name: '',
  email: '',
  phone: '',
  license_number: '',
  vehicle_type: '',
  vehicle_plate: ''
})

const filteredDrivers = computed(() => {
  let filtered = drivers.value

  if (searchQuery.value) {
    filtered = filtered.filter(driver => 
      driver.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      driver.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      driver.phone.includes(searchQuery.value) ||
      driver.vehicle_plate.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (statusFilter.value) {
    if (statusFilter.value === 'available') {
      filtered = filtered.filter(driver => driver.is_available)
    } else if (statusFilter.value === 'busy') {
      filtered = filtered.filter(driver => !driver.is_available)
    }
  }

  return filtered
})

const getAvailabilityClass = (isAvailable) => {
  return isAvailable ? 'bg-success' : 'bg-warning'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: import.meta.env.VITE_CURRENCY || 'KES'
  }).format(amount)
}

const viewDriver = (driverId) => {
  selectedDriver.value = drivers.value.find(d => d.id === driverId)
  // In a real app, you would use Bootstrap's modal or similar
  alert(`Viewing driver: ${selectedDriver.value.name}`)
}

const editDriver = (driverId) => {
  alert(`Editing driver: ${driverId}`)
}

const toggleAvailability = (driverId) => {
  const driver = drivers.value.find(d => d.id === driverId)
  if (driver) {
    driver.is_available = !driver.is_available
    alert(`Driver ${driver.name} is now ${driver.is_available ? 'available' : 'busy'}`)
  }
}

const addDriver = () => {
  const driver = {
    id: drivers.value.length + 1,
    ...newDriver.value,
    is_available: true,
    current_location: '',
    total_deliveries: 0,
    completed_today: 0,
    rating: 5.0,
    customer_rating: 5.0,
    on_time_rate: 100,
    total_earnings: 0
  }
  
  drivers.value.unshift(driver)
  newDriver.value = {
    name: '',
    email: '',
    phone: '',
    license_number: '',
    vehicle_type: '',
    vehicle_plate: ''
  }
  alert('Driver added successfully!')
}

const exportDrivers = () => {
  alert('Exporting drivers to CSV...')
}

onMounted(() => {
  console.log('Loading drivers...')
})
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
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

.card-title {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.text-primary {
  font-size: 1.2rem;
}

.text-success {
  font-size: 1.2rem;
}
</style>