from datetime import datetime

import pytz
from rest_framework import serializers

from api.users.serializers.double_vizit_excel_serializer import create_mp_doctor_or_pharmacy_all_excel
from apps.users.models import CheckMp, User, City, Hospital, Doctor, Pharmacy, District


class DoctorCheckMpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class CityCheckMpSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityCheckMpSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityCheckMpSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class LpuCheckMpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class UserDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class MpCheckMpSerializer(serializers.ModelSerializer):
    district = UserDistrictSerializer()

    class Meta:
        model = User
        fields = '__all__'


class CreatedByCheckMpSerializer(serializers.ModelSerializer):
    district = UserDistrictSerializer()

    class Meta:
        model = User
        fields = '__all__'


class CheckMpPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckMp
        fields = "__all__"

    def validate(self, attrs):
        user = attrs.get('created_by')
        city = attrs.get('city')
        lpu = attrs.get('lpu')
        doctor = attrs.get('doctor')
        pharmacy = attrs.get('pharmacy')
        created_at = str(pytz.timezone('Asia/Tashkent').localize(datetime.now()))[:19]
        created_by = user.first_name
        if user.last_name:
            created_by = f"{user.first_name} {user.last_name}"
        village = user.district.name
        doctor_name = None
        category = None
        d_type = None
        doctor_phone = None
        if doctor:
            doctor_name = doctor.name
            category = doctor.category_doctor
            d_type = doctor.type_doctor
            doctor_phone = doctor.phone_number
        # phone_number = user.phone_number
        comment = attrs.get('comment'),
        pharmacy_name = None
        pharmacy_address = None
        mp_full_name = None
        lpu_name = None
        if lpu:
            lpu_name = lpu.name
        if pharmacy:
            pharmacy_name = pharmacy.name,
            pharmacy_address = pharmacy.address,
        mp: User = attrs.get('mp')
        if mp:
            mp_full_name = mp.first_name
            if mp.last_name:
                mp_full_name = f"{mp.first_name} {mp.last_name}"
        preparation = int(attrs.get('preparation')),
        communication = int(attrs.get('communication')),
        the_need = int(attrs.get('the_need')),
        presentation = int(attrs.get('presentation')),
        protest = int(attrs.get('protest')),
        agreement = int(attrs.get('agreement')),
        analysis = int(attrs.get('analysis')),
        if pharmacy_name:
            pharmacy_name = pharmacy_name[0]
        if pharmacy_address:
            pharmacy_address = pharmacy_address[0]
        create_mp_doctor_or_pharmacy_all_excel(
            created_at=created_at,
            created_by=created_by,
            city=city.name,
            lpu=lpu_name,
            doctor_name=doctor_name,
            doctor_phone=doctor_phone,
            d_type=d_type,
            category=category,
            village=village,
            pharmacy_name=pharmacy_name,
            pharmacy_address=pharmacy_address,
            mp=mp_full_name,
            comment=comment[0],
            communication=communication,
            preparation=preparation,
            protest=protest,
            the_need=the_need,
            presentation=presentation,
            agreement=agreement,
            analysis=analysis
        )
        if doctor:
            attrs['is_pharmacy'] = False
        else:
            attrs['is_pharmacy'] = True
        # CheckMp.objects.create(**attrs)
        return attrs


class HospitalMpPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"


class CheckMpSerializer(serializers.ModelSerializer):
    doctor = DoctorCheckMpSerializer()
    city = CityCheckMpSerializer()
    lpu = LpuCheckMpSerializer()
    pharmacy = HospitalMpPostSerializer()
    mp = MpCheckMpSerializer()
    created_by = CreatedByCheckMpSerializer()

    class Meta:
        model = CheckMp
        fields = "__all__"


class CheckMpCreateVizitSerializer(serializers.ModelSerializer):
    mp = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    lpu = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)
    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all(), required=False)
    comment = serializers.CharField(max_length=500)
    preparation = serializers.IntegerField(required=False)
    communication = serializers.IntegerField(required=False)
    the_need = serializers.IntegerField(required=False)
    presentation = serializers.IntegerField(required=False)
    protest = serializers.IntegerField(required=False)
    agreement = serializers.IntegerField(required=False)
    analysis = serializers.IntegerField(required=False)

    class Meta:
        model = CheckMp
        fields = [
            "mp",
            'city',
            'lpu',
            'doctor',
            'pharmacy',
            'comment',
            'preparation',
            'communication',
            'the_need',
            'presentation',
            'protest',
            'agreement',
            'analysis'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_pharmacy'] = False
        CheckMp.objects.create(**validated_data)
        return "Success"


class CheckMpCreatePharmacySerializer(serializers.ModelSerializer):
    mp = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all())
    comment = serializers.CharField(max_length=500)
    preparation = serializers.IntegerField()
    communication = serializers.IntegerField()
    the_need = serializers.IntegerField()
    presentation = serializers.IntegerField()
    protest = serializers.IntegerField()
    agreement = serializers.IntegerField()
    analysis = serializers.IntegerField()

    class Meta:
        model = CheckMp
        fields = [
            "mp",
            'city',
            'pharmacy',
            'comment',
            'preparation',
            'communication',
            'the_need',
            'presentation',
            'protest',
            'agreement',
            'analysis'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_pharmacy'] = True
        CheckMp.objects.create(**validated_data)
        return "Success"
