from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.order.serializer.contract_number import ContractNumberSerializer
from api.users.serializers.debit import UserDebitSerializer
from apps.order.models import ContractNumber


class ContractNumberModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractNumberSerializer
    queryset = ContractNumber.objects.all()
