import datetime

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.income import UserIncomeSerializer
from apps.users.models import Income


class IncomeModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserIncomeSerializer
    queryset = Income.objects.all()

    def list(self, request, *args, **kwargs):
        day = self.request.query_params.get('day')
        month = self.request.query_params.get('month')
        year = datetime.datetime.now().year
        self.queryset = Income.objects.filter(Q(created_date__day=day) & Q(created_date__year=year) & Q(
            created_date__month=month))
        self.serializer_class = UserIncomeSerializer
        return super(IncomeModelViewSet, self).list(request, *args, **kwargs)
