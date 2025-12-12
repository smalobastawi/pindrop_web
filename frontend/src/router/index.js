// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Admin routes
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      redirect: '/dashboard'
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
      meta: { requiresAuth: true }
    },
    
    // Customer routes
    {
      path: '/customer-login',
      name: 'CustomerLogin',
      component: () => import('@/views/CustomerLogin.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-register',
      name: 'CustomerRegister',
      component: () => import('@/views/CustomerRegister.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/customer-portal',
      name: 'CustomerPortal',
      component: () => import('@/views/CustomerPortal.vue'),
      meta: { requiresCustomerAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check for customer routes
  if (to.meta.requiresCustomerAuth) {
    const customerToken = localStorage.getItem('access_token')
    if (!customerToken) {
      next('/customer-login')
      return
    }
  }
  
  // Check for admin routes
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Handle login redirects
  if (to.name === 'Login' && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  if (to.name === 'CustomerLogin') {
    const customerToken = localStorage.getItem('access_token')
    if (customerToken) {
      next('/customer-portal')
      return
    }
  }
  
  next()
})

export default router