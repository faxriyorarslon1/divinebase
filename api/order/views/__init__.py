import datetime

from django.db.models import Q
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.order.serializer import GetAllOrderSerializer, UpdateContractNumberSerializer, UpdateStatusSerializer, \
    CompanySerializer, UpdateCompanySerializer, UpdateHospitalVizitSerializer, WebCompanySerializer, \
    WebCompanyCreateSerializer, UpdateWebCompanySerializer, WebOrderSerializer, WebOrderCreateSerializer, \
    WebOrderUpdateSerializer
from api.product.filter import ProductPaginationPage
from apps.order.models import Order, Company


class OrderModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    serializer_class = GetAllOrderSerializer
    filter_backends = [filters.SearchFilter]

    def list(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(seller=request.user)
        self.serializer_class = GetAllOrderSerializer
        return super(OrderModelViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def status_order(self, request):
        status = self.request.query_params.get('status')
        self.queryset = Order.objects.filter(status=status).all()
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def object(self, order_id):
        return Order.objects.get(id=order_id)

    @action(methods=['put'], detail=True)
    def status_update(self, request, *args, **kwargs):
        self.serializer_class = UpdateStatusSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_confirmed_office_manager(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        year = datetime.datetime.now().year
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month), status__isnull=False, finished=False,
                                             ).all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_confirmed_office_manager_send(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        year = datetime.datetime.now().year
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month) & ~Q(status='office_manager') & Q(status__isnull=False), finished=False,
                                             ).all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def send_manager_office_manager(self, request, *args, **kwargs):
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(status__isnull=False, finished=False, seller=request.user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def not_send_manager_office_manager(self, request, *args, **kwargs):
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(finished=False, status__isnull=True, seller=request.user)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def create_excel_hospital_residue(self, request):
        self.serializer_class = UpdateHospitalVizitSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def mp_agent_order_office_manager(self, request):
        user = self.request.query_params.get('user')
        day = self.request.query_params.get('day')
        month = self.request.query_params.get('month')
        year = datetime.datetime.now().year
        order = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month), seller=user, finished=False, )
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def mp_agent_village(self, request):
        district = self.request.query_params.get('district')
        day = self.request.query_params.get('day')
        month = self.request.query_params.get('month')
        year = datetime.datetime.now().year
        order = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month), seller__district=district, finished=False)
        serializer = self.get_serializer(order, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_unreviewed_office_manager(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        year = datetime.datetime.now().year
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month), status__isnull=True, finished=False,
                                             ).all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_unreviewed_office_manager_send(self, request, *args, **kwargs):
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        year = datetime.datetime.now().year
        self.serializer_class = GetAllOrderSerializer
        self.queryset = Order.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month) & Q(status='office_manager'), finished=False,
                                             ).all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def contract_number_update(self, request, *args, **kwargs):
        serializer = UpdateContractNumberSerializer(self.object(kwargs['pk']), data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(methods=['get'], detail=False)
    def get_contract_number(self, request):
        inn = self.request.query_params.get('inn')
        company_name = self.request.query_params.get('company_name')
        created_by = self.request.user
        if company_name:
            self.queryset = Order.objects.filter(company_name__startswith=company_name, seller=created_by,
                                                 finished=False,
                                                 contract_number__isnull=False).first()
        if inn:
            self.queryset = Order.objects.filter(inn=inn, seller=created_by, finished=False,
                                                 contract_number__isnull=False).first()
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def set_contract_number(self, request):
        inn = self.request.query_params.get('inn')
        created_by = self.request.user
        self.queryset = Order.objects.filter(inn=inn, seller=created_by, finished=False,
                                             contract_number__isnull=True).first()
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)

    def get_queryset(self):
        is_manager_send = self.request.query_params.get("manager_send")
        if is_manager_send:
            self.queryset = Order.objects.filter(is_manager_send=False).all()
        else:
            self.queryset = Order.objects.all()
        return self.queryset


class WebOrderModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    serializer_class = WebOrderSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = WebOrderCreateSerializer
        return super(WebOrderModelViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = WebOrderUpdateSerializer
        return super(WebOrderModelViewSet, self).update(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def order_filter_region(self, request):
        self.serializer_class = WebOrderSerializer
        district = self.request.query_params.get('district')
        queryset = Order.objects.filter(district=district)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_filter_reviewed(self, request):
        self.serializer_class = WebOrderSerializer
        queryset = Order.objects.filter(status='office_manager')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def order_filter_unreviewed(self, request):
        self.serializer_class = WebOrderSerializer
        queryset = Order.objects.filter(~Q(status='office_manager'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanyModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = ProductPaginationPage
    search_fields = ['^company_name']

    def get_queryset(self):
        queryset = Company.objects.filter(created_by=self.request.user)
        if queryset:
            return queryset
        return []


class CompanyWebModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WebCompanySerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = WebCompanyCreateSerializer
        return super(CompanyWebModelViewSet, self).create(request, *args, **kwargs)

    # @action(methods=['put'],detail=True)
    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateWebCompanySerializer
        return super(CompanyWebModelViewSet, self).update(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def inn_company(self, request):
        params = self.request.query_params.get('inn')
        queryset = Company.objects.filter(inn_icontains=params)
        serializer = WebCompanySerializer(queryset, many=True)
        return Response(serializer.data)
