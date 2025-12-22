<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>{{ isEdit ? 'Edit Customer' : 'Add New Customer' }}</h3>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-grid">
            <!-- Basic Information -->
            <div class="form-section">
              <h4>Basic Information</h4>
              
              <div class="form-group">
                <label for="name">Full Name *</label>
                <input
                  id="name"
                  v-model="form.name"
                  type="text"
                  required
                  :class="{ 'error': errors.name }"
                  placeholder="Enter customer's full name"
                >
                <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
              </div>

              <div class="form-group">
                <label for="email">Email Address *</label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  required
                  :class="{ 'error': errors.email }"
                  placeholder="Enter email address"
                >
                <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
              </div>

              <div class="form-group">
                <label for="phone">Phone Number *</label>
                <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  required
                  :class="{ 'error': errors.phone }"
                  placeholder="Enter phone number"
                >
                <div v-if="errors.phone" class="error-text">{{ errors.phone }}</div>
              </div>
            </div>

            <!-- Address Information -->
            <div class="form-section">
              <h4>Address Information</h4>
              
              <div class="form-group">
                <label for="address">Street Address *</label>
                <textarea
                  id="address"
                  v-model="form.address"
                  required
                  :class="{ 'error': errors.address }"
                  rows="3"
                  placeholder="Enter street address"
                ></textarea>
                <div v-if="errors.address" class="error-text">{{ errors.address }}</div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="city">City</label>
                  <input
                    id="city"
                    v-model="form.city"
                    type="text"
                    placeholder="Enter city"
                  >
                </div>

                <div class="form-group">
                  <label for="state">State/Province</label>
                  <input
                    id="state"
                    v-model="form.state"
                    type="text"
                    placeholder="Enter state"
                  >
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="postal_code">Postal Code</label>
                  <input
                    id="postal_code"
                    v-model="form.postal_code"
                    type="text"
                    placeholder="Enter postal code"
                  >
                </div>

                <div class="form-group">
                  <label for="country">Country</label>
                  <input
                    id="country"
                    v-model="form.country"
                    type="text"
                    placeholder="Enter country"
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Information -->
          <div class="form-section">
            <h4>Additional Information</h4>
            
            <div class="form-row">
              <div class="form-group">
                <label for="date_of_birth">Date of Birth</label>
                <input
                  id="date_of_birth"
                  v-model="form.date_of_birth"
                  type="date"
                >
              </div>

              <div class="form-group">
                <label for="customer_type">Customer Type</label>
                <select id="customer_type" v-model="form.customer_type">
                  <option value="individual">Individual</option>
                  <option value="business">Business</option>
                  <option value="vip">VIP</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="notes">Notes</label>
              <textarea
                id="notes"
                v-model="form.notes"
                rows="3"
                placeholder="Additional notes about the customer"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="checkbox-wrapper">
                <input
                  v-model="form.is_active"
                  type="checkbox"
                >
                <span class="checkmark"></span>
                Active Customer
              </label>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" @click="$emit('close')" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="loading-spinner"></span>
              {{ saving ? 'Saving...' : (isEdit ? 'Update Customer' : 'Add Customer') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'

export default {
  name: 'CustomerModal',
  props: {
    customer: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    // Reactive state
    const saving = ref(false)
    const errors = ref({})
    
    const form = ref({
      name: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      state: '',
      postal_code: '',
      country: '',
      date_of_birth: '',
      customer_type: 'individual',
      notes: '',
      is_active: true
    })
    
    // Computed properties
    const isEdit = computed(() => !!props.customer)
    
    // Methods
    const resetForm = () => {
      form.value = {
        name: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        postal_code: '',
        country: '',
        date_of_birth: '',
        customer_type: 'individual',
        notes: '',
        is_active: true
      }
      errors.value = {}
    }
    
    const populateForm = (customer) => {
      form.value = {
        name: customer.name || '',
        email: customer.email || '',
        phone: customer.phone || '',
        address: customer.address || '',
        city: customer.city || '',
        state: customer.state || '',
        postal_code: customer.postal_code || '',
        country: customer.country || '',
        date_of_birth: customer.date_of_birth || '',
        customer_type: customer.customer_type || 'individual',
        notes: customer.notes || '',
        is_active: customer.is_active !== undefined ? customer.is_active : true
      }
    }
    
    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.name.trim()) {
        errors.value.name = 'Name is required'
      }
      
      if (!form.value.email.trim()) {
        errors.value.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }
      
      if (!form.value.phone.trim()) {
        errors.value.phone = 'Phone number is required'
      }
      
      if (!form.value.address.trim()) {
        errors.value.address = 'Address is required'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }
      
      saving.value = true
      
      try {
        // Prepare the data for submission
        const submitData = { ...form.value }
        
        // Format date if present
        if (submitData.date_of_birth) {
          submitData.date_of_birth = new Date(submitData.date_of_birth).toISOString().split('T')[0]
        }
        
        emit('save', submitData)
        
      } catch (error) {
        console.error('Form submission error:', error)
      } finally {
        saving.value = false
      }
    }
    
    // Watch for customer prop changes
    watch(() => props.customer, (newCustomer) => {
      if (newCustomer) {
        populateForm(newCustomer)
      } else {
        resetForm()
      }
    }, { immediate: true })
    
    // Lifecycle
    onMounted(() => {
      if (props.customer) {
        populateForm(props.customer)
      }
    })
    
    return {
      form,
      errors,
      saving,
      isEdit,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
  max-width: 800px;
  width: 100%;
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
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

.modal-body {
  padding: 1.5rem;
}

/* Form Layout */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.375rem;
  border: 1px solid #e9ecef;
}

.form-section h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #495057;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input.error,
.form-group select.error,
.form-group textarea.error {
  border-color: #dc3545;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.error-text {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
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

/* Modal Actions */
.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #dee2e6;
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
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-section {
    padding: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>