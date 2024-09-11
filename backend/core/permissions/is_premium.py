from rest_framework.permissions import BasePermission


class IsPremium(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_premium and request.user
