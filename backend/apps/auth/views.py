from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.exceptions.jwt_exception import JwtException
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, ApprovalToken, JWTService, RecoveryToken, SocketToken

from apps.auth.serializers import EmailSerializer, NewEmailSerializer, PasswordSerializer
from apps.users.serializers import UserSerializer

UserModel = get_user_model()


@method_decorator(name='patch', decorator=swagger_auto_schema(security=[],))
class ActiveUserView(GenericAPIView):
    """
    patch:
    This view is used to activate a user's account by verifying a token provided in the URL.
    Once the token is validated, the user is marked as active, and their updated information is returned in the response.
    Accessible to any user, as it doesn't require authentication.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[],))
class RecoveryPasswordRequestView(GenericAPIView):
    """
    post:
    This view handles password recovery requests. It validates the provided email, checks if the user exists,
    and sends a password recovery email if the user is found. The view is open to any user and doesn't require authentication.
    """
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery_email(user)
        return Response({'detail': 'check your email'}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[],))
class RecoverPasswordView(GenericAPIView):
    """
    post:
    Handles password reset requests by validating the provided token and updating the user's password.
    Accessible to any user.
    """
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
    """
    post:
    Handles requests to change a user's email. The user must provide their current password and a new email.
    Sends a confirmation email to the new address. Requires authentication.
    """
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
    """
    post:
    Processes email change confirmation via a token. Verifies the token and updates the user's email.
    Checks for duplicate emails and sends a warning to the old address. Requires authentication.
    """
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


class SocketView(GenericAPIView):
    """
    get:
    Generates and returns a token for socket authentication, allowing the user to connect to WebSocket services.
    Requires authentication.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        token = JWTService.create_token(self.request.user, SocketToken)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
