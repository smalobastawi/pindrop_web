<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="text-center mb-0">Rider Registration</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="registerRider" enctype="multipart/form-data">
              
              <!-- Personal Information Section -->
              <div class="mb-4">
                <h5 class="text-primary">Personal Information</h5>
                <hr>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label">First Name</label>
                    <input type="text" class="form-control" id="firstName" v-model="form.firstName" required>
                  </div>
                  <div class="col-md-6">
                    <label for="lastName" class="form-label">Last Name</label>
                    <input type="text" class="form-control" id="lastName" v-model="form.lastName" required>
                  </div>
                </div>
                
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" v-model="form.email" required>
                  </div>
                  <div class="col-md-6">
                    <label for="phone" class="form-label">Phone Number</label>
                    <input type="tel" class="form-control" id="phone" v-model="form.phone" required>
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="address" class="form-label">Address</label>
                  <textarea class="form-control" id="address" v-model="form.address" rows="2" required></textarea>
                </div>
              </div>
              
              <!-- Identity Information Section -->
              <div class="mb-4">
                <h5 class="text-primary">Identity Information</h5>
                <hr>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="identityType" class="form-label">Identity Type</label>
                    <select class="form-select" id="identityType" v-model="form.identityType" required>
                      <option value="">Select Identity Type</option>
                      <option value="passport">Passport</option>
                      <option value="national_id">National ID</option>
                      <option value="drivers_license">Driver's License</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label for="identityNumber" class="form-label">Identity Number</label>
                    <input type="text" class="form-control" id="identityNumber" v-model="form.identityNumber" required>
                  </div>
                </div>
                
                <div class="mb-3">
                    <label for="identityDocument" class="form-label">Identity Document (Passport Photo)</label>
                    <input type="file" class="form-control" id="identityDocument" @change="handleIdentityDocumentUpload" accept="image/*" capture="environment">
                    <small class="text-muted">You can upload an image or take a photo using your device camera (optional)</small>
                  </div>
                
                <div class="mb-3" v-if="identityDocumentPreview">
                  <img :src="identityDocumentPreview" alt="Identity Document Preview" class="img-thumbnail" style="max-height: 200px;">
                </div>
              </div>
              
              <!-- License Information Section -->
              <div class="mb-4">
                <h5 class="text-primary">License Information</h5>
                <hr>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="licenseNumber" class="form-label">License Number</label>
                    <input type="text" class="form-control" id="licenseNumber" v-model="form.licenseNumber" required>
                  </div>
                  <div class="col-md-6">
                    <label for="licenseExpiry" class="form-label">License Expiry Date</label>
                    <input type="date" class="form-control" id="licenseExpiry" v-model="form.licenseExpiry" required>
                  </div>
                </div>
              </div>
              
              <!-- Vehicle Information Section -->
              <div class="mb-4">
                <h5 class="text-primary">Vehicle Information</h5>
                <hr>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="vehicleType" class="form-label">Vehicle Type</label>
                    <select class="form-select" id="vehicleType" v-model="form.vehicleType" required>
                      <option value="">Select Vehicle Type</option>
                      <option value="bicycle">Bicycle</option>
                      <option value="motorcycle">Motorcycle</option>
                      <option value="car">Car</option>
                      <option value="van">Van</option>
                      <option value="truck">Truck</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label for="vehiclePlate" class="form-label">Vehicle Plate Number</label>
                    <input type="text" class="form-control" id="vehiclePlate" v-model="form.vehiclePlate" required>
                  </div>
                </div>
                
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="vehicleModel" class="form-label">Vehicle Model</label>
                    <input type="text" class="form-control" id="vehicleModel" v-model="form.vehicleModel">
                  </div>
                  <div class="col-md-6">
                    <label for="vehicleColor" class="form-label">Vehicle Color</label>
                    <input type="text" class="form-control" id="vehicleColor" v-model="form.vehicleColor">
                  </div>
                </div>
              </div>
              
              <!-- Account Information Section -->
              <div class="mb-4">
                <h5 class="text-primary">Account Information</h5>
                <hr>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" v-model="form.username" required>
                  </div>
                  <div class="col-md-6">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="form.password" required>
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <input type="password" class="form-control" id="confirmPassword" v-model="form.confirmPassword" required>
                </div>
              </div>
              
              <!-- Submit Button -->
              <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="submit" class="btn btn-primary btn-lg px-5" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-else>Register as Rider</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

export default {
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const loading = ref(false);
    const identityDocumentPreview = ref(null);
    
    const form = ref({
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: '',
      identityType: '',
      identityNumber: '',
      identityDocument: null,
      licenseNumber: '',
      licenseExpiry: '',
      vehicleType: '',
      vehiclePlate: '',
      vehicleModel: '',
      vehicleColor: '',
      username: '',
      password: '',
      confirmPassword: ''
    });
    
    const handleIdentityDocumentUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        // For now, just store the file (can be used later for profile update)
        form.value.identityDocument = file;

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          identityDocumentPreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };
    
    const registerRider = async () => {
      // Validate required fields
      if (!form.value.firstName.trim()) {
        alert('First name is required!');
        return;
      }
      if (!form.value.lastName.trim()) {
        alert('Last name is required!');
        return;
      }
      if (!form.value.email.trim()) {
        alert('Email is required!');
        return;
      }
      if (!form.value.phone.trim()) {
        alert('Phone number is required!');
        return;
      }
      if (!form.value.address.trim()) {
        alert('Address is required!');
        return;
      }
      if (!form.value.identityType) {
        alert('Identity type is required!');
        return;
      }
      if (!form.value.identityNumber.trim()) {
        alert('Identity number is required!');
        return;
      }
      // Note: identity_document is optional
      if (!form.value.licenseNumber.trim()) {
        alert('License number is required!');
        return;
      }
      if (!form.value.vehicleType) {
        alert('Vehicle type is required!');
        return;
      }
      if (!form.value.vehiclePlate.trim()) {
        alert('Vehicle plate number is required!');
        return;
      }
      if (!form.value.username.trim()) {
        alert('Username is required!');
        return;
      }
      if (!form.value.password.trim()) {
        alert('Password is required!');
        return;
      }
      if (form.value.password !== form.value.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }

      loading.value = true;

      try {
        const registrationData = {
          first_name: form.value.firstName,
          last_name: form.value.lastName,
          email: form.value.email,
          phone: form.value.phone,
          address: form.value.address,
          identity_type: form.value.identityType,
          identity_number: form.value.identityNumber,
          license_number: form.value.licenseNumber,
          license_expiry: form.value.licenseExpiry,
          vehicle_type: form.value.vehicleType,
          vehicle_plate: form.value.vehiclePlate,
          vehicle_model: form.value.vehicleModel,
          vehicle_color: form.value.vehicleColor,
          username: form.value.username,
          password: form.value.password
        };

        // Call the API to register rider
        const response = await authStore.registerRider(registrationData);

        if (response.success) {
          // Try to auto-login
          try {
            const loginResponse = await axios.post('/api/token/', {
              username: form.email,
              password: form.password
            })

            // Store tokens
            localStorage.setItem('access_token', loginResponse.data.access)
            localStorage.setItem('refresh_token', loginResponse.data.refresh)

            alert('Rider registration successful! Your account is pending approval.');
            router.push('/dashboard');
          } catch (loginErr) {
            console.error('Auto-login failed:', loginErr);
            // If auto-login fails, redirect to login
            alert('Rider registration successful! Please wait for admin approval before logging in.');
            router.push('/rider-login');
          }
        } else {
          alert('Registration failed: ' + (response.message || 'Unknown error'));
        }
      } catch (error) {
        console.error('Registration error:', error);
        alert('An error occurred during registration. Please try again.');
      } finally {
        loading.value = false;
      }
    };
    
    return {
      form,
      loading,
      identityDocumentPreview,
      handleIdentityDocumentUpload,
      registerRider
    };
  }
};
</script>

<style scoped>
.card {
  border-radius: 15px;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, #007bff, #0056b3);
}

.btn-primary {
  background: linear-gradient(135deg, #007bff, #0056b3);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0069d9, #004085);
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25);
}
</style>