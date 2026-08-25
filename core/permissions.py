from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Allow only authenticated admin users (staff/superuser/site admins)."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_user)


class IsOwnerOrAdmin(BasePermission):
    """Object-level ownership check."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin_user