# admin_panel/models.py
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import json


class AdminRole(models.Model):
    """Custom admin roles for fine-grained permissions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, help_text="Store permission configuration as JSON")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_permission(self, permission_key):
        """Check if role has specific permission"""
        return self.permissions.get(permission_key, False)


class AdminUser(models.Model):
    """Extended admin user profile"""
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrator'),
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    custom_role = models.ForeignKey(AdminRole, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Profile information
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    
    # Access control
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    
    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_admins')

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def has_permission(self, permission_key):
        """Check if user has specific permission"""
        if self.role == 'super_admin':
            return True
        
        # Check custom role permissions
        if self.custom_role and self.custom_role.has_permission(permission_key):
            return True
        
        # Default role permissions
        role_permissions = {
            'admin': [
                'view_dashboard', 'manage_customers', 'manage_drivers', 
                'manage_deliveries', 'manage_packages', 'view_reports',
                'manage_settings', 'manage_users'
            ],
            'manager': [
                'view_dashboard', 'manage_customers', 'manage_drivers',
                'manage_deliveries', 'manage_packages', 'view_reports'
            ],
            'operator': [
                'view_dashboard', 'manage_customers', 'manage_deliveries'
            ],
            'viewer': ['view_dashboard', 'view_reports']
        }
        
        return permission_key in role_permissions.get(self.role, [])


class SystemSettings(models.Model):
    """System-wide configuration settings"""
    SETTING_TYPES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    setting_type = models.CharField(max_length=20, choices=SETTING_TYPES, default='string')
    description = models.TextField(blank=True)
    is_editable = models.BooleanField(default=True)
    category = models.CharField(max_length=50, default='general')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'key']
        verbose_name_plural = 'System Settings'

    def __str__(self):
        return f"{self.key} ({self.category})"

    def get_typed_value(self):
        """Return the value with proper type conversion"""
        if self.setting_type == 'integer':
            try:
                return int(self.value)
            except ValueError:
                return 0
        elif self.setting_type == 'float':
            try:
                return float(self.value)
            except ValueError:
                return 0.0
        elif self.setting_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.setting_type == 'json':
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return {}
        else:
            return self.value


class AuditLog(models.Model):
    """Audit log for admin actions"""
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class DeliveryRoute(models.Model):
    """Predefined delivery routes for optimization"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Route definition
    waypoints = models.JSONField(default=list, help_text="List of waypoint coordinates and addresses")
    estimated_distance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    
    # Route settings
    is_active = models.BooleanField(default=True)
    is_optimized = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    """Email/SMS notification templates"""
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    variables = models.JSONField(default=list, help_text="List of available template variables")
    is_active = models.BooleanField(default=True)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class SystemBackup(models.Model):
    """System backup management"""
    BACKUP_TYPES = [
        ('full', 'Full Backup'),
        ('database', 'Database Only'),
        ('media', 'Media Files Only'),
        ('settings', 'Settings Only'),
    ]
    
    BACKUP_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    name = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES)
    status = models.CharField(max_length=20, choices=BACKUP_STATUS, default='pending')
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    
    # Scheduling
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, blank=True, help_text="daily, weekly, monthly")
    next_backup = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
