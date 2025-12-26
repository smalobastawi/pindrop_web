<!-- frontend/src/components/layout/CommonHeader.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold text-primary" to="/">
        <i class="fas fa-shipping-fast me-2"></i>RiderApp
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/customer-login" class="nav-link">Customer Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/rider-login" class="nav-link">Rider Login</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="registerDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Register
            </a>
            <ul class="dropdown-menu" aria-labelledby="registerDropdown">
              <li><router-link to="/customer-register" class="dropdown-item">Customer Register</router-link></li>
              <li><router-link to="/rider-register" class="dropdown-item">Rider Register</router-link></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
// No script needed for this component
</script>

<style scoped>
.navbar {
  padding: 1rem 0;
  transition: all 0.3s ease;
  z-index: 1030;
}

.navbar.scrolled {
  padding: 0.5rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  color: #007bff !important;
}

.nav-link:hover {
  color: #0056b3 !important;
}
</style>