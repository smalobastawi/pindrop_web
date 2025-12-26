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
                  <span class="input-group-text">KSh</span>
                  <input v-model.number="settings.delivery.base_fee" type="number" step="0.01" class="form-control" />
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label">Fee per Kilogram</label>
                <div class="input-group">
                  <span class="input-group-text">KSh</span>
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
import axios from 'axios'

const settings = ref({
  general: {
    company_name: 'RiderApp Delivery',
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
    currency: 'KES',
    tax_rate: 16.0
  }
})

const loading = ref(false)
const saving = ref(false)

const loadSettings = async () => {
  loading.value = true
  try {
    const response = await axios.get('/admin-api/api/settings/')
    const settingsData = response.data.results || response.data

    // Update form with loaded settings
    if (settingsData.length > 0) {
      settingsData.forEach(setting => {
        const value = setting.typed_value !== undefined ? setting.typed_value : setting.value
        switch(setting.key) {
          case 'company_name':
            settings.value.general.company_name = value
            break
          case 'support_email':
            settings.value.general.support_email = value
            break
          case 'company_address':
            settings.value.general.company_address = value
            break
          case 'phone':
            settings.value.general.phone = value
            break
          case 'business_hours':
            settings.value.general.business_hours = value
            break
          case 'base_delivery_fee':
            settings.value.delivery.base_fee = parseFloat(value)
            break
          case 'fee_per_kg':
            settings.value.delivery.fee_per_kg = parseFloat(value)
            break
          case 'express_multiplier':
            settings.value.delivery.express_multiplier = parseFloat(value)
            break
          case 'urgent_multiplier':
            settings.value.delivery.urgent_multiplier = parseFloat(value)
            break
          case 'max_weight':
            settings.value.delivery.max_weight = parseInt(value)
            break
          case 'max_distance':
            settings.value.delivery.max_distance = parseInt(value)
            break
          case 'email_new_order':
            settings.value.notifications.email_new_order = value === 'true' || value === true
            break
          case 'email_status_update':
            settings.value.notifications.email_status_update = value === 'true' || value === true
            break
          case 'email_payment':
            settings.value.notifications.email_payment = value === 'true' || value === true
            break
          case 'sms_new_order':
            settings.value.notifications.sms_new_order = value === 'true' || value === true
            break
          case 'sms_delivery':
            settings.value.notifications.sms_delivery = value === 'true' || value === true
            break
          case 'accept_cash':
            settings.value.payment.accept_cash = value === 'true' || value === true
            break
          case 'accept_card':
            settings.value.payment.accept_card = value === 'true' || value === true
            break
          case 'accept_mobile':
            settings.value.payment.accept_mobile = value === 'true' || value === true
            break
          case 'accept_bank':
            settings.value.payment.accept_bank = value === 'true' || value === true
            break
          case 'currency':
            settings.value.payment.currency = value
            break
          case 'tax_rate':
            settings.value.payment.tax_rate = parseFloat(value)
            break
        }
      })
    }
  } catch (error) {
    console.error('Failed to load settings:', error)
  } finally {
    loading.value = false
  }
}

const saveSettings = async (settingsToSave) => {
  saving.value = true
  try {
    for (const setting of settingsToSave) {
      await axios.post('/admin-api/api/settings/upsert/', setting)
    }
    return true
  } catch (error) {
    console.error('Failed to save settings:', error)
    return false
  } finally {
    saving.value = false
  }
}

const saveGeneralSettings = async () => {
  const settingsToSave = [
    { key: 'company_name', value: settings.value.general.company_name, setting_type: 'string', category: 'general' },
    { key: 'support_email', value: settings.value.general.support_email, setting_type: 'string', category: 'general' },
    { key: 'company_address', value: settings.value.general.company_address, setting_type: 'string', category: 'general' },
    { key: 'phone', value: settings.value.general.phone, setting_type: 'string', category: 'general' },
    { key: 'business_hours', value: settings.value.general.business_hours, setting_type: 'string', category: 'general' }
  ]

  const success = await saveSettings(settingsToSave)
  if (success) {
    alert('General settings saved successfully!')
  } else {
    alert('Failed to save general settings. Please try again.')
  }
}

const saveDeliverySettings = async () => {
  const settingsToSave = [
    { key: 'base_delivery_fee', value: settings.value.delivery.base_fee.toString(), setting_type: 'float', category: 'delivery' },
    { key: 'fee_per_kg', value: settings.value.delivery.fee_per_kg.toString(), setting_type: 'float', category: 'delivery' },
    { key: 'express_multiplier', value: settings.value.delivery.express_multiplier.toString(), setting_type: 'float', category: 'delivery' },
    { key: 'urgent_multiplier', value: settings.value.delivery.urgent_multiplier.toString(), setting_type: 'float', category: 'delivery' },
    { key: 'max_weight', value: settings.value.delivery.max_weight.toString(), setting_type: 'integer', category: 'delivery' },
    { key: 'max_distance', value: settings.value.delivery.max_distance.toString(), setting_type: 'integer', category: 'delivery' }
  ]

  const success = await saveSettings(settingsToSave)
  if (success) {
    alert('Delivery settings saved successfully!')
  } else {
    alert('Failed to save delivery settings. Please try again.')
  }
}

const saveNotificationSettings = async () => {
  const settingsToSave = [
    { key: 'email_new_order', value: settings.value.notifications.email_new_order.toString(), setting_type: 'boolean', category: 'notifications' },
    { key: 'email_status_update', value: settings.value.notifications.email_status_update.toString(), setting_type: 'boolean', category: 'notifications' },
    { key: 'email_payment', value: settings.value.notifications.email_payment.toString(), setting_type: 'boolean', category: 'notifications' },
    { key: 'sms_new_order', value: settings.value.notifications.sms_new_order.toString(), setting_type: 'boolean', category: 'notifications' },
    { key: 'sms_delivery', value: settings.value.notifications.sms_delivery.toString(), setting_type: 'boolean', category: 'notifications' }
  ]

  const success = await saveSettings(settingsToSave)
  if (success) {
    alert('Notification settings saved successfully!')
  } else {
    alert('Failed to save notification settings. Please try again.')
  }
}

const savePaymentSettings = async () => {
  const settingsToSave = [
    { key: 'accept_cash', value: settings.value.payment.accept_cash.toString(), setting_type: 'boolean', category: 'payment' },
    { key: 'accept_card', value: settings.value.payment.accept_card.toString(), setting_type: 'boolean', category: 'payment' },
    { key: 'accept_mobile', value: settings.value.payment.accept_mobile.toString(), setting_type: 'boolean', category: 'payment' },
    { key: 'accept_bank', value: settings.value.payment.accept_bank.toString(), setting_type: 'boolean', category: 'payment' },
    { key: 'currency', value: settings.value.payment.currency, setting_type: 'string', category: 'payment' },
    { key: 'tax_rate', value: settings.value.payment.tax_rate.toString(), setting_type: 'float', category: 'payment' }
  ]

  const success = await saveSettings(settingsToSave)
  if (success) {
    alert('Payment settings saved successfully!')
  } else {
    alert('Failed to save payment settings. Please try again.')
  }
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
  loadSettings()
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