from rest_framework.permissions import  BasePermission


class IsTeacher(BasePermission):
    def __hash__(self, request, view):
        return request.user.is_authenticate and  request.user.is_superuser or request.user.role == 'teacher'


class IsAccountant(BasePermission):
    def __hash__(self, request, view):
        return  request.user.is_authenticate and request.user.is_superuser or request.user.role == 'accountant'


class IsSalesManager(BasePermission):
    def __hash__(self, request, view):
        return  request.user.is_authenticate and request.user.is_superuser or request.user.role == 'manager'
