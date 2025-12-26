<template>
  <AdminLayout>
    <div class="admin-settings">
      <!-- Page Header -->
      <div class="page-header">
        <h1>System Settings</h1>
        <p>Configure system-wide settings and preferences</p>
      </div>

      <!-- Settings Categories -->
      <div class="settings-container">
        <div class="settings-sidebar">
          <nav class="settings-nav">
            <button 
              v-for="category in settingCategories"
              :key="category.key"
              @click="activeCategory = category.key"
              :class="['nav-item', { active: activeCategory === category.key }]"
            >
              <i :class="category.icon"></i>
              <span>{{ category.name }}</span>
            </button>
          </nav>
        </div>

        <div class="settings-content">
          <!-- General Settings -->
          <div v-if="activeCategory === 'general'" class="settings-section">
            <div class="section-header">
              <h2>General Settings</h2>
              <p>Basic system configuration</p>
            </div>

            <div class="settings-grid">
              <div class="setting-item">
                <label for="site_name">Site Name</label>
                <input 
                  id="site_name"
                  v-model="settings.site_name"
                  type="text"
                  placeholder="Enter site name"
                >
                <small>The name of your delivery service</small>
              </div>

              <div class="setting-item">
                <label for="site_description">Site Description</label>
                <textarea 
                  id="site_description"
                  v-model="settings.site_description"
                  rows="3"
                  placeholder="Enter site description"
                ></textarea>
                <small>Brief description of your service</small>
              </div>

              <div class="setting-item">
                <label for="contact_email">Contact Email</label>
                <input 
                  id="contact_email"
                  v-model="settings.contact_email"
                  type="email"
                  placeholder="Enter contact email"
                >
                <small>Primary contact email for customer support</small>
              </div>

              <div class="setting-item">
                <label for="contact_phone">Contact Phone</label>
                <input 
                  id="contact_phone"
                  v-model="settings.contact_phone"
                  type="tel"
                  placeholder="Enter contact phone"
                >
                <small>Primary contact phone number</small>
              </div>

              <div class="setting-item">
                <label for="timezone">Timezone</label>
                <select id="timezone" v-model="settings.timezone">
                  <option value="UTC">UTC</option>
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                  <option value="Europe/London">London</option>
                  <option value="Europe/Paris">Paris</option>
                </select>
                <small>System timezone for date/time operations</small>
              </div>

              <div class="setting-item">
                <label for="date_format">Date Format</label>
                <select id="date_format" v-model="settings.date_format">
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
                <small>Default date format for displaying dates</small>
              </div>
            </div>
          </div>

          <!-- Delivery Settings -->
          <div v-if="activeCategory === 'delivery'" class="settings-section">
            <div class="section-header">
              <h2>Delivery Settings</h2>
              <p>Configure delivery-related options</p>
            </div>

            <div class="settings-grid">
              <div class="setting-item">
                <label for="base_delivery_fee">Base Delivery Fee</label>
                <div class="input-group">
                  <span class="input-prefix">KSh</span>
                  <input
                    id="base_delivery_fee"
                    v-model="settings.base_delivery_fee"
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="0.00"
                  >
                </div>
                <small>Base fee for all deliveries</small>
              </div>

              <div class="setting-item">
                <label for="fee_per_km">Fee Per Kilometer</label>
                <div class="input-group">
                  <span class="input-prefix">KSh</span>
                  <input
                    id="fee_per_km"
                    v-model="settings.fee_per_km"
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="0.00"
                  >
                </div>
                <small>Additional fee per kilometer</small>
              </div>

              <div class="setting-item">
                <label for="max_delivery_distance">Max Delivery Distance</label>
                <div class="input-group">
                  <input 
                    id="max_delivery_distance"
                    v-model="settings.max_delivery_distance"
                    type="number"
                    min="1"
                    placeholder="50"
                  >
                  <span class="input-suffix">km</span>
                </div>
                <small>Maximum distance for deliveries</small>
              </div>

              <div class="setting-item">
                <label for="default_delivery_time">Default Delivery Time</label>
                <div class="input-group">
                  <input 
                    id="default_delivery_time"
                    v-model="settings.default_delivery_time"
                    type="number"
                    min="1"
                    placeholder="2"
                  >
                  <span class="input-suffix">hours</span>
                </div>
                <small>Default estimated delivery time</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.allow_scheduled_deliveries"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Allow Scheduled Deliveries
                </label>
                <small>Enable customers to schedule future deliveries</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.require_signature"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Require Signature on Delivery
                </label>
                <small>Require customer signature for delivery confirmation</small>
              </div>
            </div>
          </div>

          <!-- Notification Settings -->
          <div v-if="activeCategory === 'notifications'" class="settings-section">
            <div class="section-header">
              <h2>Notification Settings</h2>
              <p>Configure email and SMS notifications</p>
            </div>

            <div class="settings-grid">
              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.email_notifications_enabled"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Enable Email Notifications
                </label>
                <small>Send email notifications to customers</small>
              </div>

              <div class="setting-item">
                <label for="smtp_host">SMTP Host</label>
                <input 
                  id="smtp_host"
                  v-model="settings.smtp_host"
                  type="text"
                  placeholder="smtp.gmail.com"
                >
                <small>SMTP server for sending emails</small>
              </div>

              <div class="setting-item">
                <label for="smtp_port">SMTP Port</label>
                <input 
                  id="smtp_port"
                  v-model="settings.smtp_port"
                  type="number"
                  placeholder="587"
                >
                <small>SMTP server port</small>
              </div>

              <div class="setting-item">
                <label for="smtp_username">SMTP Username</label>
                <input 
                  id="smtp_username"
                  v-model="settings.smtp_username"
                  type="text"
                  placeholder="your-email@gmail.com"
                >
                <small>SMTP authentication username</small>
              </div>

              <div class="setting-item">
                <label for="smtp_password">SMTP Password</label>
                <input 
                  id="smtp_password"
                  v-model="settings.smtp_password"
                  type="password"
                  placeholder="Enter SMTP password"
                >
                <small>SMTP authentication password</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.sms_notifications_enabled"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Enable SMS Notifications
                </label>
                <small>Send SMS notifications to customers</small>
              </div>
            </div>
          </div>

          <!-- Security Settings -->
          <div v-if="activeCategory === 'security'" class="settings-section">
            <div class="section-header">
              <h2>Security Settings</h2>
              <p>Configure security and access controls</p>
            </div>

            <div class="settings-grid">
              <div class="setting-item">
                <label for="session_timeout">Session Timeout</label>
                <div class="input-group">
                  <input 
                    id="session_timeout"
                    v-model="settings.session_timeout"
                    type="number"
                    min="5"
                    placeholder="60"
                  >
                  <span class="input-suffix">minutes</span>
                </div>
                <small>Automatically log out inactive users</small>
              </div>

              <div class="setting-item">
                <label for="max_login_attempts">Max Login Attempts</label>
                <input 
                  id="max_login_attempts"
                  v-model="settings.max_login_attempts"
                  type="number"
                  min="3"
                  placeholder="5"
                >
                <small>Maximum failed login attempts before account lockout</small>
              </div>

              <div class="setting-item">
                <label for="lockout_duration">Account Lockout Duration</label>
                <div class="input-group">
                  <input 
                    id="lockout_duration"
                    v-model="settings.lockout_duration"
                    type="number"
                    min="5"
                    placeholder="30"
                  >
                  <span class="input-suffix">minutes</span>
                </div>
                <small>Duration to lock account after max failed attempts</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.require_password_change"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Require Password Change Every 90 Days
                </label>
                <small>Force users to change password regularly</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.enable_two_factor"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Enable Two-Factor Authentication
                </label>
                <small>Require 2FA for admin users</small>
              </div>

              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.log_admin_actions"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Log Admin Actions
                </label>
                <small>Keep audit log of all admin actions</small>
              </div>
            </div>
          </div>

          <!-- Backup Settings -->
          <div v-if="activeCategory === 'backup'" class="settings-section">
            <div class="section-header">
              <h2>Backup Settings</h2>
              <p>Configure automatic backup options</p>
            </div>

            <div class="settings-grid">
              <div class="setting-item">
                <label class="checkbox-wrapper">
                  <input 
                    v-model="settings.auto_backup_enabled"
                    type="checkbox"
                  >
                  <span class="checkmark"></span>
                  Enable Automatic Backups
                </label>
                <small>Automatically create backups on schedule</small>
              </div>

              <div class="setting-item">
                <label for="backup_frequency">Backup Frequency</label>
                <select id="backup_frequency" v-model="settings.backup_frequency">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
                <small>How often to create backups</small>
              </div>

              <div class="setting-item">
                <label for="backup_retention">Backup Retention</label>
                <div class="input-group">
                  <input 
                    id="backup_retention"
                    v-model="settings.backup_retention"
                    type="number"
                    min="1"
                    placeholder="30"
                  >
                  <span class="input-suffix">days</span>
                </div>
                <small>How long to keep backup files</small>
              </div>

              <div class="setting-item">
                <label for="backup_location">Backup Storage Location</label>
                <input 
                  id="backup_location"
                  v-model="settings.backup_location"
                  type="text"
                  placeholder="/backups/"
                >
                <small>Local path to store backup files</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="settings-footer">
        <button 
          @click="saveSettings"
          class="btn btn-primary"
          :disabled="saving"
        >
          <span v-if="saving" class="loading-spinner"></span>
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
        <button 
          @click="resetToDefaults"
          class="btn btn-secondary"
          :disabled="saving"
        >
          Reset to Defaults
        </button>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import axios from 'axios'

export default {
  name: 'AdminSettings',
  components: {
    AdminLayout
  },
  setup() {
    // Reactive state
    const activeCategory = ref('general')
    const saving = ref(false)
    
    const settings = ref({
      // General
      site_name: 'RiderApp Delivery',
      site_description: 'Fast and reliable delivery service',
      contact_email: 'support@pindrop.com',
      contact_phone: '+1-555-0123',
      timezone: 'UTC',
      date_format: 'MM/DD/YYYY',
      
      // Delivery
      base_delivery_fee: '5.00',
      fee_per_km: '0.50',
      max_delivery_distance: '50',
      default_delivery_time: '2',
      allow_scheduled_deliveries: true,
      require_signature: false,
      
      // Notifications
      email_notifications_enabled: true,
      smtp_host: 'smtp.gmail.com',
      smtp_port: '587',
      smtp_username: '',
      smtp_password: '',
      sms_notifications_enabled: false,
      
      // Security
      session_timeout: '60',
      max_login_attempts: '5',
      lockout_duration: '30',
      require_password_change: false,
      enable_two_factor: false,
      log_admin_actions: true,
      
      // Backup
      auto_backup_enabled: false,
      backup_frequency: 'daily',
      backup_retention: '30',
      backup_location: '/backups/'
    })
    
    const settingCategories = [
      { key: 'general', name: 'General', icon: 'icon-settings' },
      { key: 'delivery', name: 'Delivery', icon: 'icon-truck' },
      { key: 'notifications', name: 'Notifications', icon: 'icon-mail' },
      { key: 'security', name: 'Security', icon: 'icon-shield' },
      { key: 'backup', name: 'Backup', icon: 'icon-database' }
    ]
    
    // Methods
    const loadSettings = async () => {
      try {
        const response = await axios.get('/admin-api/api/settings/')
        const settingsData = response.data.results || response.data
        
        // Update form with loaded settings
        if (settingsData.length > 0) {
          settingsData.forEach(setting => {
            if (settings.value.hasOwnProperty(setting.key)) {
              settings.value[setting.key] = setting.value
            }
          })
        }
      } catch (error) {
        console.error('Failed to load settings:', error)
      }
    }
    
    const saveSettings = async () => {
      saving.value = true
      try {
        // Prepare settings for saving
        const settingsToSave = []
        
        Object.keys(settings.value).forEach(key => {
          settingsToSave.push({
            key: key,
            value: settings.value[key].toString(),
            setting_type: getSettingType(settings.value[key]),
            category: getSettingCategory(key)
          })
        })
        
        // Save settings in batches
        for (const setting of settingsToSave) {
          try {
            await axios.post('/admin-api/api/settings/', setting)
          } catch (error) {
            // If it exists, update it
            if (error.response?.status === 400) {
              await axios.put(`/admin-api/api/settings/${setting.key}/`, setting)
            } else {
              throw error
            }
          }
        }
        
        alert('Settings saved successfully!')
      } catch (error) {
        console.error('Failed to save settings:', error)
        alert('Failed to save settings. Please try again.')
      } finally {
        saving.value = false
      }
    }
    
    const resetToDefaults = () => {
      if (!confirm('Are you sure you want to reset all settings to default values?')) {
        return
      }
      
      // Reset to default values
      settings.value = {
        site_name: 'RiderApp Delivery',
        site_description: 'Fast and reliable delivery service',
        contact_email: 'support@pindrop.com',
        contact_phone: '+1-555-0123',
        timezone: 'UTC',
        date_format: 'MM/DD/YYYY',
        base_delivery_fee: '5.00',
        fee_per_km: '0.50',
        max_delivery_distance: '50',
        default_delivery_time: '2',
        allow_scheduled_deliveries: true,
        require_signature: false,
        email_notifications_enabled: true,
        smtp_host: 'smtp.gmail.com',
        smtp_port: '587',
        smtp_username: '',
        smtp_password: '',
        sms_notifications_enabled: false,
        session_timeout: '60',
        max_login_attempts: '5',
        lockout_duration: '30',
        require_password_change: false,
        enable_two_factor: false,
        log_admin_actions: true,
        auto_backup_enabled: false,
        backup_frequency: 'daily',
        backup_retention: '30',
        backup_location: '/backups/'
      }
    }
    
    const getSettingType = (value) => {
      if (typeof value === 'boolean') return 'boolean'
      if (!isNaN(Number(value))) return 'float'
      return 'string'
    }
    
    const getSettingCategory = (key) => {
      if (['site_name', 'site_description', 'contact_email', 'contact_phone', 'timezone', 'date_format'].includes(key)) {
        return 'general'
      }
      if (['base_delivery_fee', 'fee_per_km', 'max_delivery_distance', 'default_delivery_time', 'allow_scheduled_deliveries', 'require_signature'].includes(key)) {
        return 'delivery'
      }
      if (['email_notifications_enabled', 'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'sms_notifications_enabled'].includes(key)) {
        return 'notifications'
      }
      if (['session_timeout', 'max_login_attempts', 'lockout_duration', 'require_password_change', 'enable_two_factor', 'log_admin_actions'].includes(key)) {
        return 'security'
      }
      if (['auto_backup_enabled', 'backup_frequency', 'backup_retention', 'backup_location'].includes(key)) {
        return 'backup'
      }
      return 'general'
    }
    
    // Lifecycle
    onMounted(() => {
      loadSettings()
    })
    
    return {
      activeCategory,
      settings,
      settingCategories,
      saving,
      saveSettings,
      resetToDefaults
    }
  }
}
</script>

<style scoped>
.admin-settings {
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
  margin: 0;
}

/* Settings Container */
.settings-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

/* Settings Sidebar */
.settings-sidebar {
  background: #f8f9fa;
  border-right: 1px solid #dee2e6;
}

.settings-nav {
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  color: #6c757d;
  font-size: 0.9rem;
}

.nav-item:hover {
  background: #e9ecef;
  color: #495057;
}

.nav-item.active {
  background: #007bff;
  color: white;
}

.nav-item i {
  width: 16px;
  text-align: center;
}

/* Settings Content */
.settings-content {
  padding: 2rem;
  max-height: 600px;
  overflow-y: auto;
}

.settings-section {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: #6c757d;
  margin: 0;
}

.settings-grid {
  display: grid;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.setting-item label {
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.setting-item input,
.setting-item select,
.setting-item textarea {
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.setting-item input:focus,
.setting-item select:focus,
.setting-item textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.setting-item small {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Input Groups */
.input-group {
  display: flex;
  align-items: center;
}

.input-prefix,
.input-suffix {
  background: #f8f9fa;
  border: 1px solid #ced4da;
  padding: 0.75rem;
  font-size: 1rem;
  color: #495057;
}

.input-prefix {
  border-right: none;
  border-radius: 0.375rem 0 0 0.375rem;
}

.input-suffix {
  border-left: none;
  border-radius: 0 0.375rem 0.375rem 0;
}

.input-group input {
  border-radius: 0;
  flex: 1;
}

.input-group input:first-child {
  border-radius: 0.375rem 0 0 0.375rem;
}

.input-group input:last-child {
  border-radius: 0 0.375rem 0.375rem 0;
}

/* Checkbox */
.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #495057;
}

.checkbox-wrapper input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #ced4da;
  border-radius: 0.25rem;
  position: relative;
  transition: all 0.2s;
  flex-shrink: 0;
}

.checkbox-wrapper input[type="checkbox"]:checked + .checkmark {
  background: #007bff;
  border-color: #007bff;
}

.checkbox-wrapper input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
}

/* Settings Footer */
.settings-footer {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
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
  font-weight: 500;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
  }
  
  .settings-sidebar {
    border-right: none;
    border-bottom: 1px solid #dee2e6;
  }
  
  .settings-nav {
    display: flex;
    overflow-x: auto;
    padding: 1rem;
  }
  
  .nav-item {
    white-space: nowrap;
    padding: 0.75rem 1rem;
  }
  
  .settings-content {
    padding: 1rem;
    max-height: none;
  }
  
  .settings-footer {
    flex-direction: column;
  }
  
  .settings-footer .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>