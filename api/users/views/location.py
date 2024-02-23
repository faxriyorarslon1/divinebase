# from requests import Response
import datetime

from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from api.users.location_filter import LocationFilter
from api.users.serializers.location import LocationModelSerializer, CreateLocationSerializer, LocationDaySerializer
from apps.users.models import Location, User


class LocationModelViewSet(ModelViewSet):
    # authentication_classes = TokenAuthentication
    permission_classes = [AllowAny, ]
    serializer_class = LocationModelSerializer
    queryset = Location.objects.all()
    filter_backends = [filters.DjangoFilterBackend, ]

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateLocationSerializer
        return super(LocationModelViewSet, self).create(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def get_day_user_location(self, request):
        year = self.request.query_params.get('year')
        year = int(year)
        day = self.request.query_params.get('day')
        day = int(day)
        user = self.request.query_params.get('user_id')
        month = self.request.query_params.get('month')
        month = int(month)
        start_date = datetime.datetime(year=year, month=month, day=day, hour=0, minute=0,
                                       second=0)
        end_date = datetime.datetime(year=year, month=month, day=day, hour=23, minute=59,
                                     second=59)
        self.queryset = Location.objects.filter(created_at__gte=start_date,
                                                created_at__lte=end_date,
                                                created_by=user).all()
        serializer = LocationDaySerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_day_location(self, request):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        user = self.request.query_params.get('user')
        district = self.request.query_params.get('district')
        day = self.request.query_params.get('day')
        month = self.request.query_params.get('month')
        user_id = self.request.query_params.get('user_id')
        year = self.request.query_params.get('year')

        if start:
            start = f"{start} 00:00:00{str(datetime.datetime.now())[19:]}"
        if end:
            end = f"{end} 23:59:59{str(datetime.datetime.now())[19:]}"
        if user:
            if district:
                if start:
                    self.queryset = Location.objects.filter(created_at__gte=start,
                                                            created_at__lte=end or str(datetime.datetime.now()),
                                                            created_by=user, district=district).all()
                else:
                    self.queryset = Location.objects.filter(created_by=user, district=district).all()
            else:
                if start:
                    self.queryset = Location.objects.filter(created_at__gte=start,
                                                            created_at__lte=end or str(datetime.datetime.now()),
                                                            created_by=user).all()
                else:
                    self.queryset = Location.objects.filter(created_by=user).all()
        else:
            if district:
                if start:
                    self.queryset = Location.objects.filter(created_at__gte=start, district=district,
                                                            created_at__lte=end or str(datetime.datetime.now()),
                                                            ).all()
                else:
                    self.queryset = Location.objects.filter(district=district).all()
            else:
                if start:
                    self.queryset = Location.objects.filter(created_at__gte=start,
                                                            created_at__lte=end or str(datetime.datetime.now()),
                                                            ).all()
                else:
                    self.queryset = Location.objects.all()
        if day and month and user_id:
            self.queryset = Location.objects.filter(created_by=user_id).filter(created_at__day=day,
                                                                               created_at__month=month,
                                                                               created_at__year=year)
        serializer = LocationDaySerializer(self.queryset, many=True)
        data = {
            'results': serializer.data,
            'message': {
                'status': '200',
                'language': {
                    'uz': 'Hammasi ajoyib',
                    'ru': 'Все отлично',
                    'cyr': 'Ҳаммаси ажойиб'
                }
            }
        }
        return Response(data)

    def get_queryset(self):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        user = self.request.query_params.get("user")
        if start and end:
            queryset = Location.objects.filter(created_at__gte=start, created_at__lte=end, created_by=user)
        else:
            queryset = Location.objects.filter(created_by=user)
        return queryset
