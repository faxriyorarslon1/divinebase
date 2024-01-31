from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.vizit.models import Vizit, VizitExcel


@admin.register(Vizit)
class ModelAdminVizit(ModelAdmin):
    list_display = ["id", 'user', 'lpu', 'doctor', 'city', 'comment']


@admin.register(VizitExcel)
class ModelAdminVizitExcel(ModelAdmin):
    list_display = ["id", 'path', 'district']
