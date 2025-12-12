# main/urls.py
from django.urls import path
from . import views
from . import views_customer

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('bootstrap-test/', views.bootstrap_test, name='bootstrap_test'),
    
    # Form pages
    path('contact-form/', views.contact_form, name='contact_form'),
    
    # Dynamic URL with parameter
    path('profile/<str:username>/', views.user_profile, name='profile'),
    
    # Customer portal
    path('customer-register/', views_customer.customer_register, name='customer_register'),
    path('customer-login/', views_customer.customer_login, name='customer_login'),
    path('customer-portal/', views_customer.customer_portal, name='customer_portal'),
    path('customer-logout/', views_customer.customer_logout, name='customer_logout'),
    
    # Customer API endpoints
    path('api/customer/create-order/', views_customer.create_order, name='create_order'),
    path('api/customer/track-order/', views_customer.track_order, name='track_order'),
]