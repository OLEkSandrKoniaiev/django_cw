from rest_framework.permissions import BasePermission


class IsOwnerAndPremium(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_premium

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
