from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.permissions.is_super_user_permission import IsSuperUser

from apps.users.serializers import ProfileUpdateSerializer, UserDeleteSerializer, UserSerializer

UserModel = get_user_model()


class UserListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDeleteSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.delete()

        return Response({"detail": ""}, status=status.HTTP_204_NO_CONTENT)


class UserBlockView(GenericAPIView):
    permission_classes = (IsAdminUser,)

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

    def patch(self, *args, **kwargs):
        user = self.request.user

        if not user.is_premium:
            user.is_premium = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class PremiumToUserView(GenericAPIView):
    permission_classes = (IsAdminUser,)

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
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user.profile
