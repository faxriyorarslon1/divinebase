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
from api.users.serializers.location import LocationModelSerializer, CreateLocationSerializer, LocationDaySerializer, \
    MobileLocationModelSerializer, CreateMobileLocationSerializer
from apps.users.models import Location, User, MobileLocation


class MobileLocationModelViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = MobileLocationModelSerializer
    queryset = MobileLocation.objects.all()
    filter_backends = [filters.DjangoFilterBackend, ]

    def create(self, request, *args, **kwargs):
        serializer = CreateMobileLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'results': serializer.data,
            'message': {
                'status': '200',
                'language': serializer.instance['language']

            }
        }
        return Response(data)

    @action(methods=['get'], detail=False)
    def get_day_location(self, request):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        user = self.request.query_params.get('user')
        district = self.request.query_params.get('district')
        self.queryset = MobileLocation.objects.all()
        if start:
            start = f"{start} 00:00:00{str(datetime.datetime.now())[19:]}"
        if end:
            end = f"{end} 23:59:59{str(datetime.datetime.now())[19:]}"
        if district:
            if start:
                if user:
                    self.queryset = MobileLocation.objects.filter(created_at__gte=start,
                                                                  created_at__lte=end or str(datetime.datetime.now()),
                                                                  created_by=user, district=district).all()
                else:
                    self.queryset = MobileLocation.objects.filter(created_at__gte=start,
                                                                  created_at__lte=end or str(datetime.datetime.now()),
                                                                  district=district).all()
            else:
                if user:
                    self.queryset = MobileLocation.objects.filter(created_by=user, district=district).all()
                else:
                    self.queryset = MobileLocation.objects.filter(district=district).all()

        else:
            if start:
                if user:
                    self.queryset = MobileLocation.objects.filter(created_at__gte=start,
                                                                  created_at__lte=end or str(datetime.datetime.now()),
                                                                  created_by=user).all()
                else:
                    self.queryset = MobileLocation.objects.filter(created_at__gte=start,
                                                                  created_at__lte=end or str(
                                                                      datetime.datetime.now())).all()
            else:
                if user:
                    self.queryset = MobileLocation.objects.filter(created_by=user).all()
                else:
                    self.queryset = MobileLocation.objects.all()

        user_count = User.objects.all().count()
        serializer = LocationDaySerializer(self.queryset, many=True)
        data_list = []
        first = 0
        last = len(serializer.data)
        first_user = 1
        for u in range(0, user_count + 1):
            n_first = 0
            user_dict = {}
            user_all_data = []
            while n_first < last:
                if first_user == serializer.data[n_first].get('created_by').get('id'):
                    user_lan = {'lan': serializer.data[n_first].get('lan'),
                                'lat': serializer.data[n_first].get('lat'),
                                'created_at': serializer.data[n_first].get('created_at')}
                    user_dict = {'created_by': serializer.data[n_first].get('created_by')}
                    user_all_data.append(user_lan)
                n_first += 1
            if user_dict and user_all_data:
                if len(user_all_data) != 0:
                    user_dict['location'] = user_all_data
                data_list.append(user_dict)
            first_user += 1
        if len(serializer.data) == 0:
            data = {
                'results': serializer.data,
                'message': {
                    'status': '200',
                    'language': {
                        'uz': 'Afsuski ma\'lumot topilmadi',
                        'ru': 'Информация не найдена',
                        'cyr': 'Афсуски маълумот топилмади'
                    }
                }
            }
        else:
            data = {
                'results': data_list,
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
