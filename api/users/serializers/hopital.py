from rest_framework import serializers

from apps.users.models import Hospital, City


class HospitalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name",
            "city"
        ]


class HospitalRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name"
        ]


class CreateHospitalSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Hospital
        fields = [
            "name",
            "city"
        ]
