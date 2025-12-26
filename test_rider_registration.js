/**
 * Rider Registration Test Script
 * This script tests the rider registration functionality with all required details
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Test configuration
const API_BASE_URL = 'http://localhost:8000'; // Adjust if your API runs on a different port
const TEST_IMAGE_PATH = 'frontend/src/assets/images/riderapp-logo.png'; // Using existing image for test

// Test rider data
const testRiderData = {
  firstName: 'Jane',
  lastName: 'Smith',
  email: 'jane.smith.rider' + Date.now() + '@example.com',
  phone: '+254723456789',
  address: '456 Rider Avenue, Nairobi, Kenya',
  identityType: 'national_id',
  identityNumber: '87654321',
  identityDocument: null, // Will be set from file
  licenseNumber: 'DRV123456',
  licenseExpiry: '2028-12-31',
  vehicleType: 'motorcycle',
  vehiclePlate: 'KCA456Y',
  vehicleModel: 'Honda CB125',
  vehicleColor: 'Red',
  username: 'janesmith_rider' + Date.now(),
  password: 'SecurePassword456!',
  confirmPassword: 'SecurePassword456!'
};

async function testRiderRegistration() {
  console.log('🚀 Starting Rider Registration Test...\n');

  try {
    // Create form data
    const formData = new FormData();
    
    // Add all rider details to form data
    formData.append('first_name', testRiderData.firstName);
    formData.append('last_name', testRiderData.lastName);
    formData.append('email', testRiderData.email);
    formData.append('phone', testRiderData.phone);
    formData.append('address', testRiderData.address);
    formData.append('identity_type', testRiderData.identityType);
    formData.append('identity_number', testRiderData.identityNumber);
    formData.append('license_number', testRiderData.licenseNumber);
    formData.append('license_expiry', testRiderData.licenseExpiry);
    formData.append('vehicle_type', testRiderData.vehicleType);
    formData.append('vehicle_plate', testRiderData.vehiclePlate);
    formData.append('vehicle_model', testRiderData.vehicleModel);
    formData.append('vehicle_color', testRiderData.vehicleColor);
    formData.append('username', testRiderData.username);
    formData.append('password', testRiderData.password);

    // Add identity document if available
    if (fs.existsSync(TEST_IMAGE_PATH)) {
      formData.append('identity_document', fs.createReadStream(TEST_IMAGE_PATH));
      console.log('✅ Identity document attached successfully');
    } else {
      console.log('⚠️  Test image not found, proceeding without identity document');
    }

    console.log('📋 Test Rider Data:');
    console.log(`   - Name: ${testRiderData.firstName} ${testRiderData.lastName}`);
    console.log(`   - Email: ${testRiderData.email}`);
    console.log(`   - Phone: ${testRiderData.phone}`);
    console.log(`   - Identity: ${testRiderData.identityType} (${testRiderData.identityNumber})`);
    console.log(`   - License: ${testRiderData.licenseNumber} (expires ${testRiderData.licenseExpiry})`);
    console.log(`   - Vehicle: ${testRiderData.vehicleColor} ${testRiderData.vehicleModel} (${testRiderData.vehiclePlate})`);
    console.log(`   - Username: ${testRiderData.username}`);
    console.log('');

    console.log('🔄 Sending registration request...');

    // Send registration request
    const response = await axios.post(`${API_BASE_URL}/api/register/rider/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log('🎉 Registration Response:');
    console.log('   Status:', response.status);
    console.log('   Data:', JSON.stringify(response.data, null, 2));
    console.log('');

    if (response.data.success) {
      console.log('✅ Rider registration test PASSED!');
      console.log('   Rider can now log in using:');
      console.log(`   - Username: ${testRiderData.username}`);
      console.log(`   - Password: ${testRiderData.password}`);
      console.log('');
      console.log('📝 Note: Registration may require admin approval before login is possible.');
    } else {
      console.log('❌ Rider registration test FAILED!');
      console.log('   Error:', response.data.message || 'Unknown error');
    }

  } catch (error) {
    console.error('💥 Registration test encountered an error:');
    
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('   Status:', error.response.status);
      console.error('   Data:', error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('   No response received from server');
      console.error('   Check if the API server is running at:', API_BASE_URL);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('   Error:', error.message);
    }
    
    console.log('');
    console.log('❌ Rider registration test FAILED due to error!');
  }
}

// Run the test
if (require.main === module) {
  testRiderRegistration();
}

module.exports = { testRiderRegistration };