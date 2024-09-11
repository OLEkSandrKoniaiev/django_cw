from django.contrib.auth import get_user_model

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

from core.permissions.is_super_user_permission import IsSuperUser

from apps.users.serializers import ProfileSerializer, UserSerializer

UserModel = get_user_model()


class UserListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
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


class UserAddPhotoView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = ProfileSerializer

    def patch(self, request, *args, **kwargs):
        profile = self.get_object().profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        if profile.photo:
            profile.photo.delete(save=False)

        serializer.save()
        return Response({'detail': 'Photo updated successfully', 'data': serializer.data})
