<!-- frontend/src/components/layout/CommonFooter.vue -->
<template>
  <footer class="bg-dark text-white py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 mb-4">
          <h5 class="fw-bold mb-3">
            <i class="fas fa-shipping-fast me-2"></i>RiderApp
          </h5>
          <p class="text-muted">Powerful delivery management system for modern businesses. Streamline your operations with our comprehensive platform.</p>
          <div class="d-flex gap-3 mt-4">
            <a href="#" class="text-white"><i class="fab fa-facebook fa-lg"></i></a>
            <a href="#" class="text-white"><i class="fab fa-twitter fa-lg"></i></a>
            <a href="#" class="text-white"><i class="fab fa-linkedin fa-lg"></i></a>
            <a href="#" class="text-white"><i class="fab fa-instagram fa-lg"></i></a>
          </div>
        </div>
        <div class="col-lg-2 col-md-4 mb-4">
          <h6 class="fw-bold mb-3">Product</h6>
          <ul class="list-unstyled">
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Features</a></li>
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Pricing</a></li>
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">How It Works</a></li>
         
          </ul>
        </div>
        <div class="col-lg-2 col-md-4 mb-4">
          <h6 class="fw-bold mb-3">Company</h6>
          <ul class="list-unstyled">
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">About Us</a></li>
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Careers</a></li>
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Blog</a></li>
            <li class="mb-2"><a href="#" class="text-muted text-decoration-none">Press</a></li>
          </ul>
        </div>
        <div class="col-lg-4 mb-4">
          <h6 class="fw-bold mb-3">Contact Us</h6>
          <p class="text-muted mb-2"><i class="fas fa-envelope me-2"></i> support@riderapp.com</p>
          <p class="text-muted mb-2"><i class="fas fa-phone me-2"></i> +254 700 000 000</p>
          <p class="text-muted"><i class="fas fa-map-marker-alt me-2"></i>Nairobi, Kenya</p>
        </div>
      </div>
      <hr class="bg-secondary">
      <div class="row">
        <div class="col-md-6">
          <p class="text-muted mb-0">&copy; 2025 RiderApp. All rights reserved.</p>
        </div>
        <div class="col-md-6 text-md-end">
          <a href="#" class="text-muted text-decoration-none me-3">Privacy Policy</a>
          <a href="#" class="text-muted text-decoration-none">Terms of Service</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
// No script needed for this component
</script>

<style scoped>
.footer-link:hover {
  color: white !important;
}

.text-muted {
  color: #6c757d !important;
}
</style>