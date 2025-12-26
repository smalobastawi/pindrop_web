<template>
  <div class="rider-portal">
    <div class="container">
      <h1>Rider Portal</h1>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="!loading && !error">
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Total Deliveries</h3>
            <p>{{ stats.total_deliveries }}</p>
          </div>
          <div class="stat-card">
            <h3>Pending Deliveries</h3>
            <p>{{ stats.pending_deliveries }}</p>
          </div>
          <div class="stat-card">
            <h3>In Transit</h3>
            <p>{{ stats.in_transit }}</p>
          </div>
          <div class="stat-card">
            <h3>Completed Deliveries</h3>
            <p>{{ stats.completed_deliveries }}</p>
          </div>
          <div class="stat-card">
            <h3>Total Earnings</h3>
            <p>{{ formatCurrency(stats.total_earnings) }}</p>
          </div>
          <div class="stat-card">
            <h3>Rating</h3>
            <p>{{ stats.rating }}/5</p>
          </div>
          <div class="stat-card">
            <h3>Availability</h3>
            <p :class="stats.is_available ? 'available' : 'unavailable'">{{ stats.is_available ? 'Online' : 'Offline' }}</p>
          </div>
        </div>
        <div class="availability-section">
          <h2>Availability</h2>
          <button @click="toggleAvailability" :class="rider.is_available ? 'btn-danger' : 'btn-success'">
            {{ rider.is_available ? 'Go Offline' : 'Go Online' }}
          </button>
        </div>
        <div class="deliveries-section">
          <h2>Your Deliveries</h2>
          <div v-if="deliveries.length === 0" class="no-deliveries">
            <p>You haven't been assigned any deliveries yet.</p>
          </div>
          <div v-else class="deliveries-list">
            <div v-for="delivery in deliveries" :key="delivery.id" class="delivery-card">
              <div class="delivery-header">
                <h3>Delivery #{{ delivery.tracking_number }}</h3>
                <span class="status" :class="delivery.status">{{ delivery.status }}</span>
              </div>
              <div class="delivery-details">
                <p><strong>Sender:</strong> {{ delivery.sender.user.first_name }} {{ delivery.sender.user.last_name }}</p>
                <p><strong>Recipient:</strong> {{ delivery.recipient_name }}</p>
                <p><strong>Pickup:</strong> {{ delivery.pickup_address }}</p>
                <p><strong>Delivery:</strong> {{ delivery.delivery_address }}</p>
                <p><strong>Estimated Delivery:</strong> {{ delivery.estimated_delivery }}</p>
                <p v-if="delivery.payment"><strong>Fee:</strong> {{ formatCurrency(delivery.delivery_fee) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RiderPortal',
  data() {
    return {
      rider: null,
      deliveries: [],
      stats: {},
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'KES'
      }).format(amount)
    },
    async fetchData() {
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('/api/rider/portal/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.rider = response.data.rider
        this.deliveries = response.data.deliveries
        this.stats = response.data.stats
      } catch (error) {
        this.error = 'Failed to load rider data'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async toggleAvailability() {
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.post('/api/mobile/rider/availability/', {
          is_available: !this.rider.is_available
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.rider.is_available = response.data.is_available
        this.stats.is_available = response.data.is_available
      } catch (error) {
        alert('Failed to update availability')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.rider-portal {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  color: #333;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #e9ecef;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #495057;
  font-size: 14px;
  text-transform: uppercase;
}

.stat-card p {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #007bff;
}

.stat-card p.available {
  color: #28a745;
}

.stat-card p.unavailable {
  color: #dc3545;
}

.availability-section {
  margin-bottom: 40px;
  text-align: center;
}

.availability-section h2 {
  margin-bottom: 20px;
}

.btn-success {
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.btn-danger {
  background: #dc3545;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.btn-success:hover {
  background: #218838;
}

.btn-danger:hover {
  background: #c82333;
}

.deliveries-section {
  margin-bottom: 40px;
}

.deliveries-list {
  display: grid;
  gap: 20px;
}

.delivery-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  background: #fff;
}

.delivery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.delivery-header h3 {
  margin: 0;
  color: #333;
}

.status {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
  font-weight: bold;
}

.status.pending { background: #ffc107; color: #212529; }
.status.assigned { background: #17a2b8; color: white; }
.status.in_transit { background: #007bff; color: white; }
.status.delivered { background: #28a745; color: white; }
.status.cancelled { background: #dc3545; color: white; }

.delivery-details p {
  margin: 5px 0;
  color: #666;
}

.no-deliveries {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}
</style>