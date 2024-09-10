from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView, UpdateAPIView
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


class ProfileUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileAddPhotoView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        profile = self.get_object()
        profile.photo.delete()
        super().perform_update(serializer)
