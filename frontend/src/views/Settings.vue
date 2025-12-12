<template>
  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Settings</h1>
  </div>

  <div class="row">
    <div class="col-md-8">
      <div class="card mb-4">
        <div class="card-header">
          <h5>General Settings</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="saveGeneralSettings">
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Company Name</label>
                <input v-model="settings.general.company_name" type="text" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Support Email</label>
                <input v-model="settings.general.support_email" type="email" class="form-control" />
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Company Address</label>
              <textarea v-model="settings.general.company_address" class="form-control" rows="2"></textarea>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Phone Number</label>
                <input v-model="settings.general.phone" type="tel" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Business Hours</label>
                <input v-model="settings.general.business_hours" type="text" class="form-control" placeholder="8:00 AM - 6:00 PM" />
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary">Save General Settings</button>
          </form>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h5>Delivery Settings</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="saveDeliverySettings">
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Base Delivery Fee</label>
                <div class="input-group">
                  <span class="input-group-text">$</span>
                  <input v-model.number="settings.delivery.base_fee" type="number" step="0.01" class="form-control" />
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label">Fee per Kilogram</label>
                <div class="input-group">
                  <span class="input-group-text">$</span>
                  <input v-model.number="settings.delivery.fee_per_kg" type="number" step="0.01" class="form-control" />
                </div>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Express Delivery Multiplier</label>
                <input v-model.number="settings.delivery.express_multiplier" type="number" step="0.1" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Urgent Delivery Multiplier</label>
                <input v-model.number="settings.delivery.urgent_multiplier" type="number" step="0.1" class="form-control" />
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Maximum Weight (kg)</label>
                <input v-model.number="settings.delivery.max_weight" type="number" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Maximum Distance (km)</label>
                <input v-model.number="settings.delivery.max_distance" type="number" class="form-control" />
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary">Save Delivery Settings</button>
          </form>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h5>Notification Settings</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="saveNotificationSettings">
            <div class="mb-3">
              <h6>Email Notifications</h6>
              <div class="form-check">
                <input v-model="settings.notifications.email_new_order" class="form-check-input" type="checkbox" id="emailNewOrder">
                <label class="form-check-label" for="emailNewOrder">
                  New Order Notifications
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.notifications.email_status_update" class="form-check-input" type="checkbox" id="emailStatusUpdate">
                <label class="form-check-label" for="emailStatusUpdate">
                  Status Update Notifications
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.notifications.email_payment" class="form-check-input" type="checkbox" id="emailPayment">
                <label class="form-check-label" for="emailPayment">
                  Payment Notifications
                </label>
              </div>
            </div>
            
            <div class="mb-3">
              <h6>SMS Notifications</h6>
              <div class="form-check">
                <input v-model="settings.notifications.sms_new_order" class="form-check-input" type="checkbox" id="smsNewOrder">
                <label class="form-check-label" for="smsNewOrder">
                  New Order Notifications
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.notifications.sms_delivery" class="form-check-input" type="checkbox" id="smsDelivery">
                <label class="form-check-label" for="smsDelivery">
                  Delivery Status Notifications
                </label>
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary">Save Notification Settings</button>
          </form>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h5>Payment Settings</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="savePaymentSettings">
            <div class="mb-3">
              <h6>Accepted Payment Methods</h6>
              <div class="form-check">
                <input v-model="settings.payment.accept_cash" class="form-check-input" type="checkbox" id="acceptCash">
                <label class="form-check-label" for="acceptCash">
                  Cash on Delivery
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.payment.accept_card" class="form-check-input" type="checkbox" id="acceptCard">
                <label class="form-check-label" for="acceptCard">
                  Credit/Debit Cards
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.payment.accept_mobile" class="form-check-input" type="checkbox" id="acceptMobile">
                <label class="form-check-label" for="acceptMobile">
                  Mobile Money
                </label>
              </div>
              <div class="form-check">
                <input v-model="settings.payment.accept_bank" class="form-check-input" type="checkbox" id="acceptBank">
                <label class="form-check-label" for="acceptBank">
                  Bank Transfer
                </label>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">Default Currency</label>
                <select v-model="settings.payment.currency" class="form-select">
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="KES">KES (KSh)</option>
                  <option value="GBP">GBP (£)</option>
                </select>
              </div>
              <div class="col-md-6">
                <label class="form-label">Tax Rate (%)</label>
                <input v-model.number="settings.payment.tax_rate" type="number" step="0.01" class="form-control" />
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary">Save Payment Settings</button>
          </form>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card mb-4">
        <div class="card-header">
          <h5>System Status</h5>
        </div>
        <div class="card-body">
          <div class="mb-3">
            <div class="d-flex justify-content-between">
              <span>Database</span>
              <span class="badge bg-success">Connected</span>
            </div>
          </div>
          <div class="mb-3">
            <div class="d-flex justify-content-between">
              <span>API Status</span>
              <span class="badge bg-success">Online</span>
            </div>
          </div>
          <div class="mb-3">
            <div class="d-flex justify-content-between">
              <span>Email Service</span>
              <span class="badge bg-success">Active</span>
            </div>
          </div>
          <div class="mb-3">
            <div class="d-flex justify-content-between">
              <span>SMS Service</span>
              <span class="badge bg-warning">Limited</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h5>Quick Actions</h5>
        </div>
        <div class="card-body">
          <div class="d-grid gap-2">
            <button class="btn btn-outline-primary" @click="backupDatabase">
              💾 Backup Database
            </button>
            <button class="btn btn-outline-secondary" @click="clearCache">
              🗑️ Clear Cache
            </button>
            <button class="btn btn-outline-info" @click="sendTestEmail">
              📧 Send Test Email
            </button>
            <button class="btn btn-outline-warning" @click="regenerateApiKeys">
              🔑 Regenerate API Keys
            </button>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h5>System Information</h5>
        </div>
        <div class="card-body">
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Last Updated:</strong> Dec 12, 2025</p>
          <p><strong>Uptime:</strong> 15 days, 6 hours</p>
          <p><strong>Total Users:</strong> 127</p>
          <p><strong>Total Deliveries:</strong> 1,245</p>
          <p><strong>Active Drivers:</strong> 23</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const settings = ref({
  general: {
    company_name: 'PinDrop Delivery',
    support_email: 'support@pindrop.com',
    company_address: '123 Business Street, Nairobi, Kenya',
    phone: '+254712345678',
    business_hours: '8:00 AM - 6:00 PM'
  },
  delivery: {
    base_fee: 5.00,
    fee_per_kg: 2.50,
    express_multiplier: 1.5,
    urgent_multiplier: 2.0,
    max_weight: 50,
    max_distance: 100
  },
  notifications: {
    email_new_order: true,
    email_status_update: true,
    email_payment: false,
    sms_new_order: false,
    sms_delivery: true
  },
  payment: {
    accept_cash: true,
    accept_card: true,
    accept_mobile: true,
    accept_bank: false,
    currency: 'USD',
    tax_rate: 16.0
  }
})

const saveGeneralSettings = () => {
  console.log('Saving general settings:', settings.value.general)
  alert('General settings saved successfully!')
}

const saveDeliverySettings = () => {
  console.log('Saving delivery settings:', settings.value.delivery)
  alert('Delivery settings saved successfully!')
}

const saveNotificationSettings = () => {
  console.log('Saving notification settings:', settings.value.notifications)
  alert('Notification settings saved successfully!')
}

const savePaymentSettings = () => {
  console.log('Saving payment settings:', settings.value.payment)
  alert('Payment settings saved successfully!')
}

const backupDatabase = () => {
  alert('Database backup initiated. You will be notified when complete.')
}

const clearCache = () => {
  alert('Cache cleared successfully!')
}

const sendTestEmail = () => {
  alert('Test email sent to support@pindrop.com')
}

const regenerateApiKeys = () => {
  if (confirm('Are you sure you want to regenerate API keys? This will invalidate all existing keys.')) {
    alert('API keys regenerated successfully!')
  }
}

onMounted(() => {
  console.log('Loading settings...')
  // In a real app, you would fetch settings from API
})
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

h5 {
  color: #495057;
  margin-bottom: 0;
}

h6 {
  color: #6c757d;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.badge {
  font-size: 0.75em;
}

.form-check-label {
  margin-bottom: 0.5rem;
}

.btn-outline-primary,
.btn-outline-secondary,
.btn-outline-info,
.btn-outline-warning {
  border-width: 1px;
}
</style>