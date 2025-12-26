<template>
  <AdminLayout>
    <div class="admin-customers">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <h1>Customer Management</h1>
            <p>Manage customer accounts and information</p>
          </div>
          <button 
            @click="showAddCustomerModal = true"
            class="btn btn-primary"
            :disabled="loading"
          >
            <i class="icon-user-plus"></i>
            Add Customer
          </button>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="filters-section">
        <div class="search-box">
          <i class="icon-search"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search customers..."
            @input="debouncedSearch"
          >
        </div>
        <div class="filter-controls">
          <select v-model="statusFilter" @change="applyFilters">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
          <select v-model="sortBy" @change="applyFilters">
            <option value="created_at">Sort by Date</option>
            <option value="name">Sort by Name</option>
            <option value="email">Sort by Email</option>
          </select>
        </div>
      </div>

      <!-- Customer Stats -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="icon-users"></i>
          </div>
          <div class="stat-content">
            <h3>{{ totalCustomers }}</h3>
            <p>Total Customers</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon active">
            <i class="icon-user-check"></i>
          </div>
          <div class="stat-content">
            <h3>{{ activeCustomers }}</h3>
            <p>Active Customers</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon new">
            <i class="icon-user-plus"></i>
          </div>
          <div class="stat-content">
            <h3>{{ newCustomersThisMonth }}</h3>
            <p>New This Month</p>
          </div>
        </div>
      </div>

      <!-- Customers Table -->
      <div class="table-container">
        <div class="table-header">
          <h3>Customers</h3>
          <div class="table-actions">
            <button 
              @click="exportCustomers"
              class="btn btn-secondary btn-sm"
              :disabled="loading || customers.length === 0"
            >
              <i class="icon-download"></i>
              Export
            </button>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>
                  <input 
                    type="checkbox" 
                    v-model="selectAll"
                    @change="toggleSelectAll"
                    :disabled="customers.length === 0"
                  >
                </th>
                <th>Customer</th>
                <th>Contact</th>
                <th>Address</th>
                <th>Status</th>
                <th>Orders</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="8" class="loading-row">
                  <div class="loading-spinner"></div>
                  Loading customers...
                </td>
              </tr>
              <tr v-else-if="customers.length === 0">
                <td colspan="8" class="empty-row">
                  <i class="icon-users"></i>
                  <p>No customers found</p>
                  <button 
                    @click="showAddCustomerModal = true"
                    class="btn btn-primary btn-sm"
                  >
                    Add First Customer
                  </button>
                </td>
              </tr>
              <tr v-for="customer in customers" :key="customer.id">
                <td>
                  <input 
                    type="checkbox" 
                    v-model="selectedCustomers"
                    :value="customer.id"
                  >
                </td>
                <td>
                  <div class="customer-info">
                    <div class="customer-avatar">
                      <i class="icon-user"></i>
                    </div>
                    <div>
                      <h4>{{ customer.full_name || customer.user_details?.username }}</h4>
                      <small>ID: {{ customer.id }}</small>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="contact-info">
                    <div>{{ customer.email }}</div>
                    <div>{{ customer.phone }}</div>
                  </div>
                </td>
                <td>
                  <div class="address-info">
                    {{ truncateText(customer.address, 50) }}
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', customer.status === 'active' ? 'active' : 'inactive']">
                    {{ customer.status_display }}
                  </span>
                </td>
                <td>
                  <span class="order-count">
                    {{ customer.deliveries_count || 0 }}
                  </span>
                </td>
                <td>
                  <div class="date-info">
                    {{ formatDate(customer.created_at) }}
                  </div>
                </td>
                <td>
                  <div class="action-buttons">
                    <button 
                      @click="viewCustomer(customer)"
                      class="btn-icon"
                      title="View Details"
                    >
                      <i class="icon-eye"></i>
                    </button>
                    <button 
                      @click="editCustomer(customer)"
                      class="btn-icon"
                      title="Edit Customer"
                    >
                      <i class="icon-edit"></i>
                    </button>
                    <button
                      @click="toggleCustomerStatus(customer)"
                      :class="['btn-icon', customer.status === 'active' ? 'text-warning' : 'text-success']"
                      :title="customer.status === 'active' ? 'Deactivate' : 'Activate'"
                    >
                      <i :class="customer.status === 'active' ? 'icon-pause' : 'icon-play'"></i>
                    </button>
                    <button 
                      @click="deleteCustomer(customer)"
                      class="btn-icon text-danger"
                      title="Delete Customer"
                    >
                      <i class="icon-trash-2"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="pagination-container" v-if="totalPages > 1">
          <div class="pagination-info">
            Showing {{ ((currentPage - 1) * pageSize) + 1 }} to 
            {{ Math.min(currentPage * pageSize, totalCustomers) }} of 
            {{ totalCustomers }} customers
          </div>
          <div class="pagination">
            <button 
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="page-btn"
            >
              <i class="icon-chevron-left"></i>
            </button>
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="changePage(page)"
              :class="['page-btn', { active: page === currentPage }]"
            >
              {{ page }}
            </button>
            <button 
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="page-btn"
            >
              <i class="icon-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Bulk Actions -->
      <div class="bulk-actions" v-if="selectedCustomers.length > 0">
        <div class="bulk-info">
          {{ selectedCustomers.length }} customer(s) selected
        </div>
        <div class="bulk-buttons">
          <button @click="bulkToggleStatus" class="btn btn-secondary btn-sm">
            <i class="icon-toggle-left"></i>
            Toggle Status
          </button>
          <button @click="bulkDelete" class="btn btn-danger btn-sm">
            <i class="icon-trash-2"></i>
            Delete Selected
          </button>
          <button @click="clearSelection" class="btn btn-secondary btn-sm">
            Clear Selection
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Customer Modal -->
    <CustomerModal
      v-if="showAddCustomerModal || editingCustomer"
      :customer="editingCustomer"
      @close="closeCustomerModal"
      @save="saveCustomer"
    />
  </AdminLayout>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import CustomerModal from '@/components/admin/CustomerModal.vue'
import axios from 'axios'
import debounce from 'lodash/debounce'

export default {
  name: 'AdminCustomers',
  components: {
    AdminLayout,
    CustomerModal
  },
  setup() {
    // Reactive state
    const customers = ref([])
    const loading = ref(false)
    const searchQuery = ref('')
    const statusFilter = ref('')
    const sortBy = ref('created_at')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalCustomers = ref(0)
    const selectedCustomers = ref([])
    const selectAll = ref(false)
    
    // Modal state
    const showAddCustomerModal = ref(false)
    const editingCustomer = ref(null)
    
    // Stats
    const activeCustomers = ref(0)
    const newCustomersThisMonth = ref(0)
    
    // Computed properties
    const totalPages = computed(() => Math.ceil(totalCustomers.value / pageSize.value))
    
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, currentPage.value + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    })
    
    // Methods
    const fetchCustomers = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value,
          status: statusFilter.value,
          sort_by: sortBy.value
        }
        
        const response = await axios.get('/admin-api/api/customers/', { params })
        customers.value = response.data.results || response.data
        totalCustomers.value = response.data.count || response.data.length
        
        // Calculate stats
        if (response.data.results) {
          activeCustomers.value = response.data.results.filter(c => c.status === 'active').length
          const thisMonth = new Date()
          thisMonth.setDate(1)
          thisMonth.setHours(0, 0, 0, 0)
          newCustomersThisMonth.value = response.data.results.filter(c =>
            new Date(c.created_at) >= thisMonth
          ).length
        }
        
      } catch (error) {
        console.error('Failed to fetch customers:', error)
        alert('Failed to load customers. Please try again.')
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = debounce(() => {
      currentPage.value = 1
      fetchCustomers()
    }, 500)
    
    const applyFilters = () => {
      currentPage.value = 1
      fetchCustomers()
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchCustomers()
      }
    }
    
    const toggleSelectAll = () => {
      if (selectAll.value) {
        selectedCustomers.value = customers.value.map(c => c.id)
      } else {
        selectedCustomers.value = []
      }
    }
    
    const clearSelection = () => {
      selectedCustomers.value = []
      selectAll.value = false
    }
    
    const viewCustomer = (customer) => {
      // Navigate to customer detail page
      console.log('View customer:', customer)
    }
    
    const editCustomer = (customer) => {
      editingCustomer.value = { ...customer }
      showAddCustomerModal.value = true
    }
    
    const closeCustomerModal = () => {
      showAddCustomerModal.value = false
      editingCustomer.value = null
    }
    
    const saveCustomer = async (customerData) => {
      try {
        if (editingCustomer.value) {
          await axios.put(`/admin-api/api/customers/${editingCustomer.value.id}/`, customerData)
        } else {
          await axios.post('/admin-api/api/customers/', customerData)
        }
        
        closeCustomerModal()
        fetchCustomers()
      } catch (error) {
        console.error('Failed to save customer:', error)
        alert('Failed to save customer. Please try again.')
      }
    }
    
    const toggleCustomerStatus = async (customer) => {
      try {
        await axios.patch(`/admin-api/api/customers/${customer.id}/`, {
          status: customer.status === 'active' ? 'inactive' : 'active'
        })
        fetchCustomers()
      } catch (error) {
        console.error('Failed to toggle customer status:', error)
        alert('Failed to update customer status.')
      }
    }
    
    const deleteCustomer = async (customer) => {
      if (!confirm(`Are you sure you want to delete ${customer.name}?`)) {
        return
      }
      
      try {
        await axios.delete(`/admin-api/api/customers/${customer.id}/`)
        fetchCustomers()
      } catch (error) {
        console.error('Failed to delete customer:', error)
        alert('Failed to delete customer. Please try again.')
      }
    }
    
    const bulkToggleStatus = async () => {
      try {
        await axios.patch('/admin-api/api/customers/bulk_update/', {
          customer_ids: selectedCustomers.value,
          action: 'toggle_status'
        })
        fetchCustomers()
        clearSelection()
      } catch (error) {
        console.error('Failed to bulk update customers:', error)
        alert('Failed to update customers.')
      }
    }
    
    const bulkDelete = async () => {
      if (!confirm(`Are you sure you want to delete ${selectedCustomers.value.length} customer(s)?`)) {
        return
      }
      
      try {
        await axios.delete('/admin-api/api/customers/bulk_delete/', {
          data: { customer_ids: selectedCustomers.value }
        })
        fetchCustomers()
        clearSelection()
      } catch (error) {
        console.error('Failed to bulk delete customers:', error)
        alert('Failed to delete customers.')
      }
    }
    
    const exportCustomers = () => {
      // Implement export functionality
      console.log('Exporting customers...')
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    const truncateText = (text, maxLength) => {
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
    
    // Watchers
    watch([searchQuery, statusFilter, sortBy], () => {
      currentPage.value = 1
    })
    
    // Lifecycle
    onMounted(() => {
      fetchCustomers()
    })
    
    return {
      customers,
      loading,
      searchQuery,
      statusFilter,
      sortBy,
      currentPage,
      pageSize,
      totalCustomers,
      selectedCustomers,
      selectAll,
      showAddCustomerModal,
      editingCustomer,
      activeCustomers,
      newCustomersThisMonth,
      totalPages,
      visiblePages,
      debouncedSearch,
      applyFilters,
      changePage,
      toggleSelectAll,
      clearSelection,
      viewCustomer,
      editCustomer,
      closeCustomerModal,
      saveCustomer,
      toggleCustomerStatus,
      deleteCustomer,
      bulkToggleStatus,
      bulkDelete,
      exportCustomers,
      formatDate,
      truncateText
    }
  }
}
</script>

<style scoped>
.admin-customers {
  padding: 0;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.header-content h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.header-content p {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

/* Filters Section */
.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
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
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.search-box input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.filter-controls {
  display: flex;
  gap: 0.5rem;
}

.filter-controls select {
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.stat-icon.active { background: #28a745; }
.stat-icon.new { background: #ffc107; }

.stat-content h3 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.stat-content p {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

/* Table Container */
.table-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.table-header {
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #2c3e50;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.data-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-table tbody tr:hover {
  background: #f8f9fa;
}

.loading-row {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-row {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.empty-row i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Customer Info */
.customer-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.customer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.customer-info h4 {
  margin: 0;
  font-size: 1rem;
  color: #2c3e50;
}

.customer-info small {
  color: #6c757d;
  font-size: 0.8rem;
}

.contact-info {
  font-size: 0.9rem;
}

.contact-info div:first-child {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.contact-info div:last-child {
  color: #6c757d;
}

.address-info {
  font-size: 0.9rem;
  color: #495057;
  max-width: 200px;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.order-count {
  font-weight: 600;
  color: #007bff;
}

.date-info {
  font-size: 0.9rem;
  color: #495057;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.btn-icon {
  padding: 0.5rem;
  border: none;
  background: none;
  color: #6c757d;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #e9ecef;
  color: #495057;
}

.btn-icon.text-warning:hover {
  background: #fff3cd;
  color: #856404;
}

.btn-icon.text-success:hover {
  background: #d4edda;
  color: #155724;
}

.btn-icon.text-danger:hover {
  background: #f8d7da;
  color: #721c24;
}

/* Pagination */
.pagination-container {
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-info {
  color: #6c757d;
  font-size: 0.9rem;
}

.pagination {
  display: flex;
  gap: 0.25rem;
}

.page-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid #dee2e6;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f8f9fa;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

/* Bulk Actions */
.bulk-actions {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 100;
}

.bulk-info {
  font-weight: 500;
  color: #2c3e50;
}

.bulk-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 1rem;
  cursor: pointer;
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

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #545b62;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c82333;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-controls {
    justify-content: stretch;
  }
  
  .filter-controls select {
    flex: 1;
  }
  
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .bulk-actions {
    position: static;
    transform: none;
    margin-top: 1rem;
  }
}
</style>