from django.db import models

from apps.order.models import Company
from apps.users.models import User, District


class DoubleVizitExcel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    district = models.ForeignKey(District,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    file_path = models.FileField(upload_to='double_vizit')

    def __str__(self):
        return f"{self.pk}"


class HospitalVizitOrder(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hospital_vizit')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='user_district_vizit')
    status = models.CharField(max_length=256)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user_company_vizit')
    # village = models.ForeignKey(District, on_delete=models.CASCADE, related_name='user_district_vizit')
    aknel_gel = models.CharField(max_length=256, null=True, blank=True)
    astarakson_1125 = models.CharField(max_length=256, null=True, blank=True)
    astarakson_562 = models.CharField(max_length=256, null=True, blank=True)
    astaryus = models.CharField(max_length=256, null=True, blank=True)
    intrizol = models.CharField(max_length=256, null=True, blank=True)
    livomed_tab = models.CharField(max_length=256, null=True, blank=True)
    livomed_sirop = models.CharField(max_length=256, null=True, blank=True)
    renum_cap = models.CharField(max_length=256, null=True, blank=True)
    stresson_cap = models.CharField(max_length=256, null=True, blank=True)
    tavamed = models.CharField(max_length=256, null=True, blank=True)
    x_payls_maz = models.CharField(max_length=256, null=True, blank=True)
    seprazon = models.CharField(max_length=256, null=True, blank=True)
    entro_d_cap = models.CharField(max_length=256, null=True, blank=True)
    entro_d_sashe = models.CharField(max_length=256, null=True, blank=True)
    lamino_100 = models.CharField(max_length=256, null=True, blank=True)
    lamino_200 = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.created_by.first_name}) buyurtma raqami {self.pk}"


class HospitalVizitResidueExcel(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    path = models.FileField(upload_to='hospital')

    def __str__(self):
        return f"{self.name}"
