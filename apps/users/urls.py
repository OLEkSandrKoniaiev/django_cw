from django.urls import path

from apps.users.views import (
    AdminToUserView,
    PremiumToUserView,
    ProfileAddPhotoView,
    ProfileUpdateView,
    UserBlockView,
    UserCreateView,
    UserDestroyView,
    UserListView,
    UserToAdminView,
    UserToPremiumView,
    UserUnBlockView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('/create', UserCreateView.as_view(), name='user-create'),
    path('/delete', UserDestroyView.as_view(), name='user-destroy'),
    path('/<int:pk>/block', UserBlockView.as_view(), name='user-block'),
    path('/<int:pk>/unblock', UserUnBlockView.as_view(), name='user-unblock'),
    path('/<int:pk>/admin', UserToAdminView.as_view(), name='user-to-admin'),
    path('/<int:pk>/remove-admin', AdminToUserView.as_view(), name='admin-to-user'),
    path('/premium', UserToPremiumView.as_view(), name='user-to-premium'),
    path('/<int:pk>/remove-premium', PremiumToUserView.as_view(), name='premium-to-user'),
    path('/profile', ProfileUpdateView.as_view(), name='profile-update'),
    path('/profile/photo', ProfileAddPhotoView.as_view(), name='profile-add-photo'),
]
