from rest_framework import serializers

from apps.users.models import City, Pharmacy


class PharmacyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            "id",
            "name",
            'address',
            "city"
        ]


class PharmacyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            "id",
            "name",
            'address'
        ]


class CreatePharmacySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Pharmacy
        fields = [
            "name",
            'address',
            "city"
        ]
