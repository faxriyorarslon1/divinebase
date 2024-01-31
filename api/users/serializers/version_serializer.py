from rest_framework.serializers import ModelSerializer

from apps.users.models import Version


class VersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        fields = [
            'version_text',
            'version_boolean'
        ]
