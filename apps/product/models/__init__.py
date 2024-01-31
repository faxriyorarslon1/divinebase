from django.db import models

from apps.users.models import User


# class ObjectsManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    composition = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    count = models.IntegerField()
    warehouse_count = models.IntegerField(null=True, blank=True)
    original_count = models.CharField(max_length=255)
    weight = models.CharField(max_length=255, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    expired_date = models.CharField(max_length=300, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_created_by")
    image = models.CharField(max_length=500, null=True, blank=True)
    image_mobile = models.ImageField(upload_to='product', null=True, blank=True)
    price1 = models.FloatField()
    price2 = models.FloatField()
    seria = models.CharField(max_length=255)

    # objects = ObjectsManager()

    def __str__(self):
        return f"{self.name} 50%:{self.price1} 100%:{self.price2}"
