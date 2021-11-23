from rest_framework import permissions

class IsSuperadmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_admin:
            return True
        return False

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False