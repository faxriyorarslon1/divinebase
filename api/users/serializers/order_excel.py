from rest_framework.serializers import ModelSerializer

from apps.users.models import OrderExcel


class OrderExcelModelSerializer(ModelSerializer):
    class Meta:
        model = OrderExcel
        fields = [
            "id",
            "image",
            'file_name'
        ]
