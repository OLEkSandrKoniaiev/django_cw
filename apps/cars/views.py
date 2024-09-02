from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer

# class CarListCreateView(GenericAPIView, CreateModelMixin, ListModelMixin):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()
#     def get_queryset(self):
#         return car_filter(self.request.query_params)
#
#     # def get_serializer(self, *args, **kwargs):
#     #     return super().get_serializer(*args, **kwargs)
#     #
#     # def get_object(self):
#     #     return super().get_object()
#
#
#
#     def post(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#
# class CarRetrieveUpdateDestroyView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     serializer_class = CarSerializer
#     queryset = CarModel.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return super().update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


class CarListCreateView(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    queryset = CarModel.objects.all()
