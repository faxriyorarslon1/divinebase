from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


# from apps.hospital.models import Hospital


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, **extra_fields):
        now = timezone.now()
        if not phone_number:
            raise ValueError("Iltimos telefon nomerni kiriting")
        user = self.model(phone_number=phone_number, is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.save(using=self._db)
        return user

    def _create_superuser(self, phone_number, password, **extra_fields):
        now = timezone.now()
        if not phone_number:
            raise ValueError("Iltimos telefon nomerni kiriting")
        user = self.model(phone_number=phone_number, password=password, is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, **extra_fields):
        return self._create_user(phone_number
                                 ** extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        user = self._create_superuser(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class District(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=400)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_by_city', null=True,
                                   blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="city")

    def __str__(self):
        return f"{self.name}{self.district.name}"


class Doctor(models.Model):
    name = models.CharField(max_length=400)
    phone_number = models.CharField(max_length=400)
    type_doctor = models.CharField(max_length=400)
    category_doctor = models.CharField(max_length=400)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name="hospital", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class Version(models.Model):
    version_text = models.CharField(max_length=255)
    version_boolean = models.BooleanField(default=False)

    def __str__(self):
        return self.version_text


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="hospital_city")

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pharmacy_city')


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(null=True, blank=True, max_length=300)
    id = models.AutoField(primary_key=True, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=400, null=True, blank=True)
    last_name = models.CharField(max_length=400, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="district_user")
    passport_image = models.FileField(upload_to='user/passport', null=True, blank=True)
    passport_image_path = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=400, null=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    is_member = models.BooleanField(default=False)
    chat_id = models.CharField(max_length=300, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    lan = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_location')
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='district_location')

    def __str__(self):
        return f"{self.created_by.first_name}-{self.created_at}"


class MobileLocation(models.Model):
    lan = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_mobile_location')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district_mobile_location')

    def __str__(self):
        return f"{self.lan} {self.lat}"


class AgreeDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="agree_doctor")
    comment = models.CharField(max_length=500)
    check_agreement = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", null=True, blank=True)

    def __str__(self):
        return f"{self.doctor} {self.check_agreement}"


class CheckMp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    mp = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mp_user', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='mp_district', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='my_city')
    lpu = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_mp', null=True, blank=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='pharmacy_mp', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_mp', null=True, blank=True)
    comment = models.CharField(max_length=255)
    preparation = models.IntegerField()
    communication = models.IntegerField()
    the_need = models.IntegerField()
    presentation = models.IntegerField()
    protest = models.IntegerField()
    agreement = models.IntegerField()
    analysis = models.IntegerField()
    is_pharmacy = models.BooleanField(default=True)


class OrderExcel(models.Model):
    image = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True, blank=True)


class Debit(models.Model):
    image = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True, blank=True)


class Income(models.Model):
    image = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
