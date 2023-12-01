from rest_framework import permissions

from api.models import UserType


class IsPrivateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == UserType.PRIVATE or request.user.is_staff))


class IsPublicUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == UserType.PUBLIC or request.user.is_staff))


class IsVmUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and (request.user.user_type == UserType.PRIVATE_SERVER_VM_USER or request.user.is_staff))
