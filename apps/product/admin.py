from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.product.models import Product


@admin.register(Product)
class ProductAdin(ModelAdmin):
    list_display = ['id', "name", 'count', 'size', "price1", "price2", 'warehouse_count', "active"]
