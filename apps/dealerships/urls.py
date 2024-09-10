from django.urls import path

from .views import DealershipCreateView, DealershipListView, DealershipRetrieveUpdateDestroyView

urlpatterns = [
    path('', DealershipListView.as_view(), name='dealership-list'),
    path('/create', DealershipCreateView.as_view(), name='dealership-create'),
    path('/<int:pk>', DealershipRetrieveUpdateDestroyView.as_view(), name='dealership-retrieve-update-destroy'),
]
