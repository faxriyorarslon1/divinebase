from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.double_vizit.models import DoubleVizitExcel, HospitalVizitOrder, HospitalVizitResidueExcel
from apps.users.models import CheckMp


# mp = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mp_user')
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my')
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='my_city')
#     lpu = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_mp', null=True, blank=True)
#     pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='pharmacy_mp', null=True, blank=True)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_mp', null=True, blank=True)
#     comment = models.CharField(max_length=255)
#     preparation = models.IntegerField()
#     communication = models.IntegerField()
#     the_need = models.IntegerField()
#     presentation = models.IntegerField()
#     protest = models.IntegerField()
#     agreement = models.IntegerField()
#     analysis = models.IntegerField()
#     is_pharmacy = models.BooleanField(default=True)
@admin.register(CheckMp)
class CompanyModelAdmin(ModelAdmin):
    list_display = ['id', 'mp', 'created_by', 'is_pharmacy', 'city']


@admin.register(DoubleVizitExcel)
class DoubleVizitExcelModelAdmin(ModelAdmin):
    list_display = ['id', 'district', 'file_path', 'created_at']


@admin.register(HospitalVizitOrder)
class HospitalVizitOrderModelAdmin(ModelAdmin):
    list_display = ['id', 'created_at', 'created_by', 'company']


@admin.register(HospitalVizitResidueExcel)
class HospitalVizitOrderExcelModelAdmin(ModelAdmin):
    list_display = ['id', 'name', 'path']
