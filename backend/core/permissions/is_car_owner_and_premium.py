from rest_framework.permissions import BasePermission


class IsOwnerAndPremium(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated or not request.user.is_premium:
            return False
        return obj.user == request.user
