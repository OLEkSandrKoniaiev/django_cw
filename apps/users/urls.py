from django.urls import path

from apps.users.views import (
    AdminToUserView,
    UserBlockView,
    UserCreateView,
    UserListView,
    UserToAdminView,
    UserUnBlockView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('<int:pk>/block/', UserBlockView.as_view(), name='user-block'),
    path('<int:pk>/un_block/', UserUnBlockView.as_view(), name='user-unblock'),
    path('<int:pk>/admins/', UserToAdminView.as_view(), name='user-to-admin'),
    path('<int:pk>/disadmins/', AdminToUserView.as_view(), name='admin-to-user'),
]
