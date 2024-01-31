from rest_framework import serializers

from apps.users.models import City, Doctor, District, Hospital, User


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "type_doctor",
            "category_doctor",
            "phone_number"
        ]


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name"
        ]


class CreateDoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    category_doctor = serializers.CharField(max_length=255, required=False)
    type_doctor = serializers.CharField(max_length=255, required=False)
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    phone_number = serializers.CharField(max_length=300)

    class Meta:
        model = Doctor
        fields = [
            "name",
            "type_doctor",
            "category_doctor",
            "hospital",
            "phone_number"
        ]


class CitySerializer(serializers.ModelSerializer):
    # hospital_city = HospitalSerializer(many=True)
    class Meta:
        model = City
        fields = [
            "id",
            "name"
        ]


class CreateCitySerializer(serializers.ModelSerializer):
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    name = serializers.CharField(max_length=400)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = City
        fields = [
            "name",
            "district",
            'created_by'
        ]
