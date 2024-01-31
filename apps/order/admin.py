from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.order.models import Order, OrderItem, Company, ContractNumber
from apps.product.models import Product


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'inn', 'comment', "total_price", "type_price", 'created_date']


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['id', "product", 'count', 'price']


@admin.register(ContractNumber)
class ContractNumberAdmin(ModelAdmin):
    list_display = ['id', 'image', 'file_name']


@admin.register(Company)
class CompanyModelAdmin(ModelAdmin):
    list_display = ['id', 'company_name', 'company_address', 'phone_number', 'bank_name', 'inn',
                    'company_director_name',
                    'company_director_phone_number',
                    'company_provider_phone_number',
                    'company_provider_name'
                    ]
