// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Admin routes
    {
      path: '/admin',
      name: 'AdminDashboard',
      component: () => import('@/views/admin/AdminDashboard.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/customers',
      name: 'AdminCustomers',
      component: () => import('@/views/admin/AdminCustomers.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/drivers',
      name: 'AdminDrivers',
      component: () => import('@/views/admin/AdminDrivers.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/deliveries',
      name: 'AdminDeliveries',
      component: () => import('@/views/admin/AdminDeliveries.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/deliveries/new',
      name: 'AdminNewDelivery',
      component: () => import('@/views/admin/AdminNewDelivery.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/routes',
      name: 'AdminRoutes',
      component: () => import('@/views/admin/AdminRoutes.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/users',
      name: 'AdminUsers',
      component: () => import('@/views/admin/AdminUsers.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/roles',
      name: 'AdminRoles',
      component: () => import('@/views/admin/AdminRoles.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/settings',
      name: 'AdminSettings',
      component: () => import('@/views/admin/AdminSettings.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/reports',
      name: 'AdminReports',
      component: () => import('@/views/admin/AdminReports.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/audit-logs',
      name: 'AdminAuditLogs',
      component: () => import('@/views/admin/AdminAuditLogs.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/templates',
      name: 'AdminTemplates',
      component: () => import('@/views/admin/AdminTemplates.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/backup',
      name: 'AdminBackup',
      component: () => import('@/views/admin/AdminBackup.vue'),
      meta: { requiresAdminAuth: true }
    },
    {
      path: '/admin/profile',
      name: 'AdminProfile',
      component: () => import('@/views/admin/AdminProfile.vue'),
      meta: { requiresAdminAuth: true }
    },
    
    // Legacy admin routes (for backward compatibility)
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
 {
  path: '/',
  name: 'Home',
  component: () => import('@/views/LandingPage.vue'),
  meta: { requiresAuth: false }
},
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/deliveries',
      name: 'Deliveries',
      component: () => import('@/views/Deliveries.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/deliveries/new',
      name: 'NewDelivery',
      component: () => import('@/views/NewDelivery.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/deliveries/:id',
      name: 'DeliveryDetail',
      component: () => import('@/views/DeliveryDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/customers',
      name: 'Customers',
      component: () => import('@/views/Customers.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/drivers',
      name: 'Drivers',
      component: () => import('@/views/Drivers.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/views/Settings.vue'),
      meta: { requiresAdminAuth: true }
    },

    // Customer routes
    {
      path: '/customer-portal/login',
      name: 'CustomerLogin',
      component: () => import('@/views/CustomerLogin.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-portal/register',
      name: 'CustomerRegister',
      component: () => import('@/views/CustomerRegister.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-login',
      name: 'CustomerLoginLegacy',
      component: () => import('@/views/CustomerLogin.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-register',
      name: 'CustomerRegisterLegacy',
      component: () => import('@/views/CustomerRegister.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-portal',
      name: 'CustomerPortal',
      component: () => import('@/views/CustomerPortal.vue'),
      meta: { requiresCustomerAuth: true, title: 'Customer Portal' }
    },
    {
      path: '/rider-register',
      name: 'RiderRegister',
      component: () => import('@/views/RiderRegister.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/rider-login',
      name: 'RiderLogin',
      component: () => import('@/views/RiderLogin.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/rider-portal',
      name: 'RiderPortal',
      component: () => import('@/views/RiderPortal.vue'),
      meta: { requiresRiderAuth: true, title: 'Rider Portal' }
    }
  ]
})

// Move admin auth initialization to router guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Import admin store only when needed to avoid initialization issues
  let adminAuthStore = null
  
  // Check for admin routes
  if (to.meta.requiresAdminAuth) {
    // Dynamic import to avoid initialization issues
    import('@/stores/adminAuth').then(({ useAdminAuthStore }) => {
      adminAuthStore = useAdminAuthStore()
      
      if (!adminAuthStore.isAuthenticated) {
        next('/login')
        return
      }
      
      // Continue with other checks
      checkOtherRoutes(to, next, authStore, adminAuthStore)
    }).catch(() => {
      next('/login')
    })
    return
  }
  
  // For non-admin routes, proceed with normal checks
  checkOtherRoutes(to, next, authStore, adminAuthStore)
})

// Helper function for route checks
function checkOtherRoutes(to, next, authStore, adminAuthStore) {
  // Check for customer routes
  if (to.meta.requiresCustomerAuth) {
    const customerToken = localStorage.getItem('access_token')
    if (!customerToken) {
      next('/customer-portal/login')
      return
    }
  }

  // Check for rider routes
  if (to.meta.requiresRiderAuth) {
    const riderToken = localStorage.getItem('access_token')
    if (!riderToken) {
      next('/rider-login')
      return
    }
  }
  
  // Check for regular admin routes
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Handle login redirects
  if (to.name === 'Login' && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  if (to.name === 'CustomerLogin' || to.name === 'CustomerLoginLegacy') {
    const customerToken = localStorage.getItem('access_token')
    if (customerToken) {
      next('/customer-portal')
      return
    }
  }
  
  if (to.name === 'CustomerRegister' || to.name === 'CustomerRegisterLegacy') {
    const customerToken = localStorage.getItem('access_token')
    if (customerToken) {
      next('/customer-portal')
      return
    }
  }
  
  next()
}

export default router