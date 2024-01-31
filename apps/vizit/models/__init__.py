import datetime

from django.db import models
from django.db.models import Model

from apps.users.models import User, City, Hospital, Doctor, District


class Vizit(Model):
    created_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='user_vizit')
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='district_vizit_all')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='city_vizit')
    lpu = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='hospital_vizit')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='doctor_vizit')
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.pk}) {self.user} - {self.comment}'


# print(datetime.datetime.now())
class VizitExcel(Model):
    created_at = models.DateTimeField(auto_now=True)
    path = models.FileField(upload_to='excel_utils', null=True, blank=True)
    district = models.ForeignKey(District,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)

    def __str__(self):
        return f"{self.pk}"
