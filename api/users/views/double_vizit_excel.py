from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.double_vizit_excel_serializer import DoubleVizitSerializer
from apps.double_vizit.models import DoubleVizitExcel


class DoubleVizitExcelModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = DoubleVizitExcel.objects.all()
    serializer_class = DoubleVizitSerializer
