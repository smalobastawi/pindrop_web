<template>
  <div class="address-selector">
    <label :for="inputId" class="form-label">{{ label }}</label>
    <div class="d-flex">
      <gmp-place-autocomplete
        :id="inputId"
        ref="searchInput"
        class="form-control mb-2 me-2"
        :placeholder="placeholder"
        location-restriction="KE"
        @gmp-placeselect="onPlaceSelect"
      ></gmp-place-autocomplete>
      <button type="button" class="btn btn-outline-secondary mb-2" @click="getCurrentLocation" :disabled="locationLoading">
        <span v-if="locationLoading" class="spinner-border spinner-border-sm me-1"></span>
        📍 Current Location
      </button>
    </div>

    <textarea
      v-model="formattedAddress"
      class="form-control mt-2"
      :rows="rows"
      :placeholder="addressPlaceholder"
      readonly
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: 'Address'
  },
  placeholder: {
    type: String,
    default: 'Search for a place...'
  },
  addressPlaceholder: {
    type: String,
    default: 'Selected address will appear here...'
  },
  rows: {
    type: Number,
    default: 2
  },
  inputId: {
    type: String,
    default: () => `address-input-${Date.now()}`
  }
})

const emit = defineEmits(['update:modelValue'])

const searchInput = ref(null)
const selectedPlace = ref(null)
const formattedAddress = ref(props.modelValue)
const locationLoading = ref(false)

const onPlaceSelect = (event) => {
  const place = event.detail.place
  if (place.geometry) {
    selectedPlace.value = place
    formattedAddress.value = place.formatted_address
    emit('update:modelValue', place.formatted_address)
  }
}

const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by this browser.')
    return
  }

  locationLoading.value = true

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude
      const latLng = new google.maps.LatLng(lat, lng)

      // Reverse geocode to get address
      const geocoder = new google.maps.Geocoder()
      geocoder.geocode({ location: latLng }, (results, status) => {
        locationLoading.value = false
        if (status === 'OK' && results[0]) {
          selectedPlace.value = {
            geometry: { location: latLng },
            formatted_address: results[0].formatted_address
          }
          formattedAddress.value = results[0].formatted_address
          emit('update:modelValue', results[0].formatted_address)
        } else {
          alert('Unable to retrieve address for your location.')
        }
      })
    },
    (error) => {
      locationLoading.value = false
      switch (error.code) {
        case error.PERMISSION_DENIED:
          alert('Location access denied by user.')
          break
        case error.POSITION_UNAVAILABLE:
          alert('Location information is unavailable.')
          break
        case error.TIMEOUT:
          alert('Location request timed out.')
          break
        default:
          alert('An unknown error occurred.')
          break
      }
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 300000 // 5 minutes
    }
  )
}


watch(() => props.modelValue, (newValue) => {
  if (newValue !== formattedAddress.value) {
    formattedAddress.value = newValue
  }
})

onMounted(async () => {
  await nextTick()
  // Google Maps and Places are loaded by vue3-google-map
})
</script>

<style scoped>
.address-selector .form-label {
  font-weight: 500;
  color: #495057;
}
</style>