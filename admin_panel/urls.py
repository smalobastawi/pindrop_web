# admin_panel/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet, AdminRoleViewSet, SystemSettingsViewSet, AuditLogViewSet,
    DeliveryRouteViewSet, NotificationTemplateViewSet, SystemBackupViewSet,
    AdminDashboardViewSet, RiderManagementViewSet, UserManagementViewSet,
    DeliveryManagementViewSet, CustomerManagementViewSet,
    admin_login, admin_token_refresh, admin_change_password
)

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-users')
router.register(r'roles', AdminRoleViewSet, basename='admin-roles')
router.register(r'settings', SystemSettingsViewSet, basename='admin-settings')
router.register(r'audit-logs', AuditLogViewSet, basename='admin-audit-logs')
router.register(r'routes', DeliveryRouteViewSet, basename='admin-routes')
router.register(r'templates', NotificationTemplateViewSet, basename='admin-templates')
router.register(r'backups', SystemBackupViewSet, basename='admin-backups')
router.register(r'dashboard', AdminDashboardViewSet, basename='admin-dashboard')
router.register(r'riders', RiderManagementViewSet, basename='admin-riders')
router.register(r'customers', CustomerManagementViewSet, basename='admin-customers')
router.register(r'user-management', UserManagementViewSet, basename='admin-user-management')
router.register(r'deliveries', DeliveryManagementViewSet, basename='admin-deliveries')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', admin_login, name='admin-login'),
    path('api/token/refresh/', admin_token_refresh, name='admin-token-refresh'),
    path('api/change-password/', admin_change_password, name='admin-change-password'),
]