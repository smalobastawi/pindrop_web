<template>
  <div class="landing-page">
    <!-- Common Header -->
    <CommonHeader />

    <!-- Compact Slider Section -->
    <section class="slider-section">
      <div id="heroCarousel" class="carousel slide compact-carousel" data-bs-ride="carousel" data-bs-interval="4000">
        <!-- Indicators -->
        <div class="carousel-indicators">
          <button type="button" 
                  data-bs-target="#heroCarousel" 
                  data-bs-slide-to="0" 
                  class="active" 
                  aria-current="true" 
                  aria-label="Slide 1"></button>
          <button type="button" 
                  data-bs-target="#heroCarousel" 
                  data-bs-slide-to="1" 
                  aria-label="Slide 2"></button>
          <button type="button" 
                  data-bs-target="#heroCarousel" 
                  data-bs-slide-to="2" 
                  aria-label="Slide 3"></button>
        </div>
        
        <!-- Carousel Inner -->
        <div class="carousel-inner">
          <!-- Slide 1 -->
          <div class="carousel-item active">
            <div class="slider-image-wrapper">
              <img :src="deliveryDashboardSlider" 
                   class="d-block w-100" 
                   alt="Delivery Dashboard"
                   loading="lazy">
              <div class="slider-overlay"></div>
            </div>
            <div class="carousel-caption">
              <div class="caption-content">
                <h2 class="fw-bold mb-3">Efficient Delivery Management</h2>
                <p class="lead mb-4">Streamline your delivery operations with our powerful platform.</p>
                <router-link to="/customer-register" class="btn btn-light btn-lg px-4">
                  Get Started <i class="fas fa-arrow-right ms-2"></i>
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Slide 2 -->
          <div class="carousel-item">
            <div class="slider-image-wrapper">
              <img :src="customerPortalSlider" 
                   class="d-block w-100" 
                   alt="Customer Portal"
                   loading="lazy">
              <div class="slider-overlay"></div>
            </div>
            <div class="carousel-caption">
              <div class="caption-content">
                <h2 class="fw-bold mb-3">Customer Portal</h2>
                <p class="lead mb-4">Track your orders and manage deliveries with ease.</p>
                <router-link to="/customer-register" class="btn btn-light btn-lg px-4">
                  Track Orders <i class="fas fa-map-marker-alt ms-2"></i>
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Slide 3 -->
          <div class="carousel-item">
            <div class="slider-image-wrapper">
              <img :src="riderPortalSlider" 
                   class="d-block w-100" 
                   alt="Rider Portal"
                   loading="lazy">
              <div class="slider-overlay"></div>
            </div>
            <div class="carousel-caption">
              <div class="caption-content">
                <h2 class="fw-bold mb-3">Rider Portal</h2>
                <p class="lead mb-4">Manage your deliveries and track your earnings efficiently.</p>
                <router-link to="/rider-register" class="btn btn-light btn-lg px-4">
                  Join as Rider <i class="fas fa-motorcycle ms-2"></i>
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Navigation Buttons -->
        <button class="carousel-control-prev" 
                type="button" 
                data-bs-target="#heroCarousel" 
                data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" 
                type="button" 
                data-bs-target="#heroCarousel" 
                data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>
  
    <!-- Features Section -->
    <section id="features" class="py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-5 fw-bold mb-4">Streamline Your Delivery Operations</h1>
            <p class="lead mb-4">Powerful delivery management system for businesses of all sizes. Track, manage, and optimize your deliveries in real-time.</p>
            <div class="d-flex gap-3">
              <router-link to="/customer-register" class="btn btn-primary btn-lg px-4">
                Get Started <i class="fas fa-arrow-right ms-2"></i>
              </router-link>
              <a href="#how-it-works" class="btn btn-outline-primary btn-lg px-4">
                Learn More
              </a>
            </div>
          </div>
          <div class="col-lg-6">
            <!-- Use local image here too -->
            <img :src="deliveryDashboardSlider" 
                 alt="Delivery Dashboard" class="img-fluid rounded shadow-lg">
          </div>
        </div>
      </div>
    </section>

    <!-- Features Grid Section -->
    <section class="py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold">Just the Useful Stuff!</h2>
          <p class="text-muted">Everything you need to manage your delivery operations efficiently</p>
        </div>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon bg-primary bg-gradient text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                  <i class="fas fa-map-marked-alt fa-2x"></i>
                </div>
                <h4 class="fw-bold">Real-time Tracking</h4>
                <p class="text-muted">Track deliveries in real-time with GPS integration and live updates for customers.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon bg-success bg-gradient text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                  <i class="fas fa-route fa-2x"></i>
                </div>
                <h4 class="fw-bold">Route Optimization</h4>
                <p class="text-muted">AI-powered route planning to reduce delivery time and fuel consumption.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm hover-card">
              <div class="card-body text-center p-4">
                <div class="feature-icon bg-warning bg-gradient text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                  <i class="fas fa-chart-line fa-2x"></i>
                </div>
                <h4 class="fw-bold">Analytics Dashboard</h4>
                <p class="text-muted">Comprehensive analytics and reporting to make data-driven decisions.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold">How It Works</h2>
          <p class="text-muted">Simple three-step process to manage your deliveries</p>
        </div>
        <div class="row align-items-center">
          <div class="col-lg-4 text-center">
            <div class="step-number bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <span class="h4 mb-0">1</span>
            </div>
            <h4>Place an Order</h4>
            <p>Place a delivery order with pickup and drop-off locations, package details, and special instructions.</p>
          </div>
          <div class="col-lg-4 text-center">
            <div class="step-number bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <span class="h4 mb-0">2</span>
            </div>
            <h4>Assign & Track</h4>
            <p>Your package is assigned to the immediate available drivers. Track the progress in real-time on the map.</p>
          </div>
          <div class="col-lg-4 text-center">
            <div class="step-number bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 60px; height: 60px;">
              <span class="h4 mb-0">3</span>
            </div>
            <h4>Complete & Review</h4>
            <p>Once delivered, give us a thumbs up and review the delivery experience.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Customers Section -->
    <section id="customers" class="py-5 bg-light">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <!-- Use local image -->
            <img :src="customerPortalSlider" 
                 alt="Customer Portal" class="img-fluid rounded shadow-lg">
          </div>
          <div class="col-lg-6">
            <h2 class="fw-bold mb-4">For Customers</h2>
            <p class="lead mb-4">Track your orders, manage deliveries, and stay updated with real-time notifications.</p>
            <ul class="list-unstyled mb-4">
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Real-time order tracking</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Easy order management</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Secure payment options</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Delivery notifications</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Multiple delivery options</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Package insurance</li>
            </ul>
            <router-link to="/customer-register" class="btn btn-primary btn-lg px-4">
              Get Started <i class="fas fa-arrow-right ms-2"></i>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Riders Section -->
    <section id="riders" class="py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h2 class="fw-bold mb-4">For Riders</h2>
            <p class="lead mb-4">Manage your deliveries, track your earnings, and optimize your routes.</p>
            <ul class="list-unstyled mb-4">
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Flexible schedule management</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Real-time earnings tracking</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> AI-powered route optimization</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Instant payment processing</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Rider support 24/7</li>
              <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Performance analytics</li>
            </ul>
            <router-link to="/rider-register" class="btn btn-primary btn-lg px-4">
              Join Now <i class="fas fa-arrow-right ms-2"></i>
            </router-link>
          </div>
          <div class="col-lg-6">
            <!-- Use local image -->
            <img :src="riderPortalSlider" 
                 alt="Rider Portal" class="img-fluid rounded shadow-lg">
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold">Simple Pricing</h2>
          <p class="text-muted">Choose the plan that fits your business needs</p>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-4">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body p-4">
                <h5 class="card-title fw-bold">Starter</h5>
                <h2 class="fw-bold text-primary">Ksh 3000<span class="fs-6 text-muted">/month</span></h2>
                <p class="text-muted">Perfect for small businesses</p>
                <ul class="list-unstyled mb-4">
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Up to 100 deliveries/month</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Basic tracking</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Email support</li>
                  <li class="mb-2"><i class="fas fa-times text-muted me-2"></i> Advanced analytics</li>
                  <li class="mb-2"><i class="fas fa-times text-muted me-2"></i> API access</li>
                </ul>
                <router-link to="/customer-register" class="btn btn-outline-primary w-100">Get Started</router-link>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-primary shadow-lg h-100">
              <div class="card-body p-4">
                <span class="badge bg-primary position-absolute top-0 start-50 translate-middle px-3 py-2">Most Popular</span>
                <h5 class="card-title fw-bold">Business</h5>
                <h2 class="fw-bold text-primary">Ksh 10000<span class="fs-6 text-muted">/month</span></h2>
                <p class="text-muted">For growing businesses</p>
                <ul class="list-unstyled mb-4">
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Up to 1000 packages/month</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Advanced tracking</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Priority support</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Advanced analytics</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Basic API access</li>
                </ul>
                <router-link to="/customer-register" class="btn btn-primary w-100">Get Started</router-link>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body p-4">
                <h5 class="card-title fw-bold">Enterprise</h5>
                <h2 class="fw-bold text-primary">Custom</h2>
                <p class="text-muted">For large enterprises</p>
                <ul class="list-unstyled mb-4">
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Unlimited deliveries</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Real-time tracking</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> 24/7 dedicated support</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Custom analytics</li>
                  <li class="mb-2"><i class="fas fa-check text-success me-2"></i> Full API access</li>
                </ul>
                <button class="btn btn-outline-primary w-100" @click="contactSales">Contact Sales</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-5 bg-primary text-white">
      <div class="container">
        <div class="row justify-content-center text-center">
          <div class="col-lg-8">
            <h2 class="fw-bold mb-4">Ready to Transform Your Delivery Operations?</h2>
            <p class="lead mb-4">Join thousands of businesses that trust RiderApp for their delivery management needs.</p>
            <div class="d-flex gap-3 justify-content-center">
              <router-link to="/customer-register" class="btn btn-light btn-lg px-5">
                Start Free Trial <i class="fas fa-rocket ms-2"></i>
              </router-link>
              <router-link to="/rider-register" class="btn btn-outline-light btn-lg px-5">
                Join as Rider <i class="fas fa-motorcycle ms-2"></i>
              </router-link>
            </div>
            <p class="small mt-3 opacity-75">No credit card required • 14-day free trial</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Common Footer -->
    <CommonFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CommonHeader from '@/components/layout/CommonHeader.vue'
import CommonFooter from '@/components/layout/CommonFooter.vue'

// Import local images - fix the paths as needed
import deliveryDashboardSlider from '@/assets/images/slider1.jpg'
import customerPortalSlider from '@/assets/images/customer-portal.png'
import riderPortalSlider from '@/assets/images/rider-electric-bike.png'

// If you have different images for features, import them here too
// import deliveryDashboardFeature from '@/assets/images/feature1.jpg'
// import customerPortalFeature from '@/assets/images/feature2.jpg'
// import riderPortalFeature from '@/assets/images/feature3.jpg'

const contactSales = () => {
  alert('Thank you for your interest! Our sales team will contact you shortly.')
}

// Initialize carousel if Bootstrap doesn't auto-initialize
onMounted(() => {
  // Wait a bit to ensure DOM is ready
  setTimeout(() => {
    const carouselElement = document.getElementById('heroCarousel')
    if (carouselElement && window.bootstrap && window.bootstrap.Carousel) {
      new window.bootstrap.Carousel(carouselElement, {
        interval: 4000,
        wrap: true,
        touch: true
      })
    }
  }, 100)
})
</script>

<style scoped>
.landing-page {
  scroll-behavior: smooth;
}

/* Compact Slider - Reduced Height */
.slider-section {
  margin-top: 76px; /* Account for fixed navbar */
}

.compact-carousel {
  height: 450px; /* Reduced height - was 500px */
  overflow: hidden;
  position: relative;
}

.compact-carousel .carousel-inner {
  height: 100%;
  width: 100%;
}

.compact-carousel .carousel-item {
  height: 100%;
  transition: transform 0.6s ease-in-out;
}

.slider-image-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
}

.compact-carousel .carousel-item img {
  object-fit: cover;
  height: 100%;
  width: 100%;
  filter: brightness(0.7);
}

.slider-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to right, 
    rgba(0,0,0,0.3) 0%, 
    rgba(0,0,0,0.5) 50%,
    rgba(0,0,0,0.2) 100%);
}

.carousel-caption {
  position: absolute;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  text-align: left;
  padding: 2rem;
  max-width: 600px;
}

.caption-content h2 {
  font-size: 2.2rem; /* Slightly smaller */
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  color: white;
}

.caption-content .lead {
  font-size: 1.1rem; /* Slightly smaller */
  margin-bottom: 1.5rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
  color: rgba(255,255,255,0.9);
}

/* Carousel Indicators */
.carousel-indicators {
  bottom: 15px; /* Moved up a bit */
}

.carousel-indicators [data-bs-target] {
  width: 10px; /* Smaller */
  height: 10px; /* Smaller */
  margin: 0 4px; /* Tighter spacing */
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  background-color: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-indicators .active {
  background-color: white;
  border-color: white;
}

/* Carousel Controls */
.carousel-control-prev,
.carousel-control-next {
  width: 40px; /* Smaller */
  height: 40px; /* Smaller */
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  margin: 0 15px; /* Tighter margins */
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  background: rgba(0, 0, 0, 0.5);
}

/* Features Cards */
.feature-icon {
  transition: transform 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
  transition: all 0.3s ease;
}

.hover-card:hover .feature-icon {
  transform: scale(1.1);
}

.step-number {
  font-weight: bold;
}

.navbar {
  padding: 1rem 0;
  transition: all 0.3s ease;
  z-index: 1030;
}

.navbar.scrolled {
  padding: 0.5rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.footer-link:hover {
  color: white !important;
}

.text-muted {
  color: #6c757d !important;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .compact-carousel {
    height: 400px; /* Even smaller on tablets */
  }
  
  .carousel-caption {
    left: 5%;
    padding: 1.5rem;
  }
  
  .caption-content h2 {
    font-size: 1.8rem;
  }
  
  .caption-content .lead {
    font-size: 1rem;
  }
}

@media (max-width: 768px) {
  .compact-carousel {
    height: 350px; /* Smaller on mobile */
  }
  
  .carousel-caption {
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    padding: 1rem;
    width: 90%;
  }
  
  .caption-content h2 {
    font-size: 1.5rem;
  }
  
  .caption-content .lead {
    font-size: 0.9rem;
  }
  
  .carousel-control-prev,
  .carousel-control-next {
    display: none; /* Hide arrows on small screens */
  }
  
  .display-5 {
    font-size: 2rem;
  }
  
  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .compact-carousel {
    height: 300px; /* Smallest on mobile */
  }
  
  .caption-content h2 {
    font-size: 1.3rem;
  }
  
  .caption-content .lead {
    font-size: 0.85rem;
  }
  
  .btn-light.btn-lg {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}

/* Bootstrap carousel animations */
.carousel-item {
  display: none;
  transition: transform 0.6s ease-in-out;
}

.carousel-item.active,
.carousel-item-next,
.carousel-item-prev {
  display: block;
}

.carousel-item-next:not(.carousel-item-start),
.active.carousel-item-end {
  transform: translateX(100%);
}

.carousel-item-prev:not(.carousel-item-end),
.active.carousel-item-start {
  transform: translateX(-100%);
}
</style>