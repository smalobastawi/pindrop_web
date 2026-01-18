<!-- frontend/src/views/PaymentOptions.vue -->
<template>
  <div class="payment-options">
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h4 class="mb-0">Select Payment Method</h4>
            </div>
            <div class="card-body">
              <!-- Order Summary -->
              <div class="mb-4">
                <h5>Order Summary</h5>
                <p><strong>Package:</strong> {{ pendingOrder?.package?.description }}</p>
                <p><strong>Weight:</strong> {{ pendingOrder?.package?.weight }} kg</p>
                <p><strong>Delivery Address:</strong> {{ pendingOrder?.delivery?.delivery_address }}</p>
                <p><strong>Total Amount:</strong> KSh {{ formatCurrency(pendingOrder?.payment?.amount) }}</p>
              </div>

              <!-- Payment Options -->
              <div class="row" v-if="!paymentInitiated">
                <!-- M-PESA Option -->
                <div class="col-md-6 mb-3">
                  <div class="card payment-card" :class="{ selected: selectedPayment === 'mpesa' }" @click="selectPayment('mpesa')">
                    <div class="card-body text-center">
                      <h5 class="card-title">M-PESA</h5>
                      <p class="card-text">Pay with M-PESA Mobile Money</p>
                      <i class="bi bi-phone-fill" style="font-size: 2rem;"></i>
                    </div>
                  </div>
                </div>

                <!-- DPO Option -->
                <div class="col-md-6 mb-3">
                  <div class="card payment-card" :class="{ selected: selectedPayment === 'dpo' }" @click="selectPayment('dpo')">
                    <div class="card-body text-center">
                      <h5 class="card-title">Direct Pay Online</h5>
                      <p class="card-text">Pay with Credit/Debit Card</p>
                      <i class="bi bi-credit-card-fill" style="font-size: 2rem;"></i>
                    </div>
                  </div>
                </div>
              </div>

              <!-- M-PESA Form -->
              <div v-if="selectedPayment === 'mpesa' && !paymentInitiated" class="mt-4">
                <h5>Enter M-PESA Details</h5>
                <form @submit.prevent="handleMpesaPayment">
                  <div class="mb-3">
                    <label for="phone" class="form-label">M-PESA Phone Number *</label>
                    <input
                      type="tel"
                      class="form-control"
                      id="phone"
                      v-model="mpesaPhone"
                      placeholder="254712345678"
                      required
                    />
                    <div class="form-text">Enter your M-PESA registered phone number (e.g., 254712345678)</div>
                  </div>
                  <button type="submit" class="btn btn-success" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    Send M-PESA Request
                  </button>
                </form>
              </div>

              <!-- M-PESA Waiting for Confirmation -->
              <div v-if="paymentInitiated && waitingForMpesa" class="mt-4">
                <div class="card bg-light">
                  <div class="card-body text-center">
                    <h5 class="card-title text-primary">
                      <i class="bi bi-phone-vibrate me-2"></i>
                      M-PESA Request Sent
                    </h5>
                    <p class="card-text">
                      A payment prompt has been sent to <strong>{{ mpesaPhone }}</strong>
                    </p>
                    <p class="card-text text-muted">
                      Please enter your M-PESA PIN on your phone to complete the payment.
                    </p>
                    
                    <div class="my-4">
                      <div class="spinner-border text-success" role="status">
                        <span class="visually-hidden">Waiting for confirmation...</span>
                      </div>
                      <p class="mt-2 text-muted">Waiting for payment confirmation...</p>
                      <p class="text-muted small">
                        Time remaining: <strong>{{ formatTime(timeRemaining) }}</strong>
                      </p>
                    </div>

                    <div class="progress mb-3" style="height: 8px;">
                      <div 
                        class="progress-bar bg-success" 
                        role="progressbar" 
                        :style="{ width: progressPercentage + '%' }"
                        :aria-valuenow="progressPercentage" 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Manual Transaction Code Entry (Shown after timeout or user request) -->
              <div v-if="showManualEntry" class="mt-4">
                <div class="alert alert-warning">
                  <i class="bi bi-exclamation-triangle me-2"></i>
                  <strong>Payment Confirmation Timeout</strong>
                  <p class="mb-0 mt-2">
                    We couldn't automatically confirm your payment. If you've completed the M-PESA transaction,
                    please enter the transaction code below to complete your order.
                  </p>
                </div>

                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title">Enter M-PESA Transaction Code</h5>
                    <p class="card-text text-muted small">
                      You can find the transaction code in the M-PESA confirmation SMS you received.
                      It usually starts with letters like "QJN" or "RJE" followed by numbers.
                    </p>
                    
                    <form @submit.prevent="confirmPaymentByCode">
                      <div class="mb-3">
                        <label for="transactionCode" class="form-label">M-PESA Transaction Code *</label>
                        <input
                          type="text"
                          class="form-control form-control-lg text-uppercase"
                          id="transactionCode"
                          v-model="transactionCode"
                          placeholder="e.g., QJN2ABCDEF"
                          required
                          maxlength="15"
                        />
                        <div class="form-text">Enter the M-PESA transaction code from your SMS</div>
                      </div>
                      
                      <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-success" :disabled="loading || !transactionCode.trim()">
                          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                          <i v-else class="bi bi-check-circle me-2"></i>
                          Confirm Payment
                        </button>
                        <button type="button" class="btn btn-outline-secondary" @click="retryMpesaPayment" :disabled="loading">
                          <i class="bi bi-arrow-repeat me-2"></i>
                          Retry M-PESA Request
                        </button>
                      </div>
                    </form>
                  </div>
                </div>

                <div class="mt-3 text-center">
                  <button class="btn btn-link text-muted" @click="showManualEntryEarly">
                    Didn't receive the M-PESA prompt? Enter code manually
                  </button>
                </div>
              </div>

              <!-- Show Manual Entry Link During Wait -->
              <div v-if="waitingForMpesa && !showManualEntry" class="mt-3 text-center">
                <button class="btn btn-link text-muted" @click="showManualEntryEarly">
                  Didn't receive the M-PESA prompt? Click here to enter code manually
                </button>
              </div>

              <!-- DPO Form -->
              <div v-if="selectedPayment === 'dpo' && !paymentInitiated" class="mt-4">
                <h5>Direct Pay Online</h5>
                <p>Redirecting to DPO payment gateway...</p>
                <button @click="handleDpoPayment" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  Proceed to DPO Payment
                </button>
              </div>

              <!-- Success Message -->
              <div v-if="paymentSuccess" class="alert alert-success mt-4">
                <i class="bi bi-check-circle-fill me-2"></i>
                <strong>Payment Successful!</strong>
                <p class="mb-0 mt-2">
                  Your payment has been confirmed. Redirecting to your orders...
                </p>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="alert alert-danger mt-3">
                <i class="bi bi-exclamation-circle me-2"></i>
                {{ error }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCustomerStore } from '@/stores/customerStore'
import { customerAPI } from '@/api/customers'
import { toast } from 'vue3-toastify'

const router = useRouter()
const customerStore = useCustomerStore()

const pendingOrder = computed(() => customerStore.pendingOrder)
const selectedPayment = ref('')
const mpesaPhone = ref('')
const loading = ref(false)
const error = ref('')
const waitingForMpesa = ref(false)
const paymentInitiated = ref(false)
const showManualEntry = ref(false)
const transactionCode = ref('')
const paymentSuccess = ref(false)
const currentOrderId = ref(null)
const checkoutRequestId = ref(null)

// Timer related
const PAYMENT_TIMEOUT_SECONDS = 120 // 2 minutes timeout
const POLL_INTERVAL_MS = 5000 // Check every 5 seconds
const timeRemaining = ref(PAYMENT_TIMEOUT_SECONDS)
let countdownTimer = null
let pollTimer = null

const progressPercentage = computed(() => {
  return ((PAYMENT_TIMEOUT_SECONDS - timeRemaining.value) / PAYMENT_TIMEOUT_SECONDS) * 100
})

const selectPayment = (method) => {
  selectedPayment.value = method
  error.value = ''
}

const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return new Intl.NumberFormat('en-KE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const startCountdown = () => {
  timeRemaining.value = PAYMENT_TIMEOUT_SECONDS
  
  countdownTimer = setInterval(() => {
    timeRemaining.value--
    
    if (timeRemaining.value <= 0) {
      stopTimers()
      handlePaymentTimeout()
    }
  }, 1000)
}

const startPolling = () => {
  pollTimer = setInterval(async () => {
    if (currentOrderId.value) {
      try {
        const response = await customerAPI.checkPaymentStatus(currentOrderId.value)
        const payment = response.data?.payment
        
        if (payment?.status === 'paid') {
          stopTimers()
          handlePaymentSuccess()
        } else if (payment?.status === 'failed') {
          stopTimers()
          handlePaymentFailed()
        }
      } catch (err) {
        console.error('Error checking payment status:', err)
      }
    }
  }, POLL_INTERVAL_MS)
}

const stopTimers = () => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const handlePaymentTimeout = () => {
  waitingForMpesa.value = false
  showManualEntry.value = true
  toast.warning('Payment confirmation timed out. Please enter your M-PESA transaction code manually.')
}

const handlePaymentSuccess = () => {
  waitingForMpesa.value = false
  showManualEntry.value = false
  paymentSuccess.value = true
  toast.success('Payment confirmed successfully!')
  
  // Redirect after 2 seconds
  setTimeout(() => {
    customerStore.clearPendingOrder()
    router.push('/customer-portal')
  }, 2000)
}

const handlePaymentFailed = () => {
  waitingForMpesa.value = false
  showManualEntry.value = true
  error.value = 'M-PESA payment was not completed. Please try again or enter the transaction code manually.'
  toast.error('Payment failed. Please try again.')
}

const showManualEntryEarly = () => {
  stopTimers()
  waitingForMpesa.value = false
  showManualEntry.value = true
}

const handleMpesaPayment = async () => {
  if (!mpesaPhone.value) {
    error.value = 'Please enter your M-PESA phone number'
    return
  }

  // Validate phone format
  const phoneRegex = /^254[0-9]{9}$/
  if (!phoneRegex.test(mpesaPhone.value)) {
    error.value = 'Please enter a valid Kenyan phone number starting with 254 (e.g., 254712345678)'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const paymentData = {
      payment_method: 'mpesa',
      phone_number: mpesaPhone.value
    }

    let response
    
    // Get the order ID - it could be in different places depending on how we got here
    const existingOrderId = pendingOrder.value.id || pendingOrder.value.delivery?.id

    if (existingOrderId) {
      // Existing order, update payment
      response = await customerAPI.updatePayment(existingOrderId, paymentData)
      currentOrderId.value = existingOrderId
    } else {
      // New order, create it
      const orderData = {
        ...pendingOrder.value,
        payment: {
          ...pendingOrder.value.payment,
          ...paymentData
        }
      }
      response = await customerAPI.createOrder(orderData)
      currentOrderId.value = response.data?.order?.id
    }

    // Store checkout request ID if available
    if (response.data?.checkout_request_id) {
      checkoutRequestId.value = response.data.checkout_request_id
    }

    paymentInitiated.value = true
    waitingForMpesa.value = true
    
    toast.success('M-PESA payment request sent! Please check your phone.')
    
    // Start countdown and polling
    startCountdown()
    startPolling()
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to initiate M-PESA payment. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const retryMpesaPayment = async () => {
  showManualEntry.value = false
  paymentInitiated.value = false
  error.value = ''
  transactionCode.value = ''
}

const confirmPaymentByCode = async () => {
  if (!transactionCode.value.trim()) {
    error.value = 'Please enter the M-PESA transaction code'
    return
  }

  // Validate transaction code format (typically 10 characters, alphanumeric)
  const codeRegex = /^[A-Z0-9]{8,12}$/i
  if (!codeRegex.test(transactionCode.value.trim())) {
    error.value = 'Please enter a valid M-PESA transaction code (8-12 alphanumeric characters)'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await customerAPI.confirmPaymentByCode(currentOrderId.value, {
      transaction_code: transactionCode.value.trim().toUpperCase(),
      phone_number: mpesaPhone.value
    })

    if (response.data?.success) {
      handlePaymentSuccess()
    } else {
      error.value = response.data?.message || 'Could not verify the transaction code. Please check and try again.'
      toast.error(error.value)
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to verify transaction code. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleDpoPayment = async () => {
  loading.value = true
  error.value = ''

  try {
    const paymentData = {
      payment_method: 'dpo'
    }
    
    // Get the order ID - it could be in different places depending on how we got here
    const existingOrderId = pendingOrder.value.id || pendingOrder.value.delivery?.id

    if (existingOrderId) {
      // Existing order, update payment
      await customerAPI.updatePayment(existingOrderId, paymentData)
      toast.success('Payment initiated successfully!')
    } else {
      // New order, create it
      const orderData = {
        ...pendingOrder.value,
        payment: {
          ...pendingOrder.value.payment,
          ...paymentData
        }
      }
      await customerAPI.createOrder(orderData)
      toast.success('Order created successfully! Redirecting to DPO...')
    }

    customerStore.clearPendingOrder()
    router.push('/customer-portal')
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to process DPO payment. Please try again.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!pendingOrder.value) {
    router.push('/customer-portal')
    return
  }
  
  // Pre-fill phone from customer profile if available
  const customerPhone = customerStore.customer?.phone
  if (customerPhone && customerPhone.startsWith('254')) {
    mpesaPhone.value = customerPhone
  }
})

onUnmounted(() => {
  stopTimers()
})
</script>

<style scoped>
.payment-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
}

.payment-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
}

.payment-card.selected {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.text-uppercase {
  text-transform: uppercase;
}

.progress {
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  transition: width 1s linear;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.spinner-border {
  animation: pulse 1.5s ease-in-out infinite;
}
</style>
