from rest_framework import permissions

class AdminOrStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to all users for list and retrieve operations
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user has admin role for update and delete operations
        return request.user and request.user.role == 'admin'