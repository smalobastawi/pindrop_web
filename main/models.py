from django.db import models
from django.contrib.auth.models import User
import json


class Role(models.Model):
    """User roles with permissions"""
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


class UserRole(models.Model):
    """Link users to roles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_roles')

    class Meta:
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    @property
    def has_permission(self):
        """Delegate permission check to role"""
        return self.role.has_permission
