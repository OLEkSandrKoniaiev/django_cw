from datetime import timedelta

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions.is_car_owner import IsOwner
from core.permissions.is_car_owner_and_premium import IsOwnerAndPremium
from core.permissions.is_car_owner_or_admin import IsOwnerOrAdmin
from core.permissions.is_premium import IsPremium

from apps.cars.filter import CarFilter
from apps.cars.models import BrandModel, CarModel, CurrencyModel, ModelModel, PriceModel, ViewModel
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

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        car = self.get_object()
        ViewModel.objects.create(car=car)
        return response


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


class CurrencyListView(ListAPIView):
    queryset = CurrencyModel.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        pass


class ViewCountView(APIView):
    permission_classes = (IsOwnerAndPremium,)

    def get(self, request, car_id, period):
        car = get_object_or_404(CarModel, id=car_id)

        self.check_object_permissions(request, car)

        if period == 'day':
            start_date = now() - timedelta(days=1)
        elif period == 'week':
            start_date = now() - timedelta(weeks=1)
        elif period == 'month':
            start_date = now() - timedelta(days=30)
        elif period == 'all_time':
            start_date = None
        else:
            return Response({'error': 'Invalid period'}, status=400)

        if start_date:
            view_count = ViewModel.objects.filter(car=car, created_at__gte=start_date).count()
        else:
            view_count = ViewModel.objects.filter(car=car).count()

        return Response({
            'car_id': car_id,
            'period': period,
            'view_count': view_count
        })


class AveragePriceView(APIView):
    permission_classes = (IsPremium,)

    def get(self, request, model_id, region):
        car_model = get_object_or_404(ModelModel, id=model_id)

        price_queryset = CarModel.objects.filter(model_id=car_model)
        print(price_queryset)

        if region != 'Ukraine':
            price_queryset = price_queryset.filter(car_profile__region=region)

        average_price = price_queryset.aggregate(average_price=Avg('price__price'))['average_price']

        if average_price is None:
            return Response({'error': 'No data found for the specified model or region'}, status=404)

        return Response({
            'model_id': model_id,
            'region': region if region else 'all',
            'average_price': average_price
        })
