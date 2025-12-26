<template>
  <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
    <div class="position-sticky pt-3">
      <!-- Admin/Rider Links -->
      <ul v-if="!isCustomerRoute" class="nav flex-column">
        <li class="nav-item">
          <router-link to="/dashboard" class="nav-link" active-class="active">
            📊 Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/deliveries" class="nav-link" active-class="active">
            🚚 Deliveries
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/deliveries/new" class="nav-link" active-class="active">
            ➕ New Delivery
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/customers" class="nav-link" active-class="active">
            👥 Customers
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/drivers" class="nav-link" active-class="active">
            🏃‍♂️ Drivers
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/settings" class="nav-link" active-class="active">
            ⚙️ Settings
          </router-link>
        </li>
      </ul>

    </div>
  </nav>
</template>

<script setup>
// Sidebar component logic
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 48px 0 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.1);
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
  padding: 0.5rem 1rem;
}

.sidebar .nav-link:hover {
  color: #007bff;
}

.sidebar .nav-link.active {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  border-right: 3px solid #007bff;
}

.sidebar-heading {
  font-size: 0.75rem;
  text-transform: uppercase;
}

@media (max-width: 767.98px) {
  .sidebar {
    position: static;
    height: auto;
    padding-top: 0;
  }
}
</style>