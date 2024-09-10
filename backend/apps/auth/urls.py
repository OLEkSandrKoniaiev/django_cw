from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.views import (
    ActiveUserView,
    ChangeEmailRequestView,
    ChangeEmailView,
    RecoverPasswordView,
    RecoveryPasswordRequestView,
)

urlpatterns = [
    path('', TokenObtainPairView.as_view()),
    path('/refresh', TokenRefreshView.as_view()),
    path('/activate/<str:token>', ActiveUserView.as_view()),
    path('/recovery-password', RecoveryPasswordRequestView.as_view()),
    path('/recovery-password/<str:token>', RecoverPasswordView.as_view()),
    path('/change-email', ChangeEmailRequestView.as_view()),
    path('/change-email/<str:token>', ChangeEmailView.as_view()),
]
