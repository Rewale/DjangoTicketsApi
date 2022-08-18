from django_filters import rest_framework as filters
from .models import Flight, Ticket


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class FlightFilter(filters.FilterSet):
    airTo = CharFilterInFilter(field_name='airTo__IATA_code', lookup_expr='in')
    airFrom = CharFilterInFilter(field_name='airFrom__IATA_code', lookup_expr='in')

    class Meta:
        model = Flight
        fields = ['airTo', 'airFrom']