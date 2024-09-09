from django.urls import path

from apps.cars.views import (
    BrandCreateView,
    BrandDestroyView,
    BrandListView,
    BrandRetrieveView,
    BrandUpdateView,
    CarListView,
)

urlpatterns = [
    path('', CarListView.as_view()),
    # path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
    # path('/<int:pk>/photo', CarAddPhotoView.as_view()),
    path('/brands', BrandListView.as_view(), name='brands-list'),
    path('/brands/create', BrandCreateView.as_view(), name='brand-create'),
    path('/brands/<int:pk>', BrandRetrieveView.as_view(), name='brand-retrieve'),
    path('/brands/<int:pk>/update', BrandUpdateView.as_view(), name='brand-update'),
    path('/brands/<int:pk>/destroy', BrandDestroyView.as_view(), name='brand-destroy'),
]
