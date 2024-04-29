from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.version_serializer import VersionSerializer
from apps.users.models import Version
from apps.users.models import Appmobile
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers
from rest_framework import status

class MobileAppModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appmobile
        fields = '__all__'
class MobileAPIView(RetrieveAPIView):
    serializer_class = MobileAppModelSerializer

    def get_object(self):
        try:
            latest_object = Appmobile.objects.all().last()
            return latest_object
        except Appmobile.DoesNotExist:
            return Response({"detail": "No objects found."}, status=status.HTTP_404_NOT_FOUND)


class VersionModelApiViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Version.objects.all()
        query = super(VersionModelApiViewSet, self).list(request, *args, **kwargs)
        return Response(query.data.get('results')[-1])
