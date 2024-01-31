import datetime

from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.check_mp import CheckMpSerializer, CheckMpCreateVizitSerializer, \
    CheckMpCreatePharmacySerializer, CheckMpPostSerializer
from apps.users.models import CheckMp


class CheckMpModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = CheckMp.objects.all()
    serializer_class = CheckMpSerializer
    filter_backends = [filters.SearchFilter]

    @action(methods=['post'], detail=False)
    def create_vizit(self, request, *args, **kwargs):
        self.serializer_class = CheckMpCreateVizitSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response("Success")

    @action(methods=['post'], detail=False)
    def create_pharmacy(self, request, *args, **kwargs):
        self.serializer_class = CheckMpCreatePharmacySerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response("Success")

    def list(self, request, *args, **kwargs):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        user = self.request.query_params.get('user')
        district = self.request.query_params.get('district')
        if start:
            start = f"{start} 00:00:00{str(datetime.datetime.now())[19:]}"
        if end:
            end = f"{end} 23:59:59{str(datetime.datetime.now())[19:]}"
        if user:
            if district:
                if start:
                    self.queryset = CheckMp.objects.filter(created_at__gte=start,
                                                           created_at__lte=end or str(datetime.datetime.now()),
                                                           created_by=user, district=district).all()
                else:
                    self.queryset = CheckMp.objects.filter(created_by=user, district=district).all()
            else:
                if start:
                    self.queryset = CheckMp.objects.filter(created_at__gte=start,
                                                           created_at__lte=end or str(datetime.datetime.now()),
                                                           created_by=user).all()
                else:
                    self.queryset = CheckMp.objects.filter(created_by=user).all()
        else:
            if district:
                if start:
                    self.queryset = CheckMp.objects.filter(created_at__gte=start, district=district,
                                                           created_at__lte=end or str(datetime.datetime.now()),
                                                           ).all()
                else:
                    self.queryset = CheckMp.objects.filter(district=district).all()
            else:
                if start:
                    self.queryset = CheckMp.objects.filter(created_at__gte=start,
                                                           created_at__lte=end or str(datetime.datetime.now()),
                                                           ).all()
                else:
                    self.queryset = CheckMp.objects.all()
        return super(CheckMpModelViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CheckMpPostSerializer
        return super(CheckMpModelViewSet, self).create(request, *args, **kwargs)
