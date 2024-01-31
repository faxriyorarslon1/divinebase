from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.product.filter import ProductPaginationPage
from api.users.serializers.hopital import HospitalModelSerializer, CreateHospitalSerializer, HospitalRetrieveSerializer
from apps.users.models import Hospital


class HospitalModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Hospital.objects.all()
    pagination_class = ProductPaginationPage
    serializer_class = HospitalModelSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateHospitalSerializer
        return super(HospitalModelViewSet, self).create(request, *args, **kwargs)

    # @action()
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = HospitalRetrieveSerializer
        # _id = self.request.query_params.get("id")
        # self.queryset = Hospital.objects.get(pk=_id)
        return super(HospitalModelViewSet, self).retrieve(request, *args, **kwargs)

    def get_queryset(self):
        city = self.request.query_params.get('city')
        if city:
            self.queryset = Hospital.objects.filter(city=city)
        else:
            self.queryset = Hospital.objects.all()
        return self.queryset
