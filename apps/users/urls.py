from django.urls import path

from apps.users.views import (
    AdminToUserView,
    PremiumToUserView,
    UserBlockView,
    UserCreateView,
    UserListView,
    UserToAdminView,
    UserToPremiumView,
    UserUnBlockView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/block/', UserBlockView.as_view(), name='user-block'),
    path('users/<int:pk>/unblock/', UserUnBlockView.as_view(), name='user-unblock'),
    path('users/<int:pk>/admin/', UserToAdminView.as_view(), name='user-to-admin'),
    path('users/<int:pk>/remove-admin/', AdminToUserView.as_view(), name='admin-to-user'),
    path('users/<int:pk>/premium/', UserToPremiumView.as_view(), name='user-to-premium'),
    path('users/<int:pk>/remove-premium/', PremiumToUserView.as_view(), name='premium-to-user'),
]
