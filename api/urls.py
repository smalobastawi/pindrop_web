# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'deliveries', views.DeliveryViewSet)
router.register(r'status-updates', views.DeliveryStatusUpdateViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Registration endpoints
    path('register/', views.UnifiedRegistrationView.as_view(), name='unified_register'),
    path('register/customer/', views.CustomerRegistrationView.as_view(), name='customer_register'),
    path('register/rider/', views.RiderRegistrationView.as_view(), name='rider_register'),
    
    # Customer endpoints
    path('customer/portal/', views.CustomerPortalView.as_view(), name='customer_portal'),
    path('customer/track/', views.OrderTrackingView.as_view(), name='order_tracking'),
    
    # Mobile app endpoints
    path('mobile/version/', views.MobileAPIVersionView.as_view(), name='mobile_api_version'),
    path('mobile/profile/', views.MobileUserProfileView.as_view(), name='mobile_profile'),
    path('mobile/device-token/', views.MobileDeviceTokenView.as_view(), name='mobile_device_token'),
]