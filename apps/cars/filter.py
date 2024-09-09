from django_filters import rest_framework as filters

from apps.cars.choices.body_choices import BodyChoices
from apps.cars.choices.currency_choices import CurrencyChoices
from apps.cars.choices.engine_choices import EngineChoices
from apps.cars.choices.transmission_choices import TransmissionChoices


class CarFilter(filters.FilterSet):
    # search
    brand = filters.CharFilter('model__brand__name', lookup_expr='icontains')
    model = filters.CharFilter('model__name', lookup_expr='icontains')

    city = filters.CharFilter('car_profile__city', lookup_expr='icontains')
    # region = filters.CharFilter('car_profile__region')
    description = filters.CharFilter('car_profile__description', lookup_expr='icontains')
    # color = filters.CharFilter('car_profile__color')

    # filter
    year_gte = filters.NumberFilter('year', lookup_expr='gte')
    year_lte = filters.NumberFilter('year', lookup_expr='lte')

    price_gte = filters.NumberFilter('price', lookup_expr='gte')
    price_lte = filters.NumberFilter('price', lookup_expr='lte')

    mileage_gte = filters.NumberFilter('car_profile__mileage', lookup_expr='gte')
    mileage_lte = filters.NumberFilter('car_profile__mileage', lookup_expr='lte')

    engine_capacity_gte = filters.NumberFilter('car_profile__engine_capacity', lookup_expr='gte')
    engine_capacity_lte = filters.NumberFilter('car_profile__engine_capacity', lookup_expr='lte')

    # owner_number_gte = filters.NumberFilter('car_profile__owner_number', lookup_expr='gte')

    currency = filters.ChoiceFilter('currency', choices=CurrencyChoices.choices)
    body = filters.ChoiceFilter('car_profile__body', choices=BodyChoices.choices)
    engine = filters.ChoiceFilter('car_profile__engine', choices=EngineChoices.choices)
    transmission = filters.ChoiceFilter('car_profile__transmission', choices=TransmissionChoices.choices)

    is_new = filters.BooleanFilter('is_new')

    # sort
    order = filters.OrderingFilter(fields=('price', 'year', 'id'))
