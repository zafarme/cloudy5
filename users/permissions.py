from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser or request.user.role == 'Teacher'


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser or request.user.role == 'Accountant'


class IsSalesManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser or request.user.role == 'Manager'

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user_superuser or request.user.role == 'Superadmin'

