import datetime
import os
from django.http import HttpResponse
from django.shortcuts import redirect
from openpyxl.reader.excel import load_workbook
# from openpyxl.writer.excel import save_virtual_workbook
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from os.path import join

from DivineBase.settings import BASE_DIR
from api.users.serializers.vizit import VizitSerializer, GetVizitSerializer, EXCEL_PATH, VizitExcelSerializer
from apps.users.models import User, District
from apps.vizit.models import Vizit, VizitExcel

credentials = {
    # 'auth_url': 'https://dzokirov20.pythonanywhere.com',
    # 'project': 'DivineBase',
    # 'username': 'DilshodZokirov',
    # 'password': 'Dzokirov2001',
    # 'version': '1'
}


class VizitExcelApi(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = VizitExcel.objects.all()
    serializer_class = VizitExcelSerializer

    @action(methods=['get'], detail=False)
    def district_vizit(self, request, *args, **kwargs):
        district = self.request.query_params.get('district')
        query_set = VizitExcel.objects.filter(district=district).first()
        serializer = VizitExcelSerializer(query_set)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class VizitCreateAPI(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Vizit.objects.all()
    serializer_class = VizitSerializer

    @action(methods=['post'], detail=False)
    def create_vizit(self, request):
        serializer = VizitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'results': serializer.data,
                'message': {
                    'status': '200',
                    'language': {
                        'uz': 'Muoffaqiyatli yaratildi',
                        'ru': 'Создано успешно',
                        'cyr': 'Муоффақиятли яратилди'
                    }
                }
            }
        )

    def list(self, request, *args, **kwargs):
        user = self.request.query_params.get('user')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        district = self.request.query_params.get('district')
        if district:
            if start:
                start = f"{start} 00:00:00{str(datetime.datetime.now())[19:]}"
            if end:
                end = f"{end} 23:59:59{str(datetime.datetime.now())[19:]}"
            if user:
                self.queryset = Vizit.objects.filter(user=user, district=district).all()
                if start:
                    self.queryset = Vizit.objects.filter(user=user, created_date__gte=start, district=district,
                                                         created_date__lte=end or str(datetime.datetime.now())).all()
            else:
                self.queryset = Vizit.objects.filter(district=district).all()
                if start:
                    self.queryset = Vizit.objects.filter(created_date__gte=start, district=district,
                                                         created_date__lte=end or str(datetime.datetime.now())).all()
        else:
            if start:
                start = f"{start} 00:00:00{str(datetime.datetime.now())[19:]}"
            if end:
                end = f"{end} 23:59:59{str(datetime.datetime.now())[19:]}"
            if user:
                self.queryset = Vizit.objects.filter(user=user).all()
                if start:
                    self.queryset = Vizit.objects.filter(user=user, created_date__gte=start,
                                                         created_date__lte=end or str(
                                                             datetime.datetime.now())).all()
            else:
                self.queryset = Vizit.objects.all()
                if start:
                    self.queryset = Vizit.objects.filter(created_date__gte=start,
                                                         created_date__lte=end or str(
                                                             datetime.datetime.now())).all()
        self.serializer_class = GetVizitSerializer
        return super(VizitCreateAPI, self).list(request, *args, **kwargs)
