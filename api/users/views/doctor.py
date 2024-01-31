from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.city import DoctorSerializer, CreateDoctorSerializer
from apps.users.models import Doctor, City


class DoctorModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateDoctorSerializer
        return super(DoctorModelViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        city = self.request.query_params.get('hospital_id')
        if city:
            queryset = Doctor.objects.filter(hospital=city).all()
        else:
            queryset = Doctor.objects.all()
        return queryset
