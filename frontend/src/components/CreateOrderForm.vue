<!-- frontend/src/components/CreateOrderForm.vue -->
<template>
  <form @submit.prevent="handleSubmit">
    <!-- Package Information -->
    <div class="mb-4">
      <h6 class="border-bottom pb-2 mb-3">Package Information</h6>
      <div class="row">
        <div class="col-md-8 mb-3">
          <label for="description" class="form-label">Package Description *</label>
          <textarea
            class="form-control"
            id="description"
            rows="2"
            v-model="form.package.description"
            required
          ></textarea>
        </div>
        <div class="col-md-4 mb-3">
          <label for="weight" class="form-label">Weight (kg) *</label>
          <input
            type="number"
            step="0.1"
            class="form-control"
            id="weight"
            v-model="form.package.weight"
            required
          />
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="dimensions" class="form-label">Dimensions (LxWxH cm) *</label>
          <input
            type="text"
            class="form-control"
            id="dimensions"
            v-model="form.package.dimensions"
            placeholder="30x20x10"
            required
          />
        </div>
        <div class="col-md-6 mb-3">
          <label for="package_type" class="form-label">Package Type *</label>
          <select class="form-control" id="package_type" v-model="form.package.package_type" required>
            <option value="">Select Type</option>
            <option value="document">Document</option>
            <option value="parcel">Parcel</option>
            <option value="fragile">Fragile</option>
            <option value="perishable">Perishable</option>
          </select>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="value" class="form-label">Package Value (KSh)</label>
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="value"
            v-model="form.package.value"
          />
        </div>
        <div class="col-md-6 mb-3">
          <label for="special_instructions" class="form-label">Special Instructions</label>
          <input
            type="text"
            class="form-control"
            id="special_instructions"
            v-model="form.package.special_instructions"
          />
        </div>
      </div>
    </div>

    <!-- Delivery Information -->
    <div class="mb-4">
      <h6 class="border-bottom pb-2 mb-3">Delivery Information</h6>
      <div class="mb-3">
        <AddressSelector
          v-model="form.delivery.pickup_address"
          label="Pickup Address *"
          placeholder="Search for pickup location..."
          address-placeholder="Selected pickup address will appear here..."
        />
      </div>
      
      <div class="mb-3">
        <AddressSelector
          v-model="form.delivery.delivery_address"
          label="Delivery Address *"
          placeholder="Search for delivery location..."
          address-placeholder="Selected delivery address will appear here..."
        />
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="recipient_name" class="form-label">Recipient Name *</label>
          <input
            type="text"
            class="form-control"
            id="recipient_name"
            v-model="form.delivery.recipient_name"
            required
          />
        </div>
        <div class="col-md-6 mb-3">
          <label for="recipient_phone" class="form-label">Recipient Phone *</label>
          <input
            type="tel"
            class="form-control"
            id="recipient_phone"
            v-model="form.delivery.recipient_phone"
            required
          />
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="estimated_pickup" class="form-label">Estimated Pickup *</label>
          <input
            type="datetime-local"
            class="form-control"
            id="estimated_pickup"
            v-model="form.delivery.estimated_pickup"
            required
          />
        </div>
        <div class="col-md-6 mb-3">
          <label for="estimated_delivery" class="form-label">Estimated Delivery *</label>
          <input
            type="datetime-local"
            class="form-control"
            id="estimated_delivery"
            v-model="form.delivery.estimated_delivery"
            required
          />
        </div>
      </div>
      
      <div class="mb-3">
        <label for="priority" class="form-label">Delivery Priority</label>
        <select class="form-control" id="priority" v-model="form.delivery.priority">
          <option value="1">Normal (Standard Fee)</option>
          <option value="2">Express (+50% Fee)</option>
          <option value="3">Urgent (+100% Fee)</option>
        </select>
      </div>
    </div>

    <!-- Payment Information -->
    <div class="mb-4">
      <h6 class="border-bottom pb-2 mb-3">Payment Information</h6>
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="payment_method" class="form-label">Payment Method *</label>
          <select class="form-control" id="payment_method" v-model="form.payment.payment_method" required>
            <option value="">Select Payment Method</option>
            <option value="cash">Cash on Delivery</option>
            <option value="card">Credit/Debit Card</option>
            <option value="bank">Bank Transfer</option>
            <option value="mobile">Mobile Money</option>
          </select>
        </div>
        <div class="col-md-6 mb-3">
          <label for="amount" class="form-label">Amount (KSh)</label>
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="amount"
            v-model="form.payment.amount"
            readonly
          />
        </div>
      </div>
      
      <div class="alert alert-info">
        <strong>Estimated Cost:</strong>
        Base: {{ formatCurrency(calculateBaseCost()) }} |
        Priority: {{ getPriorityText() }} |
        <strong>Total: {{ formatCurrency(form.payment.amount) }}</strong>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div class="d-flex justify-content-end">
      <button type="button" class="btn btn-secondary me-2" @click="$emit('cancel')">
        Cancel
      </button>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        Create Order
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'
import AddressSelector from '@/components/AddressSelector.vue'

const emit = defineEmits(['order-created', 'cancel'])
const loading = ref(false)
const error = ref('')

const form = reactive({
  package: {
    description: '',
    weight: '',
    dimensions: '',
    package_type: '',
    value: '',
    special_instructions: ''
  },
  delivery: {
    pickup_address: '',
    delivery_address: '',
    recipient_name: '',
    recipient_phone: '',
    estimated_pickup: '',
    estimated_delivery: '',
    priority: '1'
  },
  payment: {
    payment_method: '',
    amount: 0
  }
})

// Calculate delivery cost
const calculateBaseCost = () => {
  const weight = parseFloat(form.package.weight) || 0
  const baseRate = 10 // KSh 10 per kg
  return (weight * baseRate).toFixed(2)
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'KES'
  }).format(amount)
}

const getPriorityText = () => {
  const priority = parseInt(form.delivery.priority)
  if (priority === 1) return 'Standard'
  if (priority === 2) return '+50%'
  if (priority === 3) return '+100%'
  return 'Standard'
}

// Update amount when package weight or priority changes
watch(() => [form.package.weight, form.delivery.priority], () => {
  const baseCost = parseFloat(calculateBaseCost())
  const priority = parseInt(form.delivery.priority)
  let multiplier = 1
  
  if (priority === 2) multiplier = 1.5
  if (priority === 3) multiplier = 2
  
  form.payment.amount = (baseCost * multiplier).toFixed(2)
}, { immediate: true })

const handleSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    // Prepare the data
    const orderData = {
      package: {
        ...form.package,
        weight: parseFloat(form.package.weight),
        value: parseFloat(form.package.value) || 0
      },
      delivery: {
        ...form.delivery,
        priority: parseInt(form.delivery.priority)
      },
      payment: {
        ...form.payment,
        amount: parseFloat(form.payment.amount)
      }
    }
    
    await customerAPI.createOrder(orderData)
    emit('order-created')
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to create order. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
h6 {
  color: #495057;
  font-weight: 600;
}
</style>