from rest_framework import serializers

from apps.users.models import AgreeDoctor, Doctor, User


class DoctorSerializerGetAgree(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
        ]


class DoctorAgreeSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializerGetAgree()

    class Meta:
        model = AgreeDoctor
        fields = [
            "id",
            "doctor",
            "comment",
            "created_at",
            "check_agreement",
            "created_by"
        ]


class DoctorCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    comment = serializers.CharField(max_length=300)
    check_agreement = serializers.BooleanField()
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AgreeDoctor
        fields = [
            "doctor",
            "comment",
            "check_agreement",
            "created_by"
        ]
