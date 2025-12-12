<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <Navbar v-if="isAuthenticated" />
    <div class="container-fluid" v-if="isAuthenticated">
      <div class="row">
        <Sidebar v-if="isAuthenticated" />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          <router-view />
        </main>
      </div>
    </div>
    <router-view v-else />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import Navbar from "@/components/layout/Navbar.vue";
import Sidebar from "@/components/layout/Sidebar.vue";

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
</script>

<style>
#app {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 48px 0 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.1);
}

.main-content {
  margin-left: 250px;
  padding: 20px;
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
    height: auto;
  }
  .main-content {
    margin-left: 0;
  }
}
</style>
