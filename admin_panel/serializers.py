# admin_panel/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import AdminUser, AdminRole, SystemSettings, AuditLog, DeliveryRoute, NotificationTemplate, SystemBackup
from delivery.models import UserProfile
from main.models import Role, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for admin panel"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AdminUserSerializer(serializers.ModelSerializer):
    """Admin user profile serializer"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = AdminUser
        fields = [
            'id', 'user', 'user_id', 'role', 'custom_role', 'phone', 'department',
            'employee_id', 'is_active', 'last_login', 'login_count', 'full_name',
            'email', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_login', 'login_count', 'created_at', 'updated_at']


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating admin users"""
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = AdminUser
        fields = [
            'username', 'email', 'password', 'password_confirm', 'role', 
            'custom_role', 'phone', 'department', 'employee_id'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password and password confirmation don't match.")
        return attrs
    
    def create(self, validated_data):
        # Create user
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password']
        }
        user = User.objects.create_user(**user_data)

        # Create admin profile
        admin_data = {
            'user': user,
            'role': validated_data['role'],
            'custom_role': validated_data.get('custom_role'),
            'phone': validated_data.get('phone', ''),
            'department': validated_data.get('department', ''),
            'employee_id': validated_data.get('employee_id', '')
        }
        admin_user = AdminUser.objects.create(**admin_data)

        # Assign role based on admin role
        role_mapping = {
            'super_admin': 'SuperAdmin',
            'admin': 'Admin',
        }

        role_name = role_mapping.get(validated_data['role'])
        if role_name:
            try:
                role = Role.objects.get(name=role_name)
                UserRole.objects.create(user=user, role=role)
            except Role.DoesNotExist:
                pass  # Role not found, continue without assigning

        return admin_user


class AdminRoleSerializer(serializers.ModelSerializer):
    """Admin role serializer"""
    class Meta:
        model = AdminRole
        fields = ['id', 'name', 'description', 'permissions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemSettingsSerializer(serializers.ModelSerializer):
    """System settings serializer"""
    typed_value = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemSettings
        fields = [
            'id', 'key', 'value', 'setting_type', 'description', 
            'is_editable', 'category', 'typed_value', 'updated_by',
            'updated_at', 'created_at'
        ]
        read_only_fields = ['id', 'updated_at', 'created_at']
    
    def get_typed_value(self, obj):
        return obj.get_typed_value()


class AuditLogSerializer(serializers.ModelSerializer):
    """Audit log serializer"""
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_details', 'action', 'model_name', 'object_id',
            'details', 'ip_address', 'user_agent', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class DeliveryRouteSerializer(serializers.ModelSerializer):
    """Delivery route serializer"""
    created_by_details = UserSerializer(source='created_by', read_only=True)
    waypoints_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryRoute
        fields = [
            'id', 'name', 'description', 'waypoints', 'estimated_distance',
            'estimated_duration', 'is_active', 'is_optimized', 'priority',
            'created_by', 'created_by_details', 'created_at', 'updated_at',
            'waypoints_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'waypoints_count']
    
    def get_waypoints_count(self, obj):
        return len(obj.waypoints) if obj.waypoints else 0


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Notification template serializer"""
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'subject', 'content', 'variables',
            'is_active', 'usage_count', 'last_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'usage_count', 'last_used', 'created_at', 'updated_at']


class SystemBackupSerializer(serializers.ModelSerializer):
    """System backup serializer"""
    created_by_details = UserSerializer(source='created_by', read_only=True)
    file_size_mb = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SystemBackup
        fields = [
            'id', 'name', 'backup_type', 'status', 'status_display', 'file_path',
            'file_size', 'file_size_mb', 'is_scheduled', 'schedule_frequency',
            'next_backup', 'created_by', 'created_by_details', 'created_at',
            'completed_at'
        ]
        read_only_fields = [
            'id', 'status', 'file_path', 'file_size', 'completed_at',
            'created_at'
        ]
    
    def get_file_size_mb(self, obj):
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return None


class AdminDashboardStatsSerializer(serializers.Serializer):
    """Dashboard statistics serializer"""
    total_customers = serializers.IntegerField()
    total_drivers = serializers.IntegerField()
    total_deliveries = serializers.IntegerField()
    pending_deliveries = serializers.IntegerField()
    completed_deliveries_today = serializers.IntegerField()
    total_revenue_today = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_drivers = serializers.IntegerField()
    delivery_success_rate = serializers.FloatField()


class AdminLoginSerializer(serializers.Serializer):
    """Admin login serializer"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating admin profile"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminUser
        fields = ['phone', 'department', 'employee_id']

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.department = validated_data.get('department', instance.department)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile (drivers/riders) in admin panel"""
    user_details = UserSerializer(source='user', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    vehicle_type_display = serializers.CharField(source='get_vehicle_type_display', read_only=True)
    identity_type_display = serializers.CharField(source='get_identity_type_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_details', 'full_name', 'email', 'user_type', 'user_type_display',
            'status', 'status_display', 'phone', 'address', 'profile_image',
            'license_number', 'license_expiry', 'vehicle_type', 'vehicle_type_display',
            'vehicle_plate', 'vehicle_model', 'vehicle_color', 'vehicle_year',
            'identity_type', 'identity_type_display', 'identity_number',
            'is_available', 'current_location', 'last_location_update',
            'rating', 'total_ratings', 'completed_deliveries',
            'working_hours_start', 'working_hours_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']