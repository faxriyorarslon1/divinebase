from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.version_serializer import VersionSerializer
from apps.users.models import Version


class VersionModelApiViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Version.objects.all()
        query = super(VersionModelApiViewSet, self).list(request, *args, **kwargs)
        return Response(query.data.get('results')[-1])
