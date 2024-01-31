from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from api.product.filter import ProductPaginationPage
from api.product.serializers import ProductSerializer, ProductCreateSerializer, UpdateProductSerializer, \
    WebProductSerializer, WebCreateProductSerializer
from apps.product.models import Product


class ProductWebModelApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = WebProductSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = WebCreateProductSerializer
        return super(ProductWebModelApiViewSet, self).create(request, *args, **kwargs)


class ProductApiModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    # pagination_class = ProductPaginationPage
    search_fields = ['^name']

    @action(methods=['get'], detail=False)
    def get_all(self, request):
        self.queryset = Product.objects.all()
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateProductSerializer
        return super(ProductApiModelViewSet, self).update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(active=True).all()
        self.serializer_class = ProductSerializer
        return super(ProductApiModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Product.objects.all()
        return super(ProductApiModelViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = ProductCreateSerializer
        return super(ProductApiModelViewSet, self).create(request, *args, **kwargs)

    # def get_queryset(self):
    #     self.queryset = Product.objects.filter(active=True).all()
    #     return self.queryset