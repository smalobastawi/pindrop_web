<!-- frontend/src/components/layout/CommonHeader.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold text-primary" to="/">
        <i class="fas fa-shipping-fast me-2"></i>RiderApp
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <a href="#features" class="nav-link">Features</a>
          </li>
          <li class="nav-item">
            <a href="#how-it-works" class="nav-link">How It Works</a>
          </li>
          <li class="nav-item">
            <a href="#customers" class="nav-link">Customers</a>
          </li>
          <li class="nav-item">
            <a href="#riders" class="nav-link">Riders</a>
          </li>
          <li class="nav-item">
            <a href="#pricing" class="nav-link">Pricing</a>
          </li>
         
          <!-- Show Login and Register when NOT authenticated -->
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link to="/customer-login" class="nav-link">Login</router-link>
            </li>
           
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="registerDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Register
              </a>
              <ul class="dropdown-menu" aria-labelledby="registerDropdown">
                <li><router-link to="/customer-register" class="dropdown-item">Customer Register</router-link></li>
                <li><router-link to="/rider-register" class="dropdown-item">Rider Register</router-link></li>
              </ul>
            </li>
          </template>
          
          <!-- Show user avatar, name and dropdown when authenticated -->
          <template v-else>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle d-flex align-items-center user-dropdown" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <div class="user-avatar me-2">
                  <img 
                    v-if="authStore.user?.avatar" 
                    :src="authStore.user.avatar" 
                    :alt="userName" 
                    class="rounded-circle"
                  />
                  <div v-else class="avatar-placeholder rounded-circle">
                    {{ userInitials }}
                  </div>
                </div>
                <span class="user-name d-none d-md-inline">{{ userName }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                <li class="dropdown-header">
                  <div class="d-flex align-items-center">
                    <div class="user-avatar me-2">
                      <img 
                        v-if="authStore.user?.avatar" 
                        :src="authStore.user.avatar" 
                        :alt="userName" 
                        class="rounded-circle"
                      />
                      <div v-else class="avatar-placeholder rounded-circle">
                        {{ userInitials }}
                      </div>
                    </div>
                    <div>
                      <div class="fw-bold">{{ userName }}</div>
                      <small class="text-muted">{{ authStore.user?.email }}</small>
                    </div>
                  </div>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <router-link to="/customer-portal" class="dropdown-item">
                    <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                  </router-link>
                </li>
                <li>
                  <router-link to="/customer-portal" class="dropdown-item">
                    <i class="fas fa-user me-2"></i>My Profile
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a href="#" class="dropdown-item text-danger" @click.prevent="handleLogout">
                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Computed property for user's display name
const userName = computed(() => {
  if (authStore.user?.first_name && authStore.user?.last_name) {
    return `${authStore.user.first_name} ${authStore.user.last_name}`
  }
  if (authStore.user?.first_name) {
    return authStore.user.first_name
  }
  if (authStore.user?.username) {
    return authStore.user.username
  }
  return authStore.user?.email || 'User'
})

// Computed property for user initials (for avatar placeholder)
const userInitials = computed(() => {
  if (authStore.user?.first_name && authStore.user?.last_name) {
    return `${authStore.user.first_name[0]}${authStore.user.last_name[0]}`.toUpperCase()
  }
  if (authStore.user?.first_name) {
    return authStore.user.first_name.substring(0, 2).toUpperCase()
  }
  if (authStore.user?.username) {
    return authStore.user.username.substring(0, 2).toUpperCase()
  }
  if (authStore.user?.email) {
    return authStore.user.email.substring(0, 2).toUpperCase()
  }
  return 'U'
})

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.navbar {
  padding: 1rem 0;
  transition: all 0.3s ease;
  z-index: 1030;
}

.navbar.scrolled {
  padding: 0.5rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  color: #007bff !important;
}

.nav-link:hover {
  color: #0056b3 !important;
}

/* User avatar styles */
.user-avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 2px solid #007bff;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid #007bff;
}

.user-dropdown {
  padding: 0.5rem 1rem;
}

.user-name {
  font-weight: 500;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-header {
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
}

.dropdown-header .user-avatar {
  width: 40px;
  height: 40px;
}

.dropdown-menu {
  min-width: 250px;
  border: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  border-radius: 8px;
}

.dropdown-item {
  padding: 0.6rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f0f7ff;
}

.dropdown-item.text-danger:hover {
  background-color: #fff0f0;
}
</style>