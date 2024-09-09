from django.urls import path

from apps.cars.views import (
    BrandCreateView,
    BrandDestroyView,
    BrandListView,
    BrandRetrieveView,
    BrandUpdateView,
    CarCreateView,
    CarDestroyView,
    CarListView,
    CarRetrieveView,
    CarUpdateView,
    ModelCreateView,
    ModelDestroyView,
    ModelListView,
    ModelRetrieveView,
    ModelUpdateView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car-list'),
    path('/create', CarCreateView.as_view(), name='car-create'),
    path('/<int:pk>', CarRetrieveView.as_view(), name='car-retrieve'),
    path('/<int:pk>/update', CarUpdateView.as_view(), name='car-update'),

    path('/<int:pk>/destroy', CarDestroyView.as_view(), name='car-destroy'),
    path('/brands', BrandListView.as_view(), name='brands-list'),
    path('/brands/create', BrandCreateView.as_view(), name='brand-create'),
    path('/brands/<int:pk>', BrandRetrieveView.as_view(), name='brand-retrieve'),
    path('/brands/<int:pk>/update', BrandUpdateView.as_view(), name='brand-update'),
    path('/brands/<int:pk>/destroy', BrandDestroyView.as_view(), name='brand-destroy'),
    path('/models', ModelListView.as_view(), name='models-list'),
    path('/models/create', ModelCreateView.as_view(), name='model-create'),
    path('/models/<int:pk>', ModelRetrieveView.as_view(), name='model-retrieve'),
    path('/models/<int:pk>/update', ModelUpdateView.as_view(), name='model-update'),
    path('/models/<int:pk>/destroy', ModelDestroyView.as_view(), name='model-destroy'),
]
