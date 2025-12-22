<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <h1>PinDrop Admin</h1>
          <p>Administrator Portal</p>
        </div>
      </div>

      <div class="login-form-container">
        <form @submit.prevent="handleLogin" class="login-form">
          <h2>Sign In</h2>
          <p class="login-subtitle">Enter your credentials to access the admin panel</p>

          <div v-if="error" class="error-message">
            <i class="icon-alert-circle"></i>
            <span>{{ error }}</span>
          </div>

          <div class="form-group">
            <label for="username">Username or Email</label>
            <div class="input-wrapper">
              <i class="icon-user"></i>
              <input
                id="username"
                v-model="form.username"
                type="text"
                placeholder="Enter your username or email"
                required
                :disabled="loading"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-wrapper">
              <i class="icon-lock"></i>
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
                required
                :disabled="loading"
              >
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                :disabled="loading"
              >
                <i :class="showPassword ? 'icon-eye-off' : 'icon-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-wrapper">
              <input
                v-model="form.rememberMe"
                type="checkbox"
                :disabled="loading"
              >
              <span class="checkmark"></span>
              Remember me
            </label>
            <a href="#" class="forgot-password">Forgot password?</a>
          </div>

          <button
            type="submit"
            class="login-button"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading" class="loading-spinner"></span>
            <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>
          </button>

          <div class="login-footer">
            <p>Need access? <a href="mailto:admin@pindrop.com">Contact administrator</a></p>
          </div>
        </form>
      </div>

      <div class="login-background">
        <div class="background-pattern"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '@/stores/adminAuth'

export default {
  name: 'AdminLogin',
  setup() {
    const router = useRouter()
    const adminAuthStore = useAdminAuthStore()
    
    // Reactive state
    const form = ref({
      username: '',
      password: '',
      rememberMe: false
    })
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    // Computed properties
    const isFormValid = computed(() => {
      return form.value.username.trim() && form.value.password.trim()
    })
    
    // Methods
    const handleLogin = async () => {
      if (!isFormValid.value) return
      
      loading.value = true
      error.value = ''
      
      try {
        await adminAuthStore.login({
          username: form.value.username,
          password: form.value.password
        })
        
        // Redirect to admin dashboard
        router.push('/admin')
        
      } catch (err) {
        error.value = adminAuthStore.error || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    const handleKeyPress = (event) => {
      if (event.key === 'Enter' && isFormValid.value) {
        handleLogin()
      }
    }
    
    // Lifecycle
    onMounted(() => {
      // Clear any existing admin auth state
      adminAuthStore.logout()
      
      // Add keypress listener
      document.addEventListener('keypress', handleKeyPress)
      
      // Focus on username field
      const usernameField = document.getElementById('username')
      if (usernameField) {
        usernameField.focus()
      }
      
      // Cleanup on unmount
      return () => {
        document.removeEventListener('keypress', handleKeyPress)
      }
    })
    
    return {
      form,
      showPassword,
      loading,
      error,
      isFormValid,
      handleLogin
    }
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  min-height: 600px;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

/* Header Section */
.login-header {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
}

.logo h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.logo p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

/* Form Section */
.login-form-container {
  flex: 1;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.login-form {
  width: 100%;
  max-width: 400px;
}

.login-form h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.login-subtitle {
  color: #6c757d;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

/* Error Message */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 0.375rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

/* Form Groups */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: 0.75rem;
  color: #6c757d;
  z-index: 1;
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: white;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-wrapper input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
  z-index: 1;
}

.password-toggle:hover {
  color: #495057;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

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
}

.checkbox-wrapper input[type="checkbox"]:checked + .checkmark {
  background: #667eea;
  border-color: #667eea;
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

.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

/* Login Button */
.login-button {
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Login Footer */
.login-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.login-footer p {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* Background */
.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.background-pattern {
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    margin: 1rem;
    min-height: auto;
  }
  
  .login-header {
    padding: 2rem;
    flex: none;
  }
  
  .logo h1 {
    font-size: 2rem;
  }
  
  .login-form-container {
    padding: 2rem;
    flex: none;
  }
}

@media (max-width: 480px) {
  .admin-login {
    padding: 0.5rem;
  }
  
  .login-header {
    padding: 1.5rem;
  }
  
  .login-form-container {
    padding: 1.5rem;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>