import django_filters

from django_filters import rest_framework as filters

from apps.users.models import Location


class LocationFilter(filters.FilterSet):
    start = filters.IsoDateTimeFilter(field_name="start", lookup_expr='gte')
    end = filters.IsoDateTimeFilter(field_name="end", lookup_expr='lte')

    class Meta:
        model = Location
        fields = 'start', 'end',
