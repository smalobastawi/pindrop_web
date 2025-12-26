# core/permissions.py
from rest_framework.permissions import BasePermission
from main.models import UserRole


class HasRolePermission(BasePermission):
    """
    Custom permission to check if user has specific role-based permissions
    """

    def __init__(self, required_permissions=None):
        self.required_permissions = required_permissions or []

    def __call__(self):
        return self

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            user_role = UserRole.objects.get(user=request.user)
            role = user_role.role

            # SuperAdmin has all permissions
            if role.name == 'SuperAdmin':
                return True

            # Check if role has required permissions
            for permission in self.required_permissions:
                if not role.has_permission(permission):
                    return False

            return True

        except UserRole.DoesNotExist:
            return False


def has_permission(user, permission_key):
    """
    Utility function to check if user has a specific permission
    """
    if not user.is_authenticated:
        return False

    try:
        user_role = UserRole.objects.get(user=user)
        return user_role.role.has_permission(permission_key)
    except UserRole.DoesNotExist:
        return False


def get_user_role(user):
    """
    Get user's role name
    """
    if not user.is_authenticated:
        return None

    try:
        user_role = UserRole.objects.get(user=user)
        return user_role.role.name
    except UserRole.DoesNotExist:
        return None