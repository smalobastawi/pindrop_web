<template>
  <AdminLayout>
    <div class="admin-drivers">
      <div class="page-header">
        <h1>Driver Management</h1>
        <p>Manage delivery drivers and riders</p>
      </div>

      <!-- Filters and Actions -->
      <div class="filters-section">
        <div class="filters">
          <select v-model="filters.status" @change="fetchDrivers">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="pending_approval">Pending Approval</option>
            <option value="suspended">Suspended</option>
          </select>

          <select v-model="filters.vehicle_type" @change="fetchDrivers">
            <option value="">All Vehicle Types</option>
            <option value="bicycle">Bicycle</option>
            <option value="motorcycle">Motorcycle</option>
            <option value="car">Car</option>
            <option value="van">Van</option>
            <option value="truck">Truck</option>
          </select>

          <input
            type="text"
            v-model="filters.search"
            placeholder="Search by name, email, or phone..."
            @input="debounceSearch"
          />
        </div>

        <div class="actions">
          <button class="btn btn-primary" @click="showAddDriverModal = true">
            <i class="icon-plus"></i> Add Driver
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading drivers...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="icon-error"></i>
        <p>{{ error }}</p>
        <button class="btn btn-secondary" @click="fetchDrivers">Retry</button>
      </div>

      <!-- Drivers Table -->
      <div v-else class="drivers-table-container">
        <table class="drivers-table">
          <thead>
            <tr>
              <th>Driver</th>
              <th>Contact</th>
              <th>Vehicle</th>
              <th>Status</th>
              <th>Rating</th>
              <th>Deliveries</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="driver in drivers" :key="driver.id">
              <td class="driver-info">
                <div class="driver-avatar">
                  <img v-if="driver.profile_image" :src="driver.profile_image" :alt="driver.full_name" />
                  <div v-else class="avatar-placeholder">
                    {{ driver.full_name ? driver.full_name.charAt(0).toUpperCase() : 'D' }}
                  </div>
                </div>
                <div class="driver-details">
                  <div class="driver-name">{{ driver.full_name || driver.user_details?.username }}</div>
                  <div class="driver-id">ID: {{ driver.id }}</div>
                </div>
              </td>

              <td class="contact-info">
                <div class="contact-email">{{ driver.email }}</div>
                <div class="contact-phone">{{ driver.phone }}</div>
              </td>

              <td class="vehicle-info">
                <div class="vehicle-type">{{ driver.vehicle_type_display }}</div>
                <div class="vehicle-plate">{{ driver.vehicle_plate }}</div>
                <div class="vehicle-model" v-if="driver.vehicle_model">{{ driver.vehicle_model }}</div>
              </td>

              <td class="status-info">
                <span :class="`status-badge status-${driver.status}`">
                  {{ driver.status_display }}
                </span>
                <div class="availability" v-if="driver.status === 'active'">
                  <span :class="`availability-badge ${driver.is_available ? 'available' : 'unavailable'}`">
                    {{ driver.is_available ? 'Available' : 'Unavailable' }}
                  </span>
                </div>
              </td>

              <td class="rating-info">
                <div class="rating">
                  <span class="rating-stars">
                    <i v-for="star in 5" :key="star" :class="star <= Math.floor(driver.rating) ? 'icon-star-full' : star <= driver.rating ? 'icon-star-half' : 'icon-star-empty'"></i>
                  </span>
                  <span class="rating-value">{{ driver.rating.toFixed(1) }}</span>
                </div>
                <div class="rating-count">({{ driver.total_ratings }} reviews)</div>
              </td>

              <td class="deliveries-info">
                <div class="completed-deliveries">{{ driver.completed_deliveries }}</div>
                <div class="success-rate" v-if="driver.completed_deliveries > 0">
                  {{ ((driver.completed_deliveries / (driver.completed_deliveries + (driver.assigned_deliveries || 0))) * 100).toFixed(1) }}% success
                </div>
              </td>

              <td class="actions">
                <div class="action-buttons">
                  <button class="btn btn-sm btn-outline" @click="viewDriver(driver)" title="View Details">
                    <i class="icon-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-outline" @click="editDriver(driver)" title="Edit Driver">
                    <i class="icon-edit"></i>
                  </button>
                  <button
                    v-if="driver.status === 'pending_approval'"
                    class="btn btn-sm btn-success"
                    @click="approveDriver(driver)"
                    title="Approve Driver"
                  >
                    <i class="icon-check"></i>
                  </button>
                  <button
                    v-if="driver.status === 'active'"
                    class="btn btn-sm btn-warning"
                    @click="toggleDriverStatus(driver)"
                    title="Deactivate Driver"
                  >
                    <i class="icon-pause"></i>
                  </button>
                  <button
                    v-else-if="driver.status === 'inactive'"
                    class="btn btn-sm btn-success"
                    @click="toggleDriverStatus(driver)"
                    title="Activate Driver"
                  >
                    <i class="icon-play"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="drivers.length === 0" class="empty-state">
          <i class="icon-truck"></i>
          <h3>No drivers found</h3>
          <p>No drivers match your current filters.</p>
          <button class="btn btn-primary" @click="clearFilters">Clear Filters</button>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="drivers.length > 0" class="pagination">
        <button
          class="btn btn-outline"
          :disabled="!pagination.previous"
          @click="goToPage(pagination.previous)"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ pagination.current_page }} of {{ pagination.total_pages }}
        </span>
        <button
          class="btn btn-outline"
          :disabled="!pagination.next"
          @click="goToPage(pagination.next)"
        >
          Next
        </button>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'
import axios from 'axios'
import { useAdminAuthStore } from '@/stores/adminAuth'

export default {
  name: 'AdminDrivers',
  components: {
    AdminLayout
  },
  data() {
    return {
      drivers: [],
      loading: false,
      error: null,
      filters: {
        status: '',
        vehicle_type: '',
        search: ''
      },
      pagination: {
        current_page: 1,
        total_pages: 1,
        next: null,
        previous: null,
        count: 0
      },
      showAddDriverModal: false,
      searchTimeout: null
    }
  },
  computed: {
    adminAuth() {
      return useAdminAuthStore()
    }
  },
  mounted() {
    this.fetchDrivers()
  },
  methods: {
    async fetchDrivers(page = 1) {
      this.loading = true
      this.error = null

      try {
        const params = {
          page: page,
          page_size: 20
        }

        // Add filters
        if (this.filters.status) params.status = this.filters.status
        if (this.filters.vehicle_type) params.vehicle_type = this.filters.vehicle_type
        if (this.filters.search) params.search = this.filters.search

        const response = await axios.get('/admin-api/api/riders/', { params })
        this.drivers = response.data.results || response.data
        this.updatePagination(response.data)
      } catch (error) {
        console.error('Error fetching drivers:', error)
        this.error = error.response?.data?.message || 'Failed to load drivers'
      } finally {
        this.loading = false
      }
    },

    updatePagination(data) {
      if (data.next || data.previous) {
        // Django REST framework pagination
        this.pagination = {
          current_page: Math.ceil((data.offset || 0) / (data.limit || 20)) + 1,
          total_pages: Math.ceil(data.count / (data.limit || 20)),
          next: data.next,
          previous: data.previous,
          count: data.count
        }
      } else {
        // Simple pagination
        this.pagination = {
          current_page: 1,
          total_pages: 1,
          next: null,
          previous: null,
          count: this.drivers.length
        }
      }
    },

    goToPage(url) {
      if (!url) return

      const urlObj = new URL(url)
      const page = urlObj.searchParams.get('page')
      this.fetchDrivers(parseInt(page))
    },

    debounceSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.fetchDrivers()
      }, 500)
    },

    clearFilters() {
      this.filters = {
        status: '',
        vehicle_type: '',
        search: ''
      }
      this.fetchDrivers()
    },

    viewDriver(driver) {
      // TODO: Implement view driver details
      console.log('View driver:', driver)
    },

    editDriver(driver) {
      // TODO: Implement edit driver
      console.log('Edit driver:', driver)
    },

    async approveDriver(driver) {
      if (!confirm(`Are you sure you want to approve ${driver.full_name}?`)) return

      try {
        await axios.post(`/admin-api/api/riders/${driver.id}/approve_rider/`)
        this.fetchDrivers() // Refresh the list
      } catch (error) {
        console.error('Error approving driver:', error)
        alert('Failed to approve driver')
      }
    },

    async toggleDriverStatus(driver) {
      const action = driver.status === 'active' ? 'deactivate' : 'activate'
      if (!confirm(`Are you sure you want to ${action} ${driver.full_name}?`)) return

      try {
        const newStatus = driver.status === 'active' ? 'inactive' : 'active'
        await axios.patch(`/admin-api/api/riders/${driver.id}/`, { status: newStatus })
        this.fetchDrivers() // Refresh the list
      } catch (error) {
        console.error('Error updating driver status:', error)
        alert('Failed to update driver status')
      }
    }
  }
}
</script>

<style scoped>
.admin-drivers {
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

/* Filters Section */
.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filters select,
.filters input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 0.9rem;
}

.filters input {
  min-width: 250px;
}

.actions .btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Loading and Error States */
.loading,
.error-message {
  background: white;
  padding: 3rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message i {
  font-size: 3rem;
  color: #dc3545;
  margin-bottom: 1rem;
}

/* Drivers Table */
.drivers-table-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.drivers-table {
  width: 100%;
  border-collapse: collapse;
}

.drivers-table th,
.drivers-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.drivers-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.drivers-table tbody tr:hover {
  background: #f8f9fa;
}

/* Driver Info */
.driver-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.driver-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.driver-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.driver-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.driver-id {
  font-size: 0.8rem;
  color: #6c757d;
}

/* Contact Info */
.contact-email {
  font-size: 0.9rem;
  color: #495057;
  margin-bottom: 0.25rem;
}

.contact-phone {
  font-size: 0.9rem;
  color: #6c757d;
}

/* Vehicle Info */
.vehicle-type {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.vehicle-plate {
  font-size: 0.9rem;
  color: #495057;
  margin-bottom: 0.25rem;
}

.vehicle-model {
  font-size: 0.8rem;
  color: #6c757d;
}

/* Status Info */
.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.status-pending_approval {
  background: #fff3cd;
  color: #856404;
}

.status-suspended {
  background: #f8d7da;
  color: #721c24;
}

.availability-badge {
  display: inline-block;
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
  font-size: 0.7rem;
  font-weight: 600;
  margin-top: 0.25rem;
}

.availability-badge.available {
  background: #d4edda;
  color: #155724;
}

.availability-badge.unavailable {
  background: #f8d7da;
  color: #721c24;
}

/* Rating Info */
.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.rating-stars {
  color: #ffc107;
}

.rating-stars i {
  font-size: 0.9rem;
}

.rating-value {
  font-weight: 600;
  color: #2c3e50;
}

.rating-count {
  font-size: 0.8rem;
  color: #6c757d;
}

/* Deliveries Info */
.completed-deliveries {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.success-rate {
  font-size: 0.8rem;
  color: #28a745;
}

/* Actions */
.actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: #dee2e6;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: #495057;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.page-info {
  font-size: 0.9rem;
  color: #6c757d;
}

/* Button Styles */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-outline {
  background: transparent;
  border: 1px solid #dee2e6;
  color: #495057;
}

.btn-outline:hover {
  background: #f8f9fa;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #1e7e34;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filters {
    flex-wrap: wrap;
  }

  .drivers-table {
    font-size: 0.8rem;
  }

  .drivers-table th,
  .drivers-table td {
    padding: 0.5rem;
  }

  .driver-info {
    flex-direction: column;
    text-align: center;
  }
}
</style>