# admin_panel/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.db import connection
import json
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AdminUser, AdminRole, SystemSettings, AuditLog, DeliveryRoute, NotificationTemplate, SystemBackup
from .serializers import (
    AdminUserSerializer, AdminUserCreateSerializer, AdminRoleSerializer, SystemSettingsSerializer,
    AuditLogSerializer, DeliveryRouteSerializer, NotificationTemplateSerializer,
    SystemBackupSerializer, AdminDashboardStatsSerializer, AdminLoginSerializer,
    AdminProfileUpdateSerializer, UserSerializer
)
from delivery.models import Customer, Driver, Delivery, Package, Payment


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated access for login
def admin_login(request):
    """Admin login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, status=401)
    
    # Check if user has admin profile
    try:
        admin_user = user.admin_profile
    except AdminUser.DoesNotExist:
        return Response({'error': 'User is not an admin'}, status=403)
    
    # Check if admin user is active
    if not admin_user.is_active:
        return Response({'error': 'Admin account is deactivated'}, status=403)
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    # Log the login
    AuditLog.objects.create(
        user=user,
        action='login',
        details={'login_method': 'api'}
    )
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': admin_user.id,
            'username': user.username,
            'email': user.email,
            'role': admin_user.role,
            'full_name': user.get_full_name(),
            'is_active': admin_user.is_active
        }
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated access for token refresh
def admin_token_refresh(request):
    """Admin token refresh endpoint"""
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response({'error': 'Refresh token required'}, status=400)
    
    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        return Response({
            'access': access_token
        })
    except Exception as e:
        return Response({'error': 'Invalid refresh token'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def admin_change_password(request):
    """Admin change password endpoint"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({'error': 'Old password and new password are required'}, status=400)
    
    # Check if user has admin profile
    if not hasattr(request.user, 'admin_profile'):
        return Response({"error": "User is not an admin"}, status=403)
    
    # Verify old password
    if not request.user.check_password(old_password):
        return Response({'error': 'Current password is incorrect'}, status=400)
    
    # Set new password
    request.user.set_password(new_password)
    request.user.save()
    
    # Log the password change
    AuditLog.objects.create(
        user=request.user,
        action='password_change',
        details={'method': 'api'}
    )
    
    return Response({'message': 'Password changed successfully'})


class AdminPermissionMixin:
    """Mixin to handle admin permissions"""
    
    def check_permission(self, permission_key):
        """Check if current admin user has specific permission"""
        if not hasattr(self.request.user, 'admin_profile'):
            return False
        
        admin_user = self.request.user.admin_profile
        return admin_user.has_permission(permission_key)
    
    def get_permission_required(self):
        """Get required permission for this view"""
        return getattr(self, 'permission_required', None)
    
    def check_permissions(self, request):
        """Override to add admin permission check"""
        super().check_permissions(request)
        
        permission_required = self.get_permission_required()
        if permission_required and not self.check_permission(permission_required):
            self.permission_denied(
                request,
                message="You don't have permission to access this resource."
            )


class AdminUserViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing admin users"""
    permission_required = 'manage_users'
    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.select_related('user', 'custom_role').all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSerializer
        return AdminUserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by role if specified
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current admin user profile"""
        if not hasattr(request.user, 'admin_profile'):
            return Response(
                {"error": "User is not an admin"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(request.user.admin_profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def update_profile(self, request, pk=None):
        """Update current admin user profile"""
        admin_user = self.get_object()
        
        if admin_user.user != request.user:
            return Response(
                {"error": "You can only update your own profile"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AdminProfileUpdateSerializer(admin_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle admin user active status"""
        admin_user = self.get_object()
        admin_user.is_active = not admin_user.is_active
        admin_user.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='AdminUser',
            object_id=str(admin_user.id),
            details={'field': 'is_active', 'new_value': admin_user.is_active}
        )
        
        serializer = self.get_serializer(admin_user)
        return Response(serializer.data)


class AdminRoleViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing admin roles"""
    permission_required = 'manage_users'
    serializer_class = AdminRoleSerializer
    queryset = AdminRole.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle role active status"""
        role = self.get_object()
        role.is_active = not role.is_active
        role.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='AdminRole',
            object_id=str(role.id),
            details={'field': 'is_active', 'new_value': role.is_active}
        )
        
        serializer = self.get_serializer(role)
        return Response(serializer.data)


class SystemSettingsViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing system settings"""
    permission_required = 'manage_settings'
    serializer_class = SystemSettingsSerializer
    queryset = SystemSettings.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category if specified
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique categories"""
        categories = SystemSettings.objects.values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})
    
    @action(detail=False, methods=['get'])
    def public_settings(self, request):
        """Get public settings that can be accessed by frontend"""
        settings = SystemSettings.objects.filter(
            category__in=['public', 'frontend']
        ).values('key', 'value', 'setting_type')
        return Response({'settings': list(settings)})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet, AdminPermissionMixin):
    """ViewSet for viewing audit logs"""
    permission_required = 'view_reports'
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.select_related('user').all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user if specified
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by action if specified
        action = self.request.query_params.get('action', None)
        if action:
            queryset = queryset.filter(action=action)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__date__gte=start_date.date())
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__date__lte=end_date.date())
            except ValueError:
                pass
        
        return queryset


class DeliveryRouteViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing delivery routes"""
    permission_required = 'manage_deliveries'
    serializer_class = DeliveryRouteSerializer
    queryset = DeliveryRoute.objects.select_related('created_by').all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        """Mark route as optimized"""
        route = self.get_object()
        route.is_optimized = True
        route.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='DeliveryRoute',
            object_id=str(route.id),
            details={'action': 'optimized'}
        )
        
        serializer = self.get_serializer(route)
        return Response(serializer.data)


class NotificationTemplateViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing notification templates"""
    permission_required = 'manage_settings'
    serializer_class = NotificationTemplateSerializer
    queryset = NotificationTemplate.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by template type
        template_type = self.request.query_params.get('template_type', None)
        if template_type:
            queryset = queryset.filter(template_type=template_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """Increment template usage count"""
        template = self.get_object()
        template.usage_count += 1
        template.last_used = timezone.now()
        template.save()
        
        return Response({'message': 'Template usage recorded'})


class SystemBackupViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing system backups"""
    permission_required = 'manage_settings'
    serializer_class = SystemBackupSerializer
    queryset = SystemBackup.objects.select_related('created_by').all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by backup type
        backup_type = self.request.query_params.get('backup_type', None)
        if backup_type:
            queryset = queryset.filter(backup_type=backup_type)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start_backup(self, request, pk=None):
        """Start a backup process"""
        backup = self.get_object()
        
        if backup.status != 'pending':
            return Response(
                {'error': 'Backup is already in progress or completed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        backup.status = 'running'
        backup.save()
        
        # In a real implementation, you would trigger the actual backup process here
        # For now, we'll just simulate completion
        
        return Response({'message': 'Backup started'})


class AdminDashboardViewSet(viewsets.ViewSet, AdminPermissionMixin):
    """ViewSet for admin dashboard statistics"""
    permission_required = 'view_dashboard'
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics"""
        # Get basic counts
        total_customers = Customer.objects.filter(user_type__in=['customer', 'both']).count()
        total_riders = Driver.objects.count()
        pending_riders = Driver.objects.filter(status='pending_approval').count()
        total_deliveries = Delivery.objects.count()
        
        # Get pending deliveries
        pending_deliveries = Delivery.objects.filter(
            status__in=['pending', 'assigned', 'picked_up', 'in_transit']
        ).count()
        
        # Get today's completed deliveries
        today = timezone.now().date()
        completed_deliveries_today = Delivery.objects.filter(
            status='delivered',
            actual_delivery__date=today
        ).count()
        
        # Get today's revenue
        total_revenue_today = Payment.objects.filter(
            status='paid',
            paid_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get active riders
        active_riders = Driver.objects.filter(status='active', is_available=True).count()
        
        # Calculate delivery success rate
        total_deliveries_30_days = Delivery.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        successful_deliveries_30_days = Delivery.objects.filter(
            status='delivered',
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        delivery_success_rate = 0
        if total_deliveries_30_days > 0:
            delivery_success_rate = (successful_deliveries_30_days / total_deliveries_30_days) * 100
        
        stats = {
            'total_customers': total_customers,
            'total_riders': total_riders,
            'pending_riders': pending_riders,
            'total_deliveries': total_deliveries,
            'pending_deliveries': pending_deliveries,
            'completed_deliveries_today': completed_deliveries_today,
            'total_revenue_today': float(total_revenue_today),
            'active_riders': active_riders,
            'delivery_success_rate': round(delivery_success_rate, 2)
        }
        
        serializer = AdminDashboardStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_activities(self, request):
        """Get recent admin activities"""
        limit = int(request.query_params.get('limit', 10))
        activities = AuditLog.objects.select_related('user').order_by('-timestamp')[:limit]
        serializer = AuditLogSerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def delivery_trends(self, request):
        """Get delivery trends for the last 30 days"""
        days = int(request.query_params.get('days', 30))
        
        # Get delivery counts for the last N days
        trend_data = []
        for i in range(days):
            date = timezone.now().date() - timedelta(days=i)
            
            created_count = Delivery.objects.filter(
                created_at__date=date
            ).count()
            
            completed_count = Delivery.objects.filter(
                status='delivered',
                actual_delivery__date=date
            ).count()
            
            trend_data.append({
                'date': date.isoformat(),
                'created': created_count,
                'completed': completed_count
            })
        
        return Response({'trends': trend_data})
    
    @action(detail=False, methods=['get'])
    def driver_performance(self, request):
        """Get driver performance statistics"""
        drivers = Driver.objects.select_related('user').annotate(
            total_deliveries=Count('delivery'),
            completed_deliveries=Count('delivery', filter=Q(delivery__status='delivered')),
            pending_deliveries=Count('delivery', filter=Q(delivery__status__in=['pending', 'assigned', 'picked_up', 'in_transit']))
        ).order_by('-completed_deliveries')[:10]
        
        driver_data = []
        for driver in drivers:
            total = driver.total_deliveries
            completed = driver.completed_deliveries
            success_rate = (completed / total * 100) if total > 0 else 0
            
            driver_data.append({
                'id': driver.id,
                'name': driver.user.get_full_name() or driver.user.username,
                'total_deliveries': total,
                'completed_deliveries': completed,
                'pending_deliveries': driver.pending_deliveries,
                'success_rate': round(success_rate, 2),
                'is_available': driver.is_available
            })
        
        return Response({'drivers': driver_data})

class RiderManagementViewSet(viewsets.ViewSet, AdminPermissionMixin):
    """ViewSet for managing riders specifically"""
    permission_required = 'manage_drivers'
    
    @action(detail=False, methods=['get'])
    def pending_approvals(self, request):
        """Get riders pending approval"""
        pending_riders = Driver.objects.filter(
            status='pending_approval'
        ).select_related('user', 'customer')
        
        rider_data = []
        for rider in pending_riders:
            rider_data.append({
                'id': rider.id,
                'name': rider.customer.name if rider.customer else rider.user.get_full_name(),
                'email': rider.user.email,
                'phone': rider.customer.phone if rider.customer else '',
                'license_number': rider.license_number,
                'vehicle_type': rider.vehicle_type,
                'vehicle_plate': rider.vehicle_plate,
                'vehicle_model': rider.vehicle_model,
                'applied_date': rider.created_at,
            })
        
        return Response({'pending_riders': rider_data})
    
    @action(detail=True, methods=['post'])
    def approve_rider(self, request, pk=None):
        """Approve a rider"""
        try:
            rider = Driver.objects.get(pk=pk)
            rider.status = 'active'
            rider.save()
            
            # Log the approval
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Driver',
                object_id=str(rider.id),
                details={'action': 'approved', 'status': 'active'}
            )
            
            return Response({'message': 'Rider approved successfully'})
        except Driver.DoesNotExist:
            return Response({'error': 'Rider not found'}, status=404)
    
    @action(detail=True, methods=['post'])
    def reject_rider(self, request, pk=None):
        """Reject a rider"""
        reason = request.data.get('reason', 'Application rejected')
        
        try:
            rider = Driver.objects.get(pk=pk)
            rider.status = 'suspended'
            rider.save()
            
            # Log the rejection
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Driver',
                object_id=str(rider.id),
                details={'action': 'rejected', 'reason': reason}
            )
            
            return Response({'message': 'Rider rejected successfully'})
        except Driver.DoesNotExist:
            return Response({'error': 'Rider not found'}, status=404)

class UserManagementViewSet(viewsets.ViewSet, AdminPermissionMixin):
    """ViewSet for managing both customers and riders"""
    permission_required = 'manage_customers'
    
    @action(detail=False, methods=['get'])
    def users_summary(self, request):
        """Get summary of all users"""
        # Get customers
        customers = Customer.objects.all()
        customer_summary = {
            'total': customers.count(),
            'active': customers.filter(status='active').count(),
            'inactive': customers.filter(status='inactive').count(),
            'suspended': customers.filter(status='suspended').count()
        }
        
        # Get riders
        riders = Driver.objects.all()
        rider_summary = {
            'total': riders.count(),
            'active': riders.filter(status='active').count(),
            'pending_approval': riders.filter(status='pending_approval').count(),
            'suspended': riders.filter(status='suspended').count(),
            'available': riders.filter(status='active', is_available=True).count()
        }
        
        return Response({
            'customers': customer_summary,
            'riders': rider_summary
        })
    
    @action(detail=False, methods=['get'])
    def recent_registrations(self, request):
        """Get recent user registrations"""
        days = int(request.query_params.get('days', 7))
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Recent customer registrations
        recent_customers = Customer.objects.filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:10]
        
        # Recent rider registrations
        recent_riders = Driver.objects.filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:10]
        
        customer_data = []
        for customer in recent_customers:
            customer_data.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'user_type': customer.user_type,
                'status': customer.status,
                'registered_at': customer.created_at
            })
        
        rider_data = []
        for rider in recent_riders:
            rider_data.append({
                'id': rider.id,
                'name': rider.user.get_full_name(),
                'email': rider.user.email,
                'vehicle_type': rider.vehicle_type,
                'vehicle_plate': rider.vehicle_plate,
                'status': rider.status,
                'registered_at': rider.created_at
            })
        
        return Response({
            'recent_customers': customer_data,
            'recent_riders': rider_data
        })
