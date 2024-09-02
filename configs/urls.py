from django.urls import include, path

urlpatterns = [
    # path('auth', include('apps.auth.urls')),
    # path('car_deals', include('apps.auto_parks.urls')),
    path('cars', include('apps.cars.urls')),
    # path('users', include('apps.users.urls')),
]
