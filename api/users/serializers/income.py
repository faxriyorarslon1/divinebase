from rest_framework import serializers

from apps.users.models import Income


class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            'file_name',
            'image',
            'created_date'
        ]
