from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import User, District, Location, City, Doctor, AgreeDoctor, Hospital, OrderExcel, Debit, Income, \
    Pharmacy, MobileLocation, Version,Appmobile


admin.site.register(Appmobile)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'phone_number', "first_name", "last_name", 'chat_id', 'is_active', 'role', "is_member")
    list_filter = ('phone_number',)
    fieldsets = (
        (None, {'fields': (
            'phone_number', 'first_name', 'last_name', 'role', 'district', 'chat_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', "is_member")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'first_name', 'last_name', 'role', 'chat_id',
                'district', "is_member"
            )
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)


admin.site.register(User, CustomUserAdmin)


@admin.register(District)
class ModelAdminVillage(ModelAdmin):
    list_display = ["id", 'name']


@admin.register(Location)
class LocationModelAdmin(ModelAdmin):
    list_display = ['id', "lan", "lat", "created_by", "created_at"]


@admin.register(MobileLocation)
class MobileLocationModelAdmin(ModelAdmin):
    list_display = ['id', "lan", "lat", "created_by", "created_at", 'district']


@admin.register(Version)
class AdminVersion(ModelAdmin):
    list_display = ['id', 'version_text', 'version_boolean']


@admin.register(City)
class CityModelAdmin(ModelAdmin):
    list_display = ["id", 'name', 'district', 'created_by']


@admin.register(Doctor)
class DoctorModelAdmin(ModelAdmin):
    list_display = ["id", "name", "type_doctor", "category_doctor", "hospital"]


@admin.register(Hospital)
class DoctorModelAdmin(ModelAdmin):
    list_display = ["id", "name", "city"]


@admin.register(Pharmacy)
class DoctorModelAdmin(ModelAdmin):
    list_display = ["id", "name", 'address', "city"]


@admin.register(AgreeDoctor)
class AgreeDoctorModelAdmin(ModelAdmin):
    list_display = ['id', "comment", "doctor", "created_at", "check_agreement"]


@admin.register(OrderExcel)
class OrderExcelModelAdmin(ModelAdmin):
    list_display = ['id', 'image', 'file_name']


@admin.register(Debit)
class DebitModelAdmin(ModelAdmin):
    list_display = ['id', 'image', 'file_name']


@admin.register(Income)
class IncomeModelAdmin(ModelAdmin):
    list_display = ['id', 'image', 'file_name']
