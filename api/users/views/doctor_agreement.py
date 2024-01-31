from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.doctor_agreement import DoctorAgreeSerializer, DoctorCreateSerializer
from apps.users.models import AgreeDoctor


class ModelDoctorAgreement(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = AgreeDoctor.objects.all()
    serializer_class = DoctorAgreeSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = DoctorCreateSerializer
        return super(ModelDoctorAgreement, self).create(request, *args, **kwargs)
