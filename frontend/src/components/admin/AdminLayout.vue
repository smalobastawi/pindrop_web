<template>
  <div class="admin-layout">
    <!-- Header -->
    <header class="admin-header">
      <div class="header-content">
        <div class="logo">
          <h1>RiderApp Admin</h1>
        </div>
        <div class="header-actions">
          <div class="notifications">
            <button class="notification-btn" @click="showNotifications = !showNotifications">
              <i class="icon-bell"></i>
              <span v-if="unreadNotifications > 0" class="notification-badge">{{ unreadNotifications }}</span>
            </button>
            <div v-if="showNotifications" class="notification-dropdown">
              <h4>Notifications</h4>
              <div class="notification-list">
                <div v-for="notification in notifications" :key="notification.id" class="notification-item">
                  <p>{{ notification.message }}</p>
                  <small>{{ formatDate(notification.created_at) }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="admin-profile">
            <button class="profile-btn" @click="showProfileMenu = !showProfileMenu">
              <img :src="adminProfile.avatar || '/default-avatar.png'" alt="Profile" class="avatar">
              <span>{{ adminProfile.name || 'Admin User' }}</span>
              <i class="icon-chevron-down"></i>
            </button>
            <div v-if="showProfileMenu" class="profile-dropdown">
              <a href="#" @click="viewProfile">View Profile</a>
              <a href="#" @click="showChangePassword = true">Change Password</a>
              <hr>
              <a href="#" @click="logout">Logout</a>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="admin-body">
      <!-- Sidebar -->
      <aside class="admin-sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
        <nav class="sidebar-nav">
          <div class="nav-section">
            <h3>Main</h3>
            <ul>
              <li>
                <router-link to="/admin" class="nav-link">
                  <i class="icon-dashboard"></i>
                  <span>Dashboard</span>
                </router-link>
              </li>
            </ul>
          </div>

          <div class="nav-section">
            <h3>Management</h3>
            <ul>
              <li>
                <router-link to="/admin/customers" class="nav-link">
                  <i class="icon-users"></i>
                  <span>Customers</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/drivers" class="nav-link">
                  <i class="icon-truck"></i>
                  <span>Drivers/Riders</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/deliveries" class="nav-link">
                  <i class="icon-package"></i>
                  <span>Deliveries</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/routes" class="nav-link">
                  <i class="icon-map"></i>
                  <span>Routes</span>
                </router-link>
              </li>
            </ul>
          </div>

          <div class="nav-section">
            <h3>Analytics</h3>
            <ul>
              <li>
                <router-link to="/admin/reports" class="nav-link">
                  <i class="icon-bar-chart"></i>
                  <span>Reports</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/audit-logs" class="nav-link">
                  <i class="icon-activity"></i>
                  <span>Audit Logs</span>
                </router-link>
              </li>
            </ul>
          </div>

          <div class="nav-section" v-if="canManageUsers">
            <h3>Administration</h3>
            <ul>
              <li>
                <router-link to="/admin/users" class="nav-link">
                  <i class="icon-user-cog"></i>
                  <span>Users</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/roles" class="nav-link">
                  <i class="icon-shield"></i>
                  <span>Roles & Permissions</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/settings" class="nav-link">
                  <i class="icon-settings"></i>
                  <span>System Settings</span>
                </router-link>
              </li>
            </ul>
          </div>

          <div class="nav-section" v-if="canManageSettings">
            <h3>System</h3>
            <ul>
              <li>
                <router-link to="/admin/templates" class="nav-link">
                  <i class="icon-mail"></i>
                  <span>Templates</span>
                </router-link>
              </li>
              <li>
                <router-link to="/admin/backup" class="nav-link">
                  <i class="icon-database"></i>
                  <span>Backup</span>
                </router-link>
              </li>
            </ul>
          </div>
        </nav>

        <!-- Sidebar toggle -->
        <button class="sidebar-toggle" @click="toggleSidebar">
          <i :class="sidebarCollapsed ? 'icon-chevron-right' : 'icon-chevron-left'"></i>
        </button>
      </aside>

      <!-- Main content -->
      <main class="admin-main">
        <div class="main-content">
          <slot />
        </div>
      </main>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showChangePassword" class="modal-overlay" @click="showChangePassword = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Change Password</h3>
          <button @click="showChangePassword = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="changePassword">
            <div class="form-group">
              <label for="current-password">Current Password</label>
              <input 
                type="password" 
                id="current-password" 
                v-model="passwordForm.current_password"
                required
              >
            </div>
            <div class="form-group">
              <label for="new-password">New Password</label>
              <input 
                type="password" 
                id="new-password" 
                v-model="passwordForm.new_password"
                required
              >
            </div>
            <div class="form-group">
              <label for="confirm-password">Confirm New Password</label>
              <input 
                type="password" 
                id="confirm-password" 
                v-model="passwordForm.confirm_password"
                required
              >
            </div>
            <div class="modal-actions">
              <button type="button" @click="showChangePassword = false" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="changingPassword">
                {{ changingPassword ? 'Changing...' : 'Change Password' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '@/stores/adminAuth'

export default {
  name: 'AdminLayout',
  setup() {
    const router = useRouter()
    const adminAuthStore = useAdminAuthStore()
    
    // Reactive state
    const sidebarCollapsed = ref(false)
    const showNotifications = ref(false)
    const showProfileMenu = ref(false)
    const showChangePassword = ref(false)
    const notifications = ref([])
    const unreadNotifications = ref(0)
    const adminProfile = ref({})
    const changingPassword = ref(false)
    
    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    // Computed properties
    const canManageUsers = computed(() => {
      return adminAuthStore.hasPermission('manage_users')
    })
    
    const canManageSettings = computed(() => {
      return adminAuthStore.hasPermission('manage_settings')
    })
    
    // Methods
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('admin_sidebar_collapsed', sidebarCollapsed.value)
    }
    
    const viewProfile = () => {
      showProfileMenu.value = false
      router.push('/admin/profile')
    }
    
    const logout = async () => {
      try {
        await adminAuthStore.logout()
        router.push('/admin-login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    const changePassword = async () => {
      if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
        alert('New passwords do not match')
        return
      }
      
      changingPassword.value = true
      try {
        await adminAuthStore.changePassword(passwordForm.value)
        showChangePassword.value = false
        passwordForm.value = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
        alert('Password changed successfully')
      } catch (error) {
        alert('Failed to change password: ' + error.message)
      } finally {
        changingPassword.value = false
      }
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString()
    }
    
    const loadNotifications = async () => {
      try {
        // Load notifications from API
        const response = await adminAuthStore.api.get('/admin-api/dashboard/recent-activities?limit=5')
        notifications.value = response.data.activities || []
        unreadNotifications.value = notifications.value.length
      } catch (error) {
        console.error('Failed to load notifications:', error)
      }
    }
    
    const loadAdminProfile = async () => {
      try {
        const response = await adminAuthStore.api.get('/admin-api/users/me/')
        adminProfile.value = response.data
      } catch (error) {
        console.error('Failed to load admin profile:', error)
      }
    }
    
    // Lifecycle
    onMounted(() => {
      // Load saved sidebar state
      sidebarCollapsed.value = localStorage.getItem('admin_sidebar_collapsed') === 'true'
      
      // Load initial data
      loadNotifications()
      loadAdminProfile()
    })
    
    return {
      sidebarCollapsed,
      showNotifications,
      showProfileMenu,
      showChangePassword,
      notifications,
      unreadNotifications,
      adminProfile,
      passwordForm,
      changingPassword,
      canManageUsers,
      canManageSettings,
      toggleSidebar,
      viewProfile,
      logout,
      changePassword,
      formatDate
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9fa;
}

/* Header */
.admin-header {
  background: #fff;
  border-bottom: 1px solid #dee2e6;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  height: 60px;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #007bff;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Notifications */
.notifications {
  position: relative;
}

.notification-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  position: relative;
  color: #6c757d;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 300px;
  z-index: 1001;
}

.notification-dropdown h4 {
  margin: 0;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  font-size: 1rem;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f8f9fa;
}

.notification-item:last-child {
  border-bottom: none;
}

/* Profile */
.admin-profile {
  position: relative;
}

.profile-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #6c757d;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-width: 150px;
  z-index: 1001;
}

.profile-dropdown a {
  display: block;
  padding: 0.75rem 1rem;
  color: #495057;
  text-decoration: none;
  border-bottom: 1px solid #f8f9fa;
}

.profile-dropdown a:hover {
  background: #f8f9fa;
}

.profile-dropdown hr {
  margin: 0;
  border: none;
  border-top: 1px solid #dee2e6;
}

/* Body */
.admin-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Sidebar */
.admin-sidebar {
  width: 250px;
  background: #343a40;
  color: white;
  position: relative;
  transition: width 0.3s ease;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-nav {
  padding: 1rem 0;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 1.5rem;
}

.nav-section h3 {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #adb5bd;
  padding: 0 1rem;
  margin-bottom: 0.5rem;
}

.nav-section ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #dee2e6;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: #495057;
  color: white;
}

.nav-link.router-link-active {
  background: #007bff;
  color: white;
}

.nav-link i {
  width: 20px;
  margin-right: 0.75rem;
}

.sidebar-collapsed .nav-link span {
  display: none;
}

.sidebar-toggle {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: #495057;
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Main content */
.admin-main {
  flex: 1;
  overflow-y: auto;
  background: #f8f9fa;
}

.main-content {
  padding: 1.5rem;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal {
  background: white;
  border-radius: 0.375rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 1.5rem;
}

/* Forms */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  transition: all 0.2s ease;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>