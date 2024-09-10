from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.permissions.is_car_owner import IsOwner
from core.permissions.is_car_owner_or_admin import IsOwnerOrAdmin

from apps.cars.filter import CarFilter
from apps.cars.models import BrandModel, CarModel, ModelModel
from apps.cars.serializers import BrandSerializer, CarProfileSerializer, CarSerializer, ModelSerializer


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

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        message = "Update successful"

        if isinstance(instance, tuple):
            instance, message = instance

        return Response({'detail': message, 'data': CarSerializer(instance).data})


class CarDestroyView(DestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnerOrAdmin,)


class CarAddPhotoView(UpdateAPIView):
    serializer_class = CarProfileSerializer
    queryset = CarModel.objects.all()
    permission_classes = (IsOwnerOrAdmin,)

    def patch(self, request, *args, **kwargs):
        car_profile = self.get_object().car_profile
        serializer = self.get_serializer(car_profile, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        if car_profile.photo:
            car_profile.photo.delete(save=False)

        serializer.save()
        return Response({'detail': 'Photo updated successfully', 'data': serializer.data})
