<template>
  <AdminLayout>
    <div class="admin-users">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <div>
            <h1>User Management</h1>
            <p>Manage admin users and their permissions</p>
          </div>
          <button 
            @click="showAddUserModal = true"
            class="btn btn-primary"
            :disabled="loading"
          >
            <i class="icon-user-plus"></i>
            Add User
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
            placeholder="Search users..."
            @input="debouncedSearch"
          >
        </div>
        <div class="filter-controls">
          <select v-model="roleFilter" @change="applyFilters">
            <option value="">All Roles</option>
            <option value="super_admin">Super Admin</option>
            <option value="admin">Admin</option>
            <option value="manager">Manager</option>
            <option value="operator">Operator</option>
            <option value="viewer">Viewer</option>
          </select>
          <select v-model="statusFilter" @change="applyFilters">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      <!-- Users Table -->
      <div class="table-container">
        <div class="table-header">
          <h3>Admin Users</h3>
          <div class="table-actions">
            <button 
              @click="exportUsers"
              class="btn btn-secondary btn-sm"
              :disabled="loading || users.length === 0"
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
                <th>User</th>
                <th>Role</th>
                <th>Department</th>
                <th>Status</th>
                <th>Last Login</th>
                <th>Login Count</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="7" class="loading-row">
                  <div class="loading-spinner"></div>
                  Loading users...
                </td>
              </tr>
              <tr v-else-if="users.length === 0">
                <td colspan="7" class="empty-row">
                  <i class="icon-users"></i>
                  <p>No admin users found</p>
                  <button 
                    @click="showAddUserModal = true"
                    class="btn btn-primary btn-sm"
                  >
                    Add First User
                  </button>
                </td>
              </tr>
              <tr v-for="user in users" :key="user.id">
                <td>
                  <div class="user-info">
                    <div class="user-avatar">
                      <i class="icon-user"></i>
                    </div>
                    <div>
                      <h4>{{ user.full_name || user.user.username }}</h4>
                      <div class="user-details">
                        <span>{{ user.user.email }}</span>
                        <small>ID: {{ user.id }}</small>
                      </div>
                    </div>
                  </div>
                </td>
                <td>
                  <span :class="['role-badge', `role-${user.role}`]">
                    {{ formatRole(user.role) }}
                  </span>
                  <div v-if="user.custom_role" class="custom-role">
                    <small>{{ user.custom_role.name }}</small>
                  </div>
                </td>
                <td>
                  <div class="dept-info">
                    {{ user.department || 'Not assigned' }}
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <div class="date-info">
                    {{ user.last_login ? formatDate(user.last_login) : 'Never' }}
                  </div>
                </td>
                <td>
                  <span class="login-count">
                    {{ user.login_count || 0 }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button 
                      @click="viewUser(user)"
                      class="btn-icon"
                      title="View Details"
                    >
                      <i class="icon-eye"></i>
                    </button>
                    <button 
                      @click="editUser(user)"
                      class="btn-icon"
                      title="Edit User"
                    >
                      <i class="icon-edit"></i>
                    </button>
                    <button 
                      @click="toggleUserStatus(user)"
                      :class="['btn-icon', user.is_active ? 'text-warning' : 'text-success']"
                      :title="user.is_active ? 'Deactivate' : 'Activate'"
                    >
                      <i :class="user.is_active ? 'icon-pause' : 'icon-play'"></i>
                    </button>
                    <button 
                      @click="resetPassword(user)"
                      class="btn-icon"
                      title="Reset Password"
                    >
                      <i class="icon-key"></i>
                    </button>
                    <button 
                      @click="deleteUser(user)"
                      class="btn-icon text-danger"
                      title="Delete User"
                      :disabled="user.role === 'super_admin'"
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
            {{ Math.min(currentPage * pageSize, totalUsers) }} of 
            {{ totalUsers }} users
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
    </div>

    <!-- Add/Edit User Modal -->
    <UserModal
      v-if="showAddUserModal || editingUser"
      :user="editingUser"
      @close="closeUserModal"
      @save="saveUser"
    />
  </AdminLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import UserModal from '@/components/admin/UserModal.vue'
import axios from 'axios'
import debounce from 'lodash/debounce'

export default {
  name: 'AdminUsers',
  components: {
    AdminLayout,
    UserModal
  },
  setup() {
    // Reactive state
    const users = ref([])
    const loading = ref(false)
    const searchQuery = ref('')
    const roleFilter = ref('')
    const statusFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalUsers = ref(0)
    
    // Modal state
    const showAddUserModal = ref(false)
    const editingUser = ref(null)
    
    // Computed properties
    const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize.value))
    
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
    const fetchUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value,
          role: roleFilter.value,
          is_active: statusFilter.value
        }
        
        const response = await axios.get('/admin-api/users/', { params })
        users.value = response.data.results || response.data
        totalUsers.value = response.data.count || response.data.length
        
      } catch (error) {
        console.error('Failed to fetch users:', error)
        alert('Failed to load users. Please try again.')
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = debounce(() => {
      currentPage.value = 1
      fetchUsers()
    }, 500)
    
    const applyFilters = () => {
      currentPage.value = 1
      fetchUsers()
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchUsers()
      }
    }
    
    const formatRole = (role) => {
      const roleMap = {
        'super_admin': 'Super Admin',
        'admin': 'Administrator',
        'manager': 'Manager',
        'operator': 'Operator',
        'viewer': 'Viewer'
      }
      return roleMap[role] || role
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    const viewUser = (user) => {
      console.log('View user:', user)
      // Navigate to user detail page or show modal
    }
    
    const editUser = (user) => {
      editingUser.value = { ...user }
      showAddUserModal.value = true
    }
    
    const closeUserModal = () => {
      showAddUserModal.value = false
      editingUser.value = null
    }
    
    const saveUser = async (userData) => {
      try {
        if (editingUser.value) {
          await axios.put(`/admin-api/users/${editingUser.value.id}/`, userData)
        } else {
          await axios.post('/admin-api/users/', userData)
        }
        
        closeUserModal()
        fetchUsers()
      } catch (error) {
        console.error('Failed to save user:', error)
        alert('Failed to save user. Please try again.')
      }
    }
    
    const toggleUserStatus = async (user) => {
      try {
        await axios.post(`/admin-api/users/${user.id}/toggle_status/`)
        fetchUsers()
      } catch (error) {
        console.error('Failed to toggle user status:', error)
        alert('Failed to update user status.')
      }
    }
    
    const resetPassword = async (user) => {
      if (!confirm(`Are you sure you want to reset the password for ${user.full_name || user.user.username}?`)) {
        return
      }
      
      try {
        await axios.post(`/admin-api/users/${user.id}/reset_password/`)
        alert('Password reset successfully. A temporary password has been sent to the user.')
      } catch (error) {
        console.error('Failed to reset password:', error)
        alert('Failed to reset password.')
      }
    }
    
    const deleteUser = async (user) => {
      if (user.role === 'super_admin') {
        alert('Cannot delete super admin users.')
        return
      }
      
      if (!confirm(`Are you sure you want to delete ${user.full_name || user.user.username}?`)) {
        return
      }
      
      try {
        await axios.delete(`/admin-api/users/${user.id}/`)
        fetchUsers()
      } catch (error) {
        console.error('Failed to delete user:', error)
        alert('Failed to delete user. Please try again.')
      }
    }
    
    const exportUsers = () => {
      // Implement export functionality
      console.log('Exporting users...')
    }
    
    // Lifecycle
    onMounted(() => {
      fetchUsers()
    })
    
    return {
      users,
      loading,
      searchQuery,
      roleFilter,
      statusFilter,
      currentPage,
      pageSize,
      totalUsers,
      showAddUserModal,
      editingUser,
      totalPages,
      visiblePages,
      debouncedSearch,
      applyFilters,
      changePage,
      formatRole,
      formatDate,
      viewUser,
      editUser,
      closeUserModal,
      saveUser,
      toggleUserStatus,
      resetPassword,
      deleteUser,
      exportUsers
    }
  }
}
</script>

<style scoped>
.admin-users {
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

/* User Info */
.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.user-info h4 {
  margin: 0;
  font-size: 1rem;
  color: #2c3e50;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-details span {
  font-size: 0.9rem;
  color: #495057;
}

.user-details small {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Role Badge */
.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.role-super_admin { background: #dc3545; color: white; }
.role-admin { background: #007bff; color: white; }
.role-manager { background: #28a745; color: white; }
.role-operator { background: #ffc107; color: #212529; }
.role-viewer { background: #6c757d; color: white; }

.custom-role {
  margin-top: 0.25rem;
}

.custom-role small {
  font-size: 0.75rem;
  color: #6c757d;
  font-style: italic;
}

/* Department Info */
.dept-info {
  font-size: 0.9rem;
  color: #495057;
}

/* Status Badge */
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

/* Date Info */
.date-info {
  font-size: 0.9rem;
  color: #495057;
}

/* Login Count */
.login-count {
  font-weight: 600;
  color: #007bff;
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

.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  
  .table-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>