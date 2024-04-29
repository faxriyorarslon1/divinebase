from django.db import transaction
from rest_framework import serializers
from time import timezone
from apps.users.models import Location, User, MobileLocation, District


class DistrictMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class CreatedByMobileSerializer(serializers.ModelSerializer):
    district = DistrictMobileSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'district'
        ]


class LocationDaySerializer(serializers.ModelSerializer):
    created_by = CreatedByMobileSerializer()

    class Meta:
        model = Location
        fields = [
            'created_by',
            "lan",
            "lat",
            'created_at'
        ]


class LocationModelSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Location
        fields = [
            "lan",
            "lat",
            "created_by",
            "created_at",
        ]

    def validate(self, attrs):
        user = attrs.get('created_by')
        attrs['data'] = Location.objects.filter(created_by=user)
        return attrs


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class CreatedBySerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'district'
        ]


class CreateMobileLocationSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)

    class Meta:
        model = MobileLocation
        fields = [
            "lan",
            "lat",
            "district",
            "created_by",
            "created_at",
        ]

    def create(self, validated_data: dict):
        user = validated_data.get('created_by')
        user = User.objects.get(id=user.id)
        district = user.district
        validated_data['district'] = district
        mobile_location = MobileLocation.objects.create(**validated_data)
        mobile_location.save()
        validated_data['status'] = "200"
        validated_data['language'] = {
            'uz': 'Muoffaqiyatli yaratildi',
            'ru': 'Создано успешно',
            'cyr': 'Муоффақиятли яратилди'
        }
        return validated_data


class MobileLocationModelSerializer(serializers.ModelSerializer):
    created_by = CreatedBySerializer()
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)

    class Meta:
        model = MobileLocation
        fields = [
            "lan",
            "lat",
            'district',
            "created_by",
            "created_at",
        ]

    def create(self, validated_data: dict):
        user = validated_data.get('created_by')
        user = User.objects.get(id=user.id)
        district = user.district
        validated_data['district'] = district
        mobile_location = MobileLocation.objects.create(**validated_data)
        mobile_location.save()
        validated_data['status'] = "200"
        validated_data['language'] = {
            'uz': 'Muoffaqiyatli yaratildi',
            'ru': 'Создано успешно',
            'cyr': 'Муоффақиятли яратилди'
        }
        return validated_data


class CreateLocationSerializer(serializers.ModelSerializer):
    lan = serializers.CharField(max_length=300)
    lat = serializers.CharField(max_length=300)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)

    class Meta:
        model = Location
        fields = [
            "lan",
            "lat",
            "created_by",
            'district'
        ]

    def create(self, validated_data):
        user = validated_data.get('created_by')
        user = User.objects.get(id=user.id)
        district = user.district
        validated_data['district'] = district
        mobile_location = Location.objects.create(**validated_data)
        mobile_location.save()
        return validated_data
