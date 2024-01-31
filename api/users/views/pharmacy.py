from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from api.product.filter import ProductPaginationPage
from api.users.serializers.pharmacy import PharmacyModelSerializer, CreatePharmacySerializer, PharmacyRetrieveSerializer
from apps.users.models import Pharmacy


class PharmacyModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Pharmacy.objects.all()
    pagination_class = ProductPaginationPage
    serializer_class = PharmacyModelSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreatePharmacySerializer
        return super(PharmacyModelViewSet, self).create(request, *args, **kwargs)

    # @action()
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PharmacyRetrieveSerializer
        return super(PharmacyModelViewSet, self).retrieve(request, *args, **kwargs)

    def get_queryset(self):
        city = self.request.query_params.get('city')
        if city:
            self.queryset = Pharmacy.objects.filter(city=city)
        else:
            self.queryset = Pharmacy.objects.all()
        return self.queryset
