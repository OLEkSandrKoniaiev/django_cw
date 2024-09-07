from django.urls import path

from .views import DealershipListCreateView

urlpatterns = [
    path('', DealershipListCreateView.as_view(), name='dealership-list-create'),
    # path('create/', DealershipCreateView.as_view(), name='dealership-create'),
]
