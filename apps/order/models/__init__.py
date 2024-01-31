from django.db import models
from apps.product.models import Product
from apps.users.models import User, District


class ObjectsOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(finished=False)


class ContractNumber(models.Model):
    image = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)


class Order(models.Model):
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    create_contract_number = models.DateTimeField(null=True, blank=True)
    inn = models.CharField(max_length=300)
    item = models.ManyToManyField(Product, related_name="order_products", through="OrderItem")
    seller = models.ForeignKey(User, related_name="seller", on_delete=models.CASCADE)
    comment = models.CharField(null=True, blank=True, max_length=500)
    total_price = models.FloatField(null=True, blank=True)
    type_price = models.CharField(null=True, blank=True, max_length=300)
    finished = models.BooleanField(default=False)
    company_name = models.CharField(null=True, blank=True, max_length=255)
    company_address = models.CharField(null=True, blank=True, max_length=500)
    phone_number = models.CharField(null=True, blank=True, max_length=500)
    bank_name = models.CharField(null=True, blank=True, max_length=1000)
    is_manager_send = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    district = models.ForeignKey(District, related_name='district_order', on_delete=models.CASCADE, null=True,
                                 blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)

    # objects = ObjectsOrderManager()

    def __str__(self):
        return f"Total: {self.total_price} inn: {self.inn}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    count = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product.name} of {self.count}"


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_company', null=True, blank=True)
    company_address = models.CharField(null=True, blank=True, max_length=500)
    phone_number = models.CharField(null=True, blank=True, max_length=500)
    bank_name = models.CharField(null=True, blank=True, max_length=1000)
    inn = models.CharField(null=True, blank=True, max_length=255)
    company_director_name = models.CharField(null=True, blank=True, max_length=255)
    company_director_phone_number = models.CharField(null=True, blank=True, max_length=255)
    company_provider_name = models.CharField(null=True, blank=True, max_length=255)
    company_provider_phone_number = models.CharField(null=True, blank=True, max_length=255)


class ProductResidue(models.Model):
    name = models.CharField(max_length=255)


class CompanyProduct(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ManyToManyField(ProductResidue, related_name="order_products", through="ProductResidueItem")


class ProductResidueItem(models.Model):
    product_residue = models.ForeignKey(ProductResidue, on_delete=models.CASCADE)
    company_product = models.ForeignKey(CompanyProduct, on_delete=models.CASCADE, related_name="products")
    count = models.IntegerField(default=1)
