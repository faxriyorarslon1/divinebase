from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.hospital_vizit_qoldiq import HospitalVizitOrderSerializer, HospitalVizitOrderExcelSerializer, \
    HospitalVizitOrderOneSerializer
from apps.double_vizit.models import HospitalVizitOrder, HospitalVizitResidueExcel


class HospitalVizitModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalVizitOrderSerializer
    queryset = HospitalVizitOrder.objects.all()

    def hospital_company_is_check(self):
        company = self.request.query_params.get('company')
        queryset = HospitalVizitOrder.objects.filter(company=company).all()
        serializer = HospitalVizitOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = HospitalVizitOrderSerializer
        return super(HospitalVizitModelViewSet, self).update(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def get_one_vizit(self, request):
        user = self.request.user
        company = self.request.query_params.get('company')
        queryset = HospitalVizitOrder.objects.filter(company=company, created_by=user).last()
        serializer = HospitalVizitOrderOneSerializer(queryset)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def hospital_user_create_vizit(self, request):
        user = self.request.user
        company = self.request.query_params.get('company')
        queryset = HospitalVizitOrder.objects.filter(company=company, created_by=user).all()
        serializer = HospitalVizitOrderOneSerializer(queryset, many=True)
        return Response(serializer.data)


class HospitalVizitExcelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalVizitOrderExcelSerializer
    queryset = HospitalVizitResidueExcel.objects.all()
# class HospitalVizitOrderModelViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = HospitalVizitOrderSerializer
#     queryset = HospitalVizitOrder
#     def update(self, request, *args, **kwargs):
#         self.serializer_class = HospitalVizitOrderSerializer
