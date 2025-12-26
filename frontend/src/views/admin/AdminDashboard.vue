<template>
  <AdminLayout>
    <div class="admin-dashboard">
      <!-- Page Header -->
      <div class="page-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {{ adminProfile?.full_name || 'Admin' }}!</p>
      </div>

      <!-- Statistics Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon customers">
            <i class="icon-users"></i>
          </div>
          <div class="stat-content">
            <h3>{{ dashboardStats.total_customers }}</h3>
            <p>Total Customers</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon drivers">
            <i class="icon-truck"></i>
          </div>
          <div class="stat-content">
            <h3>{{ dashboardStats.total_drivers }}</h3>
            <p>Total Drivers</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon deliveries">
            <i class="icon-package"></i>
          </div>
          <div class="stat-content">
            <h3>{{ dashboardStats.total_deliveries }}</h3>
            <p>Total Deliveries</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon revenue">
            <i class="icon-dollar-sign"></i>
          </div>
          <div class="stat-content">
            <h3>${{ (parseFloat(dashboardStats.total_revenue_today) || 0).toFixed(2) }}</h3>
            <p>Revenue Today</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions & Alerts -->
      <div class="dashboard-grid">
        <!-- Quick Actions -->
        <div class="dashboard-card">
          <h3>Quick Actions</h3>
          <div class="quick-actions">
            <button 
              v-if="canManageDeliveries" 
              @click="$router.push('/admin/deliveries/new')"
              class="action-btn"
            >
              <i class="icon-plus"></i>
              New Delivery
            </button>
            <button 
              v-if="canManageCustomers" 
              @click="$router.push('/admin/customers/new')"
              class="action-btn"
            >
              <i class="icon-user-plus"></i>
              Add Customer
            </button>
            <button 
              v-if="canManageUsers" 
              @click="$router.push('/admin/users/new')"
              class="action-btn"
            >
              <i class="icon-user-cog"></i>
              Add Admin User
            </button>
            <button 
              @click="$router.push('/admin/reports')"
              class="action-btn"
            >
              <i class="icon-bar-chart"></i>
              View Reports
            </button>
          </div>
        </div>

        <!-- System Alerts -->
        <div class="dashboard-card">
          <h3>System Alerts</h3>
          <div class="alerts-list">
            <div v-if="dashboardStats.pending_deliveries > 10" class="alert alert-warning">
              <i class="icon-alert-triangle"></i>
              <span>{{ dashboardStats.pending_deliveries }} pending deliveries</span>
            </div>
            <div v-if="dashboardStats.delivery_success_rate < 90" class="alert alert-danger">
              <i class="icon-alert-circle"></i>
              <span>Low delivery success rate: {{ dashboardStats.delivery_success_rate }}%</span>
            </div>
            <div v-if="dashboardStats.active_drivers === 0" class="alert alert-info">
              <i class="icon-info"></i>
              <span>No active drivers available</span>
            </div>
            <div v-if="noAlerts" class="alert alert-success">
              <i class="icon-check-circle"></i>
              <span>All systems running smoothly</span>
            </div>
          </div>
        </div>

        <!-- Recent Activities -->
        <div class="dashboard-card">
          <h3>Recent Activities</h3>
          <div class="activities-list">
            <div 
              v-for="activity in recentActivities" 
              :key="activity.id" 
              class="activity-item"
            >
              <div class="activity-icon">
                <i :class="getActivityIcon(activity.action)"></i>
              </div>
              <div class="activity-content">
                <p>{{ getActivityDescription(activity) }}</p>
                <small>{{ formatDate(activity.timestamp) }}</small>
              </div>
            </div>
            <div v-if="recentActivities.length === 0" class="no-activities">
              <p>No recent activities</p>
            </div>
          </div>
        </div>

        <!-- Delivery Trends -->
        <div class="dashboard-card">
          <h3>Delivery Trends (Last 30 Days)</h3>
          <div class="chart-container">
            <canvas ref="trendChart" width="400" height="200"></canvas>
          </div>
        </div>
      </div>

      <!-- Performance Overview -->
      <div class="dashboard-grid" v-if="canViewReports">
        <!-- Driver Performance -->
        <div class="dashboard-card">
          <h3>Top Driver Performance</h3>
          <div class="driver-list">
            <div 
              v-for="driver in topDrivers.slice(0, 5)" 
              :key="driver.id" 
              class="driver-item"
            >
              <div class="driver-info">
                <h4>{{ driver.name }}</h4>
                <div class="driver-stats">
                  <span class="stat">{{ driver.completed_deliveries }} completed</span>
                  <span class="stat">{{ driver.success_rate }}% success</span>
                  <span :class="['status', driver.is_available ? 'available' : 'busy']">
                    {{ driver.is_available ? 'Available' : 'Busy' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Health -->
        <div class="dashboard-card">
          <h3>System Health</h3>
          <div class="health-metrics">
            <div class="health-item">
              <span class="metric-label">API Response Time</span>
              <span class="metric-value good">145ms</span>
            </div>
            <div class="health-item">
              <span class="metric-label">Database Connections</span>
              <span class="metric-value good">8/20</span>
            </div>
            <div class="health-item">
              <span class="metric-label">Server Uptime</span>
              <span class="metric-value good">99.9%</span>
            </div>
            <div class="health-item">
              <span class="metric-label">Storage Usage</span>
              <span class="metric-value warning">78%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import { useAdminAuthStore } from '@/stores/adminAuth'
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'AdminDashboard',
  components: {
    AdminLayout
  },
  setup() {
    const adminAuthStore = useAdminAuthStore()
    
    // Reactive state
    const dashboardStats = ref({})
    const recentActivities = ref([])
    const deliveryTrends = ref([])
    const topDrivers = ref([])
    const trendChart = ref(null)
    const chartInstance = ref(null)
    
    // Computed properties
    const adminProfile = computed(() => adminAuthStore.user)
    const canManageDeliveries = computed(() => adminAuthStore.canManageDeliveries)
    const canManageCustomers = computed(() => adminAuthStore.hasPermission('manage_customers'))
    const canManageUsers = computed(() => adminAuthStore.canManageUsers)
    const canViewReports = computed(() => adminAuthStore.canViewReports)
    
    const noAlerts = computed(() => {
      return dashboardStats.value.pending_deliveries <= 10 && 
             dashboardStats.value.delivery_success_rate >= 90 &&
             dashboardStats.value.active_drivers > 0
    })
    
    // Methods
    const loadDashboardData = async () => {
      try {
        // Load dashboard statistics
        const statsResponse = await axios.get('/admin-api/api/dashboard/stats/')
        dashboardStats.value = statsResponse.data

        // Load recent activities
        const activitiesResponse = await axios.get('/admin-api/api/dashboard/recent-activities/?limit=10')
        recentActivities.value = activitiesResponse.data.activities || []

        // Load delivery trends
        const trendsResponse = await axios.get('/admin-api/api/dashboard/delivery_trends/')
        deliveryTrends.value = trendsResponse.data.trends || []

        // Load driver performance
        const driversResponse = await axios.get('/admin-api/api/dashboard/driver_performance/')
        topDrivers.value = driversResponse.data.drivers || []

        // Create trend chart
        await nextTick()
        createTrendChart()

      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      }
    }
    
    const createTrendChart = () => {
      if (!trendChart.value || deliveryTrends.value.length === 0) return
      
      const ctx = trendChart.value.getContext('2d')
      
      const labels = deliveryTrends.value.map(trend => 
        new Date(trend.date).toLocaleDateString()
      )
      const createdData = deliveryTrends.value.map(trend => trend.created)
      const completedData = deliveryTrends.value.map(trend => trend.completed)
      
      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Created',
              data: createdData,
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.1)',
              tension: 0.1
            },
            {
              label: 'Completed',
              data: completedData,
              borderColor: '#28a745',
              backgroundColor: 'rgba(40, 167, 69, 0.1)',
              tension: 0.1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }
    
    const getActivityIcon = (action) => {
      const iconMap = {
        'create': 'icon-plus-circle',
        'update': 'icon-edit',
        'delete': 'icon-trash-2',
        'login': 'icon-log-in',
        'logout': 'icon-log-out'
      }
      return iconMap[action] || 'icon-activity'
    }
    
    const getActivityDescription = (activity) => {
      const action = activity.action
      const model = activity.model_name
      
      if (action === 'login') {
        return `${activity.user_details?.username || 'User'} logged in`
      }
      
      if (model) {
        return `${activity.user_details?.username || 'User'} ${action}d a ${model.toLowerCase()}`
      }
      
      return `${activity.user_details?.username || 'User'} performed ${action}`
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)
      
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins} minutes ago`
      if (diffHours < 24) return `${diffHours} hours ago`
      if (diffDays < 7) return `${diffDays} days ago`
      
      return date.toLocaleDateString()
    }
    
    // Lifecycle
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      dashboardStats,
      recentActivities,
      deliveryTrends,
      topDrivers,
      trendChart,
      adminProfile,
      canManageDeliveries,
      canManageCustomers,
      canManageUsers,
      canViewReports,
      noAlerts,
      loadDashboardData,
      getActivityIcon,
      getActivityDescription,
      formatDate
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 0;
}

/* Page Header */
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
}

/* Statistics Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
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
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.customers { background: #17a2b8; }
.stat-icon.drivers { background: #fd7e14; }
.stat-icon.deliveries { background: #6f42c1; }
.stat-icon.revenue { background: #28a745; }

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.stat-content p {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dashboard-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background: #0056b3;
}

/* Alerts */
.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
}

.alert-warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.alert-danger {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

/* Activities */
.activities-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  background: #f8f9fa;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.activity-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #495057;
}

.activity-content small {
  color: #6c757d;
  font-size: 0.8rem;
}

.no-activities {
  text-align: center;
  color: #6c757d;
  padding: 2rem;
}

/* Chart */
.chart-container {
  height: 200px;
  position: relative;
}

/* Driver Performance */
.driver-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.driver-item {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
}

.driver-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #2c3e50;
}

.driver-stats {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.driver-stats .stat {
  font-size: 0.85rem;
  color: #6c757d;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status.available {
  background: #d4edda;
  color: #155724;
}

.status.busy {
  background: #f8d7da;
  color: #721c24;
}

/* System Health */
.health-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.health-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 0.375rem;
}

.metric-label {
  font-size: 0.9rem;
  color: #495057;
}

.metric-value {
  font-weight: 600;
  font-size: 0.9rem;
}

.metric-value.good {
  color: #28a745;
}

.metric-value.warning {
  color: #ffc107;
}

.metric-value.danger {
  color: #dc3545;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    flex-direction: column;
  }
  
  .driver-stats {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>