from rest_framework import serializers

from apps.order.models import ContractNumber


class ContractNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractNumber
        fields = [
            "id",
            'file_name',
            'image'
        ]
