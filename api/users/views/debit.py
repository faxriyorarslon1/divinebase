from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.debit import UserDebitSerializer
from apps.users.models import Debit


class DebitModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDebitSerializer
    queryset = Debit.objects.all()
