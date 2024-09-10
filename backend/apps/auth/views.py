from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.exceptions.jwt_exception import JwtException
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, ApprovalToken, JWTService, RecoveryToken

from apps.auth.serializers import EmailSerializer, NewEmailSerializer, PasswordSerializer
from apps.users.serializers import UserSerializer

UserModel = get_user_model()


class ActiveUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class RecoveryPasswordRequestView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_email(user)
        return Response({'detail': 'check your email'}, status=status.HTTP_200_OK)


class RecoverPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({'detail': 'password was changed'}, status=status.HTTP_200_OK)


class ChangeEmailRequestView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.data['password']):
            return Response({'detail': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

        new_email = data.get('new_email')
        if not new_email:
            return Response({'detail': 'New email is required'}, status=status.HTTP_400_BAD_REQUEST)

        EmailService.approve_email_change(user, new_email)

        return Response({'detail': 'Check your new email for confirmation'}, status=status.HTTP_200_OK)


class ChangeEmailView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewEmailSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        token = kwargs.get('token')
        if not token:
            return Response({'detail': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = JWTService.verify_token(token, ApprovalToken)
        except JwtException as e:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        new_email = data.get('new_email')
        if not new_email:
            return Response({'detail': 'New email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if UserModel.objects.filter(email=new_email).exists():
            return Response({'detail': 'This email is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        EmailService.warning_email(user)
        user.email = new_email
        user.save()

        return Response({'detail': 'Email was successfully changed'}, status=status.HTTP_200_OK)
