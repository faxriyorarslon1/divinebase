from rest_framework import serializers

from apps.users.models import Debit


class UserDebitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debit
        fields = [
            "id",
            'file_name',
            'image'
        ]
