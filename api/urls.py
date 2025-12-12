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
    # Customer endpoints
    path('customer/register/', views.CustomerRegistrationView.as_view(), name='customer_register'),
    path('customer/portal/', views.CustomerPortalView.as_view(), name='customer_portal'),
    path('customer/track/', views.OrderTrackingView.as_view(), name='order_tracking'),
]