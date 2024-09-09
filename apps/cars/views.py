from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.permissions.is_super_user_permission import IsSuperUser
from core.services.email_service import EmailService

from apps.cars.filter import CarFilter
from apps.cars.models import BrandModel, CarModel
from apps.cars.serializers import BrandSerializer, CarSerializer


class CarListView(ListAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)
    filterset_class = CarFilter


class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)


# class CarRetrieveUpdateView(RetrieveUpdateAPIView):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()
#     # permission_classes =


# class CarAddPhotoView(UpdateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = CarPhotoSerializer
#     queryset = CarModel.objects.all()
#     http_method_names = ('put',)
#
#     def perform_update(self, serializer):
#         car = self.get_object()
#         car.photo.delete()
#         super().perform_update(serializer)


class BrandListView(ListAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (AllowAny,)


class BrandCreateView(CreateAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (IsAdminUser,)


class BrandRetrieveView(RetrieveAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (AllowAny,)


class BrandUpdateView(UpdateAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (IsAdminUser,)


class BrandDestroyView(DestroyAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (IsAdminUser,)
