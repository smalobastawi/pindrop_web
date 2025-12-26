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
from core.logging_utils import log_api_error, log_app_error, log_db_error

from .models import AdminUser, AdminRole, SystemSettings, AuditLog, DeliveryRoute, NotificationTemplate, SystemBackup
from .serializers import (
    AdminUserSerializer, AdminUserCreateSerializer, AdminRoleSerializer, SystemSettingsSerializer,
    AuditLogSerializer, DeliveryRouteSerializer, NotificationTemplateSerializer,
    SystemBackupSerializer, AdminDashboardStatsSerializer, AdminLoginSerializer,
    AdminProfileUpdateSerializer, UserSerializer, UserProfileSerializer
)
from delivery.models import UserProfile, Delivery, Package, Payment
from delivery.serializers import DeliverySerializer, DeliveryCreateSerializer
# Driver is not a separate model, it's part of UserProfile
Driver = UserProfile


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated access for login
def admin_login(request):
    """Admin login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        log_api_error('Username and password required')
        return Response({'error': 'Username and password required'}, status=400)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if not user:
        log_api_error('Invalid credentials')
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
        log_api_error('Refresh token required')
        return Response({'error': 'Refresh token required'}, status=400)
    
    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        return Response({
            'access': access_token
        })
    except Exception as e:
        log_api_error(f'Invalid refresh token: {str(e)}')
        return Response({'error': 'Invalid refresh token'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def admin_change_password(request):
    """Admin change password endpoint"""
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        log_api_error('Old password and new password are required')
        return Response({'error': 'Old password and new password are required'}, status=400)
    
    # Check if user has admin profile
    if not hasattr(request.user, 'admin_profile'):
        log_api_error('User is not an admin')
        return Response({"error": "User is not an admin"}, status=403)
    
    # Verify old password
    if not request.user.check_password(old_password):
        log_api_error('Current password is incorrect')
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
            log_api_error('User does not have an admin profile')
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
            log_api_error(f'Permission denied for {permission_required}')
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
            log_api_error('You can only update your own profile')
            return Response(
                {"error": "You can only update your own profile"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AdminProfileUpdateSerializer(admin_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        log_api_error(f'Serializer errors: {serializer.errors}')
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

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset admin user password"""
        admin_user = self.get_object()

        # Generate a temporary password
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        temp_password = ''.join(secrets.choice(alphabet) for i in range(12))

        # Set the new password
        admin_user.user.set_password(temp_password)
        admin_user.user.save()

        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='reset_password',
            model_name='AdminUser',
            object_id=str(admin_user.id),
            details={'method': 'admin_reset'}
        )

        # In a real implementation, you would send an email with the temp password
        # For now, we'll return it in the response (not recommended for production)
        return Response({
            'message': 'Password reset successfully',
            'temp_password': temp_password  # Remove this in production
        })


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
        try:
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
        except Exception as e:
            log_api_error(f'Error toggling role status: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

    def get_object(self):
        """Override to allow lookup by key"""
        pk = self.kwargs.get('pk')
        if pk and not pk.isdigit():
            # If pk is not numeric, treat it as a key
            try:
                return SystemSettings.objects.get(key=pk)
            except SystemSettings.DoesNotExist:
                raise status.HTTP_404_NOT_FOUND
        return super().get_object()

    @action(detail=False, methods=['post'])
    def upsert(self, request):
        """Create or update a setting by key"""
        key = request.data.get('key')
        if not key:
            return Response({'error': 'Key is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            setting = SystemSettings.objects.get(key=key)
            serializer = self.get_serializer(setting, data=request.data, partial=True)
        except SystemSettings.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK if 'setting' in locals() else status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique categories"""
        try:
            categories = SystemSettings.objects.values_list('category', flat=True).distinct()
            return Response({'categories': list(categories)})
        except Exception as e:
            log_api_error(f'Error fetching categories: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def public_settings(self, request):
        """Get public settings that can be accessed by frontend"""
        try:
            settings = SystemSettings.objects.filter(
                category__in=['public', 'frontend']
            ).values('key', 'value', 'setting_type')
            return Response({'settings': list(settings)})
        except Exception as e:
            log_api_error(f'Error fetching public settings: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        try:
            serializer.save(created_by=self.request.user)
        except Exception as e:
            log_api_error(f'Error creating delivery route: {str(e)}')
            raise
    
    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        """Mark route as optimized"""
        try:
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
        except Exception as e:
            log_api_error(f'Error optimizing route: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        try:
            template = self.get_object()
            template.usage_count += 1
            template.last_used = timezone.now()
            template.save()
            
            return Response({'message': 'Template usage recorded'})
        except Exception as e:
            log_api_error(f'Error using template: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        try:
            serializer.save(created_by=self.request.user)
        except Exception as e:
            log_api_error(f'Error creating system backup: {str(e)}')
            raise
    
    @action(detail=True, methods=['post'])
    def start_backup(self, request, pk=None):
        """Start a backup process"""
        backup = self.get_object()
        
        if backup.status != 'pending':
            log_api_error('Backup is already in progress or completed')
            return Response(
                {'error': 'Backup is already in progress or completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        backup.status = 'running'
        backup.save()
        
        # In a real implementation, you would trigger the actual backup process here
        # For now, we'll just simulate completion
        
        return Response({'message': 'Backup started'})


class AdminDashboardViewSet(AdminPermissionMixin, viewsets.ViewSet):
    """ViewSet for admin dashboard statistics"""
    permission_required = 'view_dashboard'
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics"""
        try:
            # Get basic counts
            total_customers = UserProfile.objects.filter(user_type__in=['customer', 'both']).count()
            total_riders = UserProfile.objects.filter(user_type__in=['rider', 'both']).count()
            pending_riders = UserProfile.objects.filter(user_type__in=['rider', 'both'], status='pending_approval').count()
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
                'total_drivers': total_riders,
                'pending_riders': pending_riders,
                'total_deliveries': total_deliveries,
                'pending_deliveries': pending_deliveries,
                'completed_deliveries_today': completed_deliveries_today,
                'total_revenue_today': float(total_revenue_today),
                'active_drivers': active_riders,
                'delivery_success_rate': round(delivery_success_rate, 2)
            }
            
            serializer = AdminDashboardStatsSerializer(stats)
            return Response(serializer.data)
        except Exception as e:
            log_api_error(f'Error fetching dashboard stats: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def recent_activities(self, request):
        """Get recent admin activities"""
        try:
            limit = int(request.query_params.get('limit', 10))
            activities = AuditLog.objects.select_related('user').order_by('-timestamp')[:limit]
            serializer = AuditLogSerializer(activities, many=True)
            return Response({'activities': serializer.data})
        except Exception as e:
            log_api_error(f'Error fetching recent activities: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def delivery_trends(self, request):
        """Get delivery trends for the last 30 days"""
        try:
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
        except Exception as e:
            log_api_error(f'Error fetching delivery trends: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def driver_performance(self, request):
        """Get driver performance statistics"""
        try:
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
        except Exception as e:
            log_api_error(f'Error fetching driver performance: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RiderManagementViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing riders specifically"""
    permission_required = 'manage_drivers'
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """Filter to only show riders"""
        return Driver.objects.filter(user_type__in=['rider', 'both']).select_related('user').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def pending_approvals(self, request):
        """Get riders pending approval"""
        try:
            pending_riders = self.get_queryset().filter(status='pending_approval')
            serializer = self.get_serializer(pending_riders, many=True)
            return Response({'pending_riders': serializer.data})
        except Exception as e:
            log_api_error(f'Error fetching pending approvals: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            log_api_error('Rider not found during approval')
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
            log_api_error('Rider not found during rejection')
            return Response({'error': 'Rider not found'}, status=404)

    @action(detail=False, methods=['get'])
    def active_riders(self, request):
        """Get active riders for assignment"""
        try:
            active_riders = self.get_queryset().filter(status='active', is_available=True)
            serializer = self.get_serializer(active_riders, many=True)
            return Response({'riders': serializer.data})
        except Exception as e:
            log_api_error(f'Error fetching active riders: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerManagementViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing customers from admin panel"""
    permission_required = 'manage_customers'
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """Filter to only show customers"""
        return Driver.objects.filter(user_type__in=['customer', 'both']).select_related('user').order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserProfileSerializer  # We'll use the same serializer for now
        return UserProfileSerializer

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request):
        """Bulk update customers"""
        customer_ids = request.data.get('customer_ids', [])
        action = request.data.get('action')

        if not customer_ids or not action:
            return Response({'error': 'customer_ids and action are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customers = self.get_queryset().filter(id__in=customer_ids)

            if action == 'toggle_status':
                # Toggle active status for each customer
                for customer in customers:
                    customer.status = 'active' if customer.status == 'inactive' else 'inactive'
                    customer.save()
            elif action == 'activate':
                customers.update(status='active')
            elif action == 'deactivate':
                customers.update(status='inactive')
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': f'Successfully updated {len(customer_ids)} customers'})
        except Exception as e:
            log_api_error(f'Error in bulk update: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Bulk delete customers"""
        customer_ids = request.data.get('customer_ids', [])

        if not customer_ids:
            return Response({'error': 'customer_ids are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customers = self.get_queryset().filter(id__in=customer_ids)
            deleted_count = customers.count()
            customers.delete()

            return Response({'message': f'Successfully deleted {deleted_count} customers'})
        except Exception as e:
            log_api_error(f'Error in bulk delete: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserManagementViewSet(viewsets.ViewSet, AdminPermissionMixin):
    """ViewSet for managing both customers and riders"""
    permission_required = 'manage_customers'
    
    @action(detail=False, methods=['get'])
    def users_summary(self, request):
        """Get summary of all users"""
        try:
            # Get customers
            customers = UserProfile.objects.filter(user_type__in=['customer', 'both'])
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
        except Exception as e:
            log_api_error(f'Error fetching users summary: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def recent_registrations(self, request):
        """Get recent user registrations"""
        try:
            days = int(request.query_params.get('days', 7))
            cutoff_date = timezone.now() - timedelta(days=days)
            
            # Recent customer registrations
            recent_customers = UserProfile.objects.filter(
                user_type__in=['customer', 'both'],
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
                    'name': customer.user.get_full_name(),
                    'email': customer.user.email,
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
        except Exception as e:
            log_api_error(f'Error fetching recent registrations: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeliveryManagementViewSet(viewsets.ModelViewSet, AdminPermissionMixin):
    """ViewSet for managing deliveries from admin panel"""
    permission_required = 'manage_deliveries'
    queryset = Delivery.objects.select_related('sender__user', 'rider__user', 'package', 'payment').all()
    serializer_class = DeliverySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return DeliveryCreateSerializer
        return DeliverySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(tracking_number__icontains=search) |
                Q(sender__user__first_name__icontains=search) |
                Q(sender__user__last_name__icontains=search) |
                Q(sender__user__username__icontains=search) |
                Q(recipient_name__icontains=search) |
                Q(recipient_phone__icontains=search)
            )

        # Status filter
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        # Priority filter
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)

        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def assign_rider(self, request, pk=None):
        """Assign a rider to a delivery"""
        delivery = self.get_object()
        rider_id = request.data.get('rider_id')

        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rider = Driver.objects.get(id=rider_id, user_type__in=['rider', 'both'], status='active')
            delivery.rider = rider
            delivery.status = 'assigned'
            delivery.save()

            # Log the assignment
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Delivery',
                object_id=str(delivery.id),
                details={'action': 'assign_rider', 'rider_id': rider_id}
            )

            serializer = self.get_serializer(delivery)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response({'error': 'Rider not found or not available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update delivery status"""
        delivery = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')

        if not new_status:
            return Response({'error': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in dict(Delivery.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = delivery.status
        delivery.status = new_status
        if notes:
            delivery.notes = notes
        delivery.save()

        # Log the status update
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='Delivery',
            object_id=str(delivery.id),
            details={'field': 'status', 'old_value': old_status, 'new_value': new_status}
        )

        serializer = self.get_serializer(delivery)
        return Response(serializer.data)
