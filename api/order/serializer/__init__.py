import datetime
import json
from os.path import join as join_path
import openpyxl
import requests
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api.product.serializers import ProductSerializer, ProductItemSerializer
from api.users.serializers.vizit import check_excel
from apps.order.models import OrderItem, Order, Company
from apps.product.models import Product

from rest_framework import serializers

from apps.users.models import User, District
from utils import EXCEL_PATH, HOSPITAL_EXCEL_PATH


def requests_facture():
    url = "https://account.faktura.uz/token"
    grant_type = "password"
    try:
        reload = requests.post(url=url,
                               data={"grant_type": grant_type, "username": "998909972900",
                                     "password": "fwgfactura",
                                     "client_id": '998909972900',
                                     "client_secret": "aCMaZxb8aN8RmOH7CuaEz76WUDKtaIKdzKNn0SKrPZJ4m0uebDkalukN8ngP"},
                               headers={"Content-Type": "application/json"})

        return json.loads(reload.text)
    except Exception:
        return {"message": "Error"}


class WebCompanyCreateSerializer(ModelSerializer):
    company_director_name = serializers.CharField(required=False, max_length=255)
    company_director_phone_number = serializers.CharField(required=False, max_length=255)
    company_provider_name = serializers.CharField(required=False, max_length=255)
    company_provider_phone_number = serializers.CharField(required=False, max_length=255)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    company_name = serializers.CharField(max_length=255, required=False)
    company_address = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=255, required=False)
    bank_name = serializers.CharField(max_length=255, required=False)
    inn = serializers.CharField(max_length=255)

    class Meta:
        model = Company
        fields = [
            'id',
            'created_by',
            "company_name",
            "company_address",
            'phone_number',
            "bank_name",
            'inn',
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class WebCompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'created_by',
            "company_name",
            "company_address",
            'phone_number',
            "bank_name",
            'inn',
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class CompanyCreateSerializer(ModelSerializer):
    company_director_name = serializers.CharField(required=False, max_length=255)
    company_director_phone_number = serializers.CharField(required=False, max_length=255)
    company_provider_name = serializers.CharField(required=False, max_length=255)
    company_provider_phone_number = serializers.CharField(required=False, max_length=255)

    class Meta:
        model = Company
        fields = [
            "id",
            'created_by',
            "company_name",
            "company_address",
            'phone_number',
            "bank_name",
            'inn',
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            'created_by',
            "company_name",
            "company_address",
            'phone_number',
            "bank_name",
            'inn',
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class OrderItemOrderSerializer(ModelSerializer):
    product = ProductItemSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'count',
            "product",
            "price"
        ]


class OrderItemCreateOrderSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'count',
            "product",
            "price"
        ]


class WebOrderSerializer(ModelSerializer):
    products = OrderItemOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'seller',
            'district',
            'products',
            'inn',
            'phone_number',
            'status',
            'comment',
            'total_price',
            'type_price',
            'created_date'
        ]


class WebOrderCreateSerializer(ModelSerializer):
    products = OrderItemCreateOrderSerializer(many=True, required=False)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    total_price = serializers.CharField(max_length=255)
    type_price = serializers.CharField(max_length=255)
    comment = serializers.CharField(max_length=500)

    class Meta:
        model = Order
        fields = [
            "inn",
            "seller",
            "phone_number",
            "district",
            "status",
            'total_price',
            'comment',
            'type_price',
            'products'
        ]

    def create(self, validated_data):
        order_data = validated_data.pop('products')
        validated_data['seller'] = self.context['request'].user
        # validated_data['district'] = self.context['request'].user.district
        order = Order.objects.create(**validated_data)
        for person in order_data:
            d = dict(person)
            OrderItem.objects.create(order=order, product=d.get('product'), count=d.get('count'),
                                     price=d.get('price'))
        return order


class WebOrderUpdateSerializer(serializers.ModelSerializer):
    products = OrderItemCreateOrderSerializer(many=True, required=False)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    total_price = serializers.CharField(max_length=255, required=False)
    type_price = serializers.CharField(max_length=255, required=False)
    comment = serializers.CharField(max_length=500, required=False)
    status = serializers.CharField(max_length=255, required=False)
    inn = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=255, required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)

    class Meta:
        model = Order
        fields = [
            "inn",
            "seller",
            "phone_number",
            "district",
            "status",
            'total_price',
            'comment',
            'type_price',
            'products',
        ]

    def update(self, instance, validated_data):
        person_data = validated_data.pop('products')
        for item in validated_data:
            if Order._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        OrderItem.objects.filter(order=instance).delete()
        for person in person_data:
            d = dict(person)
            OrderItem.objects.create(order=instance, product=d['product'], count=d.get('count'),
                                     price=d.get('price'))
        instance.save()
        return instance


class UpdateWebCompanySerializer(ModelSerializer):
    company_director_phone_number = serializers.CharField(max_length=255, required=False)
    company_director_name = serializers.CharField(max_length=255, required=False)
    company_provider_phone_number = serializers.CharField(max_length=255, required=False)
    company_provider_name = serializers.CharField(max_length=255, required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    company_name = serializers.CharField(max_length=255, required=False)
    company_address = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=255, required=False)
    bank_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Company
        fields = [
            "id",
            'created_by',
            "company_name",
            "company_address",
            'phone_number',
            "bank_name",
            'inn',
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class UpdateCompanySerializer(ModelSerializer):
    company_director_phone_number = serializers.CharField(max_length=255, required=False)
    company_director_name = serializers.CharField(max_length=255, required=False)
    company_provider_phone_number = serializers.CharField(max_length=255, required=False)
    company_provider_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Company
        fields = [
            'company_director_phone_number',
            'company_director_name',
            'company_provider_name',
            'company_provider_phone_number'
        ]


class GetAllOrderSerializer(ModelSerializer):
    products = OrderItemOrderSerializer(many=True, required=False)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "products",
            "seller",
            'inn',
            "comment",
            "total_price",
            "type_price",
            "company_name",
            "company_address",
            "phone_number",
            "bank_name",
            "is_manager_send",
            "contract_number",
            'create_contract_number',
            "status",
            'created_date'
        ]

    def create(self, validated_data):
        order_data = validated_data.pop('products')
        validated_data['seller'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        for person in order_data:
            d = dict(person)
            OrderItem.objects.create(order=order, product=d.get('product'), count=d.get('count'),
                                     price=d.get('price'))
        return order

    def update(self, instance, validated_data):
        person_data = validated_data.pop('products')
        for item in validated_data:
            if Order._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        OrderItem.objects.filter(order=instance).delete()
        for person in person_data:
            d = dict(person)
            OrderItem.objects.create(order=instance, product=d['product'], count=d.get('count'),
                                     price=d.get('price'))
        instance.save()
        return instance


class UpdateContractNumberSerializer(serializers.ModelSerializer):
    contract_number = serializers.CharField(max_length=400)
    inn = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "company_name",
            "inn",
            'contract_number',
            "create_contract_number"
        ]

    def validate(self, attrs):
        self.instance.create_contract_number = datetime.datetime.now()
        self.instance.contract_number = attrs.get('contract_number')
        self.instance.save()
        return attrs

    # def update(self, instance: Order, validated_data: dict):
    #     instance.create_contract_number = datetime.datetime.now()
    #     instance.contract_number = validated_data.get('contract_number')
    #     instance.save()
    #     return instance


class UpdateStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=200)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    inn = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, attrs):
        self.instance.status = attrs.get('status')
        if attrs.get('status').__eq__('manager'):
            self.instance.finished = True
        self.instance.save()
        return attrs

    #
    # print(create_hospital_all_excel('2023/10/20', created_by="Dilshod Zokirov", director_phone_number='+998904323',
    #                                 intrizol=45))

    # check_excel_params = check_excel(EXCEL_PATH, excel_path)
    # if check_excel_params.__eq__("file yoq"):
    #     book1 = openpyxl.Workbook()
    #     sheet1 = book1.active
    #     columns = [
    #         "Vaqti",  # 1
    #         'Kimdan',  # 2
    #         "Viloyat",  # 3
    #         'INN',  # 4
    #         'Dorixona nomi',  # 5
    #         'Bron berilgan kun',  # 6
    #         'Акнель гель 10гр q-ty',  # 7
    #         'Астароксон TZ-1125  q-ty',  # 8
    #         "Астароксон TZ-562,5 q-ty",
    #         "Астарюс 20мг/мл амп. 5мл №5 q-ty",
    #         "Интризол крем 20гр q-ty",
    #         "Ливомед таб №60 q-ty",  # 12
    #         "Ливомед сироп 200мл q-ty",
    #         "Ренум капс. 250мг №60 q-ty",
    #         "Стрессон капс №20 q-ty",  # 15
    #         "ТАВАМЕД 500мг инфузия 100мл  q-ty",
    #         "Х-пайлс мазь 30г q-ty",
    #         "Цепразон 1,5г q-ty",  # 18
    #         "Энтро Д капс №10 q-ty",
    #         "Энтро Д саше №10 q-ty",
    #         "Ламино 100 мл q-ty",  # 21
    #         'Ламино 200 мл q-ty',
    #         'Summa',
    #         'Direktor FIO',  # 24
    #         'Direktor telefon nomeri',
    #         'Farmasevt FIO',
    #         'Farmasevt telefon nomeri',  # 27
    #
    #         'Izoh'
    #     ]
    #     sheet1['A1'] = columns[0]
    #     sheet1["B1"] = columns[1]
    #     sheet1["C1"] = columns[2]
    #     sheet1["D1"] = columns[3]
    #     sheet1["E1"] = columns[4]
    #     sheet1["F1"] = columns[5]
    #     sheet1["G1"] = columns[6]
    #     sheet1['H1'] = columns[7]
    #     sheet1['I1'] = columns[8]
    #     sheet1['J1'] = columns[9]
    #     sheet1['K1'] = columns[10]
    #     book1.save(f'{join_path(EXCEL_PATH, excel_path)}')
    #     book = openpyxl.load_workbook(f'{join_path(EXCEL_PATH, excel_path)}')
    #     sheet = book.active
    #     sheet.column_dimensions['A'].width = 30
    #     sheet.column_dimensions['B'].width = 30
    #     sheet.column_dimensions['C'].width = 30
    #     sheet.column_dimensions['D'].width = 30
    #     sheet.column_dimensions['E'].width = 30
    #     sheet.column_dimensions['F'].width = 30
    #     sheet.column_dimensions['G'].width = 30
    #     sheet.column_dimensions['H'].width = 30
    #     sheet.column_dimensions['I'].width = 30
    #     sheet.column_dimensions['J'].width = 30
    #     sheet.column_dimensions['K'].width = 60
    #     row = (
    #         created_at, created_by, phone_number, village, city, lpu, doctor_name, category, d_type, doctor_phone,
    #         comment)
    #     sheet.append(row)
    #     book.save(f'{join_path(HOSPITAL_EXCEL_PATH, excel_path)}')


class UpdateHospitalVizitSerializer(serializers.ModelSerializer):
    products = OrderItemOrderSerializer(many=True, required=False)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "products",
            "seller",
            'inn',
            "comment",
            "total_price",
            "type_price",
            "company_name",
            "company_address",
            "phone_number",
            "bank_name",
            "is_manager_send",
            "contract_number",
            'create_contract_number',
            "status",
            'created_date'
        ]

    def update(self, instance, validated_data):
        person_data = validated_data.pop('products')
        for item in validated_data:
            if Order._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        OrderItem.objects.filter(order=instance).delete()
        for person in person_data:
            d = dict(person)
            OrderItem.objects.create(order=instance, product=d['product'], count=d.get('count'),
                                     price=d.get('price'))
        instance.save()
        return instance
