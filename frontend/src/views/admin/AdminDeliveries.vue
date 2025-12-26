<template>
  <AdminLayout>
    <div class="admin-deliveries">
      <div class="page-header">
        <h1>Delivery Management</h1>
        <p>Manage all delivery orders and track shipments</p>
        <router-link to="/admin/deliveries/new" class="btn btn-primary">
          <i class="fas fa-plus"></i> Create New Delivery
        </router-link>
      </div>

      <!-- Filters and Search -->
      <div class="filters-section">
        <div class="filters-row">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by tracking number, sender, or recipient..."
              @input="debouncedSearch"
            >
          </div>

          <div class="filter-group">
            <select v-model="statusFilter" @change="fetchDeliveries">
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="assigned">Assigned</option>
              <option value="picked_up">Picked Up</option>
              <option value="in_transit">In Transit</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>

            <select v-model="priorityFilter" @change="fetchDeliveries">
              <option value="">All Priorities</option>
              <option value="1">Normal</option>
              <option value="2">Express</option>
              <option value="3">Urgent</option>
              <option value="4">Same Day</option>
            </select>

            <button @click="resetFilters" class="btn btn-secondary">
              <i class="fas fa-times"></i> Reset
            </button>
          </div>
        </div>
      </div>

      <!-- Deliveries Table -->
      <div class="deliveries-table-container">
        <div v-if="loading" class="loading-spinner">
          <i class="fas fa-spinner fa-spin"></i> Loading deliveries...
        </div>

        <div v-else-if="error" class="error-message">
          <i class="fas fa-exclamation-triangle"></i>
          {{ error }}
          <button @click="fetchDeliveries" class="btn btn-primary">Retry</button>
        </div>

        <table v-else-if="deliveries.length > 0" class="deliveries-table">
          <thead>
            <tr>
              <th>Tracking #</th>
              <th>Sender</th>
              <th>Recipient</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Rider</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="delivery in deliveries" :key="delivery.id" :class="getStatusClass(delivery.status)">
              <td>
                <strong>{{ delivery.tracking_number }}</strong>
              </td>
              <td>
                <div class="user-info">
                  <div class="name">{{ delivery.sender_details?.name || 'N/A' }}</div>
                  <div class="phone">{{ delivery.sender_details?.phone || '' }}</div>
                </div>
              </td>
              <td>
                <div class="user-info">
                  <div class="name">{{ delivery.recipient_name }}</div>
                  <div class="phone">{{ delivery.recipient_phone }}</div>
                </div>
              </td>
              <td>
                <span :class="`status-badge status-${delivery.status}`">
                  {{ delivery.status_display }}
                </span>
              </td>
              <td>
                <span :class="`priority-badge priority-${delivery.priority}`">
                  {{ delivery.priority_display }}
                </span>
              </td>
              <td>
                <div v-if="delivery.rider_details" class="rider-info">
                  <div class="name">{{ delivery.rider_details.name }}</div>
                  <div class="vehicle">{{ delivery.rider_details.vehicle_type }} - {{ delivery.rider_details.vehicle_plate }}</div>
                </div>
                <span v-else class="no-rider">Unassigned</span>
              </td>
              <td>
                {{ formatDate(delivery.created_at) }}
              </td>
              <td>
                <div class="actions">
                  <button @click="viewDelivery(delivery)" class="btn btn-sm btn-info" title="View Details">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button
                    v-if="!delivery.rider_details && canManageDeliveries"
                    @click="showAssignRiderModal(delivery)"
                    class="btn btn-sm btn-warning"
                    title="Assign Rider"
                  >
                    <i class="fas fa-user-plus"></i>
                  </button>
                  <button
                    v-if="canManageDeliveries"
                    @click="showUpdateStatusModal(delivery)"
                    class="btn btn-sm btn-secondary"
                    title="Update Status"
                  >
                    <i class="fas fa-edit"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else class="no-deliveries">
          <i class="fas fa-inbox"></i>
          <h3>No deliveries found</h3>
          <p>Try adjusting your filters or create a new delivery.</p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="btn btn-secondary"
        >
          <i class="fas fa-chevron-left"></i> Previous
        </button>

        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="btn btn-secondary"
        >
          Next <i class="fas fa-chevron-right"></i>
        </button>
      </div>

      <!-- Assign Rider Modal -->
      <div v-if="showAssignModal" class="modal-overlay" @click="closeAssignModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Assign Rider to Delivery</h3>
            <button @click="closeAssignModal" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <p><strong>Delivery:</strong> {{ selectedDelivery?.tracking_number }}</p>
            <p><strong>From:</strong> {{ selectedDelivery?.pickup_address }}</p>
            <p><strong>To:</strong> {{ selectedDelivery?.delivery_address }}</p>

            <div class="rider-selection">
              <h4>Select Available Rider:</h4>
              <div v-if="availableRidersLoading" class="loading-spinner">
                <i class="fas fa-spinner fa-spin"></i> Loading riders...
              </div>
              <div v-else-if="availableRiders.length === 0" class="no-riders">
                No available riders found.
              </div>
              <div v-else class="riders-list">
                <div
                  v-for="rider in availableRiders"
                  :key="rider.id"
                  class="rider-option"
                  @click="selectRider(rider)"
                  :class="{ selected: selectedRider?.id === rider.id }"
                >
                  <div class="rider-name">{{ rider.name }}</div>
                  <div class="rider-details">
                    {{ rider.vehicle_type }} - {{ rider.vehicle_plate }}
                  </div>
                  <div class="rider-contact">{{ rider.phone }}</div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeAssignModal" class="btn btn-secondary">Cancel</button>
            <button
              @click="assignRider"
              :disabled="!selectedRider || assigning"
              class="btn btn-primary"
            >
              <i v-if="assigning" class="fas fa-spinner fa-spin"></i>
              {{ assigning ? 'Assigning...' : 'Assign Rider' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Update Status Modal -->
      <div v-if="showStatusModal" class="modal-overlay" @click="closeStatusModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Update Delivery Status</h3>
            <button @click="closeStatusModal" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <p><strong>Delivery:</strong> {{ selectedDelivery?.tracking_number }}</p>
            <p><strong>Current Status:</strong> {{ selectedDelivery?.status_display }}</p>

            <div class="form-group">
              <label for="newStatus">New Status:</label>
              <select id="newStatus" v-model="newStatus">
                <option value="pending">Pending</option>
                <option value="assigned">Assigned</option>
                <option value="picked_up">Picked Up</option>
                <option value="in_transit">In Transit</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div class="form-group">
              <label for="statusNotes">Notes (optional):</label>
              <textarea
                id="statusNotes"
                v-model="statusNotes"
                placeholder="Add any notes about this status change..."
                rows="3"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeStatusModal" class="btn btn-secondary">Cancel</button>
            <button
              @click="updateStatus"
              :disabled="!newStatus || updating"
              class="btn btn-primary"
            >
              <i v-if="updating" class="fas fa-spinner fa-spin"></i>
              {{ updating ? 'Updating...' : 'Update Status' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'
import { useAdminAuthStore } from '@/stores/adminAuth'
import axios from 'axios'
import debounce from 'lodash/debounce'

export default {
  name: 'AdminDeliveries',
  components: {
    AdminLayout
  },
  data() {
    return {
      deliveries: [],
      loading: false,
      error: null,
      searchQuery: '',
      statusFilter: '',
      priorityFilter: '',
      currentPage: 1,
      totalPages: 1,
      pageSize: 20,

      // Modal states
      showAssignModal: false,
      showStatusModal: false,
      selectedDelivery: null,
      availableRiders: [],
      availableRidersLoading: false,
      selectedRider: null,
      assigning: false,
      newStatus: '',
      statusNotes: '',
      updating: false
    }
  },
  computed: {
    canManageDeliveries() {
      const authStore = useAdminAuthStore()
      return authStore.canManageDeliveries
    }
  },
  mounted() {
    this.debouncedSearch = debounce(this.fetchDeliveries, 500)
    this.fetchDeliveries()
  },
  methods: {
    async fetchDeliveries() {
      this.loading = true
      this.error = null

      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize
        }

        if (this.searchQuery) {
          params.search = this.searchQuery
        }

        if (this.statusFilter) {
          params.status = this.statusFilter
        }

        if (this.priorityFilter) {
          params.priority = this.priorityFilter
        }

        const response = await axios.get('/admin-api/api/deliveries/', { params })
        this.deliveries = response.data.results || response.data
        this.totalPages = Math.ceil((response.data.count || this.deliveries.length) / this.pageSize)
      } catch (error) {
        console.error('Error fetching deliveries:', error)
        this.error = 'Failed to load deliveries. Please try again.'
      } finally {
        this.loading = false
      }
    },

    resetFilters() {
      this.searchQuery = ''
      this.statusFilter = ''
      this.priorityFilter = ''
      this.currentPage = 1
      this.fetchDeliveries()
    },

    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.fetchDeliveries()
      }
    },

    getStatusClass(status) {
      return `status-${status}`
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },

    viewDelivery(delivery) {
      // Navigate to delivery detail view
      this.$router.push(`/admin/deliveries/${delivery.id}`)
    },

    async showAssignRiderModal(delivery) {
      this.selectedDelivery = delivery
      this.selectedRider = null
      this.showAssignModal = true
      await this.fetchAvailableRiders()
    },

    closeAssignModal() {
      this.showAssignModal = false
      this.selectedDelivery = null
      this.selectedRider = null
      this.availableRiders = []
    },

    async fetchAvailableRiders() {
      this.availableRidersLoading = true
      try {
        const response = await axios.get('/admin-api/api/riders/active_riders/')
        this.availableRiders = response.data.riders || []
      } catch (error) {
        console.error('Error fetching available riders:', error)
        this.availableRiders = []
      } finally {
        this.availableRidersLoading = false
      }
    },

    selectRider(rider) {
      this.selectedRider = rider
    },

    async assignRider() {
      if (!this.selectedRider || !this.selectedDelivery) return

      this.assigning = true
      try {
        await axios.post(`/admin-api/api/deliveries/${this.selectedDelivery.id}/assign_rider/`, {
          rider_id: this.selectedRider.id
        })

        // Refresh deliveries list
        await this.fetchDeliveries()
        this.closeAssignModal()

        // Show success message (you might want to add a toast notification system)
        alert('Rider assigned successfully!')
      } catch (error) {
        console.error('Error assigning rider:', error)
        alert('Failed to assign rider. Please try again.')
      } finally {
        this.assigning = false
      }
    },

    showUpdateStatusModal(delivery) {
      this.selectedDelivery = delivery
      this.newStatus = delivery.status
      this.statusNotes = ''
      this.showStatusModal = true
    },

    closeStatusModal() {
      this.showStatusModal = false
      this.selectedDelivery = null
      this.newStatus = ''
      this.statusNotes = ''
    },

    async updateStatus() {
      if (!this.newStatus || !this.selectedDelivery) return

      this.updating = true
      try {
        await axios.post(`/admin-api/api/deliveries/${this.selectedDelivery.id}/update_status/`, {
          status: this.newStatus,
          notes: this.statusNotes
        })

        // Refresh deliveries list
        await this.fetchDeliveries()
        this.closeStatusModal()

        // Show success message
        alert('Delivery status updated successfully!')
      } catch (error) {
        console.error('Error updating status:', error)
        alert('Failed to update status. Please try again.')
      } finally {
        this.updating = false
      }
    }
  }
}
</script>

<style scoped>
.admin-deliveries {
  padding: 0;
}

.page-header {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 0;
}

/* Filters Section */
.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-box i {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  font-size: 0.9rem;
}

.search-box input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.filter-group select {
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  min-width: 120px;
}

.filter-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Table Styles */
.deliveries-table-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.deliveries-table {
  width: 100%;
  border-collapse: collapse;
}

.deliveries-table th,
.deliveries-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.deliveries-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.deliveries-table tbody tr:hover {
  background-color: #f8f9fa;
}

.deliveries-table tbody tr.status-delivered {
  background-color: #d4edda;
}

.deliveries-table tbody tr.status-cancelled {
  background-color: #f8d7da;
}

/* Status and Priority Badges */
.status-badge,
.priority-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.status-pending { background-color: #fff3cd; color: #856404; }
.status-badge.status-assigned { background-color: #cce5ff; color: #004085; }
.status-badge.status-picked_up { background-color: #d1ecf1; color: #0c5460; }
.status-badge.status-in_transit { background-color: #d4edda; color: #155724; }
.status-badge.status-delivered { background-color: #d4edda; color: #155724; }
.status-badge.status-cancelled { background-color: #f8d7da; color: #721c24; }

.priority-badge.priority-1 { background-color: #e9ecef; color: #495057; }
.priority-badge.priority-2 { background-color: #cce5ff; color: #004085; }
.priority-badge.priority-3 { background-color: #fff3cd; color: #856404; }
.priority-badge.priority-4 { background-color: #f8d7da; color: #721c24; }

/* User and Rider Info */
.user-info,
.rider-info {
  line-height: 1.4;
}

.user-info .name,
.rider-info .name {
  font-weight: 500;
  color: #495057;
}

.user-info .phone,
.rider-info .vehicle,
.rider-contact {
  font-size: 0.875rem;
  color: #6c757d;
}

.no-rider {
  color: #dc3545;
  font-style: italic;
}

/* Actions */
.actions {
  display: flex;
  gap: 0.25rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-info { background-color: #17a2b8; color: white; }
.btn-warning { background-color: #ffc107; color: #212529; }
.btn-secondary { background-color: #6c757d; color: white; }

.btn-sm:hover {
  opacity: 0.8;
}

/* Loading and Error States */
.loading-spinner,
.error-message {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.loading-spinner i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.error-message {
  color: #dc3545;
}

.error-message i {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}

/* No Deliveries State */
.no-deliveries {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.no-deliveries i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.no-deliveries h3 {
  margin-bottom: 0.5rem;
  color: #495057;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
}

.page-info {
  color: #6c757d;
  font-weight: 500;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #495057;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* Rider Selection */
.rider-selection h4 {
  margin-bottom: 1rem;
  color: #495057;
}

.riders-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
}

.rider-option {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  transition: background-color 0.2s;
}

.rider-option:hover,
.rider-option.selected {
  background-color: #f8f9fa;
}

.rider-option:last-child {
  border-bottom: none;
}

.rider-name {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.25rem;
}

.rider-details {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.no-riders {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

/* Form Styles */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  font-size: 0.9rem;
}

.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

/* Button Styles */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 768px) {
  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: auto;
  }

  .filter-group {
    justify-content: center;
  }

  .deliveries-table {
    font-size: 0.875rem;
  }

  .deliveries-table th,
  .deliveries-table td {
    padding: 0.5rem;
  }

  .actions {
    flex-direction: column;
    gap: 0.125rem;
  }

  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>