// frontend/src/stores/customerStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCustomerStore = defineStore('customer', () => {
  const pendingOrder = ref(null)

  const setPendingOrder = (orderData) => {
    pendingOrder.value = orderData
  }

  const clearPendingOrder = () => {
    pendingOrder.value = null
  }

  return {
    pendingOrder,
    setPendingOrder,
    clearPendingOrder
  }
})