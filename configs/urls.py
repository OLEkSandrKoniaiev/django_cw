from django.urls import path
from apps.cars.views import CarListCreateView, CarRetrieveUpdateDestroyView

urlpatterns = [
    path('cars', CarListCreateView.as_view()),
    path('cars/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
]
