from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.city import CitySerializer, CreateCitySerializer
from apps.users.models import City
from rest_framework import filters


class CityModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def get_queryset(self):
        city = self.request.query_params.get('district_id')
        created_by = self.request.query_params.get('created_by')
        if city:
            queryset = City.objects.filter(district=city, created_by=created_by).all()
        else:
            queryset = City.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateCitySerializer
        return super(CityModelViewSet, self).create(request, *args, **kwargs)
