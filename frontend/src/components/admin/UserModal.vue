<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>{{ isEdit ? 'Edit User' : 'Add New User' }}</h3>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-section">
            <h4>User Information</h4>
            
            <div class="form-group">
              <label for="username">Username *</label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                required
                :disabled="isEdit"
                placeholder="Enter username"
              >
            </div>

            <div class="form-group">
              <label for="email">Email Address *</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                placeholder="Enter email address"
              >
            </div>

            <div class="form-group" v-if="!isEdit">
              <label for="password">Password *</label>
              <input
                id="password"
                v-model="form.password"
                type="password"
                required
                placeholder="Enter password"
              >
            </div>

            <div class="form-group" v-if="!isEdit">
              <label for="password_confirm">Confirm Password *</label>
              <input
                id="password_confirm"
                v-model="form.password_confirm"
                type="password"
                required
                placeholder="Confirm password"
              >
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="first_name">First Name</label>
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  placeholder="Enter first name"
                >
              </div>

              <div class="form-group">
                <label for="last_name">Last Name</label>
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  placeholder="Enter last name"
                >
              </div>
            </div>
          </div>

          <div class="form-section">
            <h4>Admin Profile</h4>
            
            <div class="form-group">
              <label for="role">Role *</label>
              <select id="role" v-model="form.role" required>
                <option value="">Select a role</option>
                <option value="super_admin">Super Administrator</option>
                <option value="admin">Administrator</option>
                <option value="manager">Manager</option>
                <option value="operator">Operator</option>
                <option value="viewer">Viewer</option>
              </select>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  placeholder="Enter phone number"
                >
              </div>

              <div class="form-group">
                <label for="employee_id">Employee ID</label>
                <input
                  id="employee_id"
                  v-model="form.employee_id"
                  type="text"
                  placeholder="Enter employee ID"
                >
              </div>
            </div>

            <div class="form-group">
              <label for="department">Department</label>
              <input
                id="department"
                v-model="form.department"
                type="text"
                placeholder="Enter department"
              >
            </div>

            <div class="form-group">
              <label class="checkbox-wrapper">
                <input
                  v-model="form.is_active"
                  type="checkbox"
                >
                <span class="checkmark"></span>
                Active User
              </label>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" @click="$emit('close')" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="loading-spinner"></span>
              {{ saving ? 'Saving...' : (isEdit ? 'Update User' : 'Add User') }}
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
  name: 'UserModal',
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    // Reactive state
    const saving = ref(false)
    
    const form = ref({
      username: '',
      email: '',
      password: '',
      password_confirm: '',
      first_name: '',
      last_name: '',
      role: '',
      phone: '',
      employee_id: '',
      department: '',
      is_active: true
    })
    
    // Computed properties
    const isEdit = computed(() => !!props.user)
    
    // Methods
    const resetForm = () => {
      form.value = {
        username: '',
        email: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
        role: '',
        phone: '',
        employee_id: '',
        department: '',
        is_active: true
      }
    }
    
    const populateForm = (user) => {
      form.value = {
        username: user.user?.username || '',
        email: user.user?.email || '',
        password: '',
        password_confirm: '',
        first_name: user.user?.first_name || '',
        last_name: user.user?.last_name || '',
        role: user.role || '',
        phone: user.phone || '',
        employee_id: user.employee_id || '',
        department: user.department || '',
        is_active: user.is_active !== undefined ? user.is_active : true
      }
    }
    
    const validateForm = () => {
      if (!form.value.username.trim()) {
        alert('Username is required')
        return false
      }
      
      if (!form.value.email.trim()) {
        alert('Email is required')
        return false
      }
      
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
        alert('Please enter a valid email address')
        return false
      }
      
      if (!isEdit.value) {
        if (!form.value.password) {
          alert('Password is required')
          return false
        }
        
        if (form.value.password !== form.value.password_confirm) {
          alert('Passwords do not match')
          return false
        }
      }
      
      if (!form.value.role) {
        alert('Role is required')
        return false
      }
      
      return true
    }
    
    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }
      
      saving.value = true
      
      try {
        // Prepare the data for submission
        const submitData = { ...form.value }
        
        // Remove password confirmation and empty password for edits
        if (isEdit.value) {
          delete submitData.password_confirm
          if (!submitData.password) {
            delete submitData.password
          }
        }
        
        emit('save', submitData)
        
      } catch (error) {
        console.error('Form submission error:', error)
      } finally {
        saving.value = false
      }
    }
    
    // Watch for user prop changes
    watch(() => props.user, (newUser) => {
      if (newUser) {
        populateForm(newUser)
      } else {
        resetForm()
      }
    }, { immediate: true })
    
    // Lifecycle
    onMounted(() => {
      if (props.user) {
        populateForm(props.user)
      }
    })
    
    return {
      form,
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
  max-width: 600px;
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
.form-section {
  margin-bottom: 2rem;
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
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
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