from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from core.permissions.is_car_owner import IsOwner
from core.permissions.is_car_owner_or_admin import IsOwnerOrAdmin

from apps.cars.filter import CarFilter
from apps.cars.models import BrandModel, CarModel, ModelModel
from apps.cars.serializers import BrandSerializer, CarSerializer, ModelSerializer


# brand views
class BrandListView(ListAPIView):
    serializer_class = BrandSerializer
    queryset = BrandModel.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


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


# model views
class ModelListView(ListAPIView):
    serializer_class = ModelSerializer
    queryset = ModelModel.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class ModelCreateView(CreateAPIView):
    serializer_class = ModelSerializer
    queryset = ModelModel.objects.all()
    permission_classes = (IsAdminUser,)


class ModelRetrieveView(RetrieveAPIView):
    serializer_class = ModelSerializer
    queryset = ModelModel.objects.all()
    permission_classes = (AllowAny,)


class ModelUpdateView(UpdateAPIView):
    serializer_class = ModelSerializer
    queryset = ModelModel.objects.all()
    permission_classes = (IsAdminUser,)


class ModelDestroyView(DestroyAPIView):
    serializer_class = ModelSerializer
    queryset = ModelModel.objects.all()
    permission_classes = (IsAdminUser,)


# car views
class CarListView(ListAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)
    filterset_class = CarFilter


class CarCreateView(CreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsAuthenticated,)


class CarRetrieveView(RetrieveAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (AllowAny,)


class CarUpdateView(UpdateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwner,)


class CarDestroyView(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnerOrAdmin,)
