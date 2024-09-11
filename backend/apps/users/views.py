from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import serializers, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permissions.is_super_user_permission import IsSuperUser

from apps.users.serializers import ProfileSerializer, UserSerializer

UserModel = get_user_model()


class UserListView(ListAPIView):
    """
    get:
    Returns a list of all users. Accessible only to admin users.
    """
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(security=[],))
class UserCreateView(CreateAPIView):
    """
    post:
    Allows any user to create a new user account. Open to any user, no authentication required.
    """
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[],))
class UserRetrieveView(RetrieveAPIView):
    """
    get:
    Retrieves details of a specific user by ID. Open to any user, no authentication required.
    """
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    """
    patch:
    Allows authenticated users to update their own profile information. Users can only update their own profiles.
    """
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        if serializer.instance.id != self.request.user.id:
            raise serializers.ValidationError("You can update only your own profile.")

        serializer.save()
        serializer.instance.refresh_from_db()


class UserDestroyView(DestroyAPIView):
    """
    delete:
    Allows authenticated users to delete their own account. Requires correct password confirmation for deletion.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        password = request.data.get('password')
        user = request.user

        if not user.check_password(password):
            return Response({"error": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserBlockView(GenericAPIView):
    """
    patch:
    Allows admin users to block a user by setting their account as inactive. Returns updated user data.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserUnBlockView(GenericAPIView):
    """
    patch:
    Allows admin users to unblock a user by setting their account as active. Returns updated user data.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    """
    patch:
    Allows superusers to promote a user to an admin by setting their `is_staff` flag to `True`. Returns updated user data.
    """
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    """
    patch:
    Allows superusers to demote an admin to a regular user by setting their `is_staff` flag to `False`. Returns updated user data.
    """
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToPremiumView(GenericAPIView):
    """
    patch:
    Allows authenticated users to upgrade their account to premium by setting their `is_premium` flag to `True`. Returns updated user data.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        user = self.request.user

        if not user.is_premium:
            user.is_premium = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class PremiumToUserView(GenericAPIView):
    """
    patch:
    Allows admin users to downgrade a premium user to a regular user by setting their `is_premium` flag to `False`. Returns updated user data.
    """
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if user.is_premium:
            user.is_premium = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
