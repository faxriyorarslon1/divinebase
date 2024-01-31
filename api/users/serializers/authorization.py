from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from apps.users.models import User, District, City
from apps.vizit.models import Vizit


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"


class UserDataAndPhoneNumberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number'
        ]

    def validate(self, attrs):
        self.instance.first_name = attrs.get('first_name')
        self.instance.last_name = attrs.get('last_name')
        self.instance.phone_number = attrs.get('phone_number')
        self.instance.save()
        return self.instance


class UserDistrictUpdate(serializers.ModelSerializer):
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'district'
        ]

    def validate(self, attrs):
        self.instance.district = attrs.get('district')
        self.instance.save()
        return self.instance

    def update(self, instance: User, validated_data):
        instance.district = validated_data.get('district')
        instance.save()
        return instance


class UserChatIdSerializer(serializers.Serializer):
    chat_id = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = [
            'chat_id',
            'id',
            'role',
            'token',
            'district',
            'first_name',
            'last_name',
            'phone_number'
        ]

    def validate(self, attrs):
        user = User.objects.filter(chat_id=attrs.get("chat_id")).first()
        if not user:
            attrs['message'] = "no"
        else:
            token, _ = Token.objects.get_or_create(user=user)
            attrs['message'] = "yes"
            attrs['role'] = user.role
            attrs['id'] = user.id
            attrs['token'] = token
            attrs['district'] = user.district
            attrs['first_name'] = user.first_name
            attrs['last_name'] = user.last_name
            attrs['phone_number'] = user.phone_number
        return attrs


class UserExistSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number"
        ]

    def validate(self, attrs):
        user1 = User.objects.filter(phone_number=attrs.get("phone_number")).exclude(first_name__isnull=True,
                                                                                    last_name__isnull=True).exists()
        user = User.objects.filter(phone_number=attrs.get("phone_number")).exists()
        if not user:
            attrs['message'] = "Uzr lekin bunday inson topilmadi"
            return attrs
        elif user and user1:
            user = User.objects.filter(phone_number=attrs.get("phone_number"), is_member=True).exists()
            if not user:
                attrs['message'] = "not member"
            else:
                attrs['message'] = "bor"
            return attrs
        elif user and not user1:
            user1 = User.objects.filter(phone_number=attrs.get("phone_number")).first()
            attrs['user'] = user1
            attrs['message'] = "yuq"
            return attrs


class UserVizitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vizit
        fields = "__all__"


class UserDistrictVizitSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: User):
        data = super(UserDistrictVizitSerializer, self).to_representation(instance)
        data['user_vizit'] = UserVizitSerializer(instance.user_vizit, many=True).data
        data['count'] = len(data['user_vizit'])
        return data

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'district',
            # 'user_vizit'
        ]


class UserLoginExistSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number"
        ]

    def validate(self, attrs):
        user = User.objects.filter(phone_number=attrs.get("phone_number")).exists()
        if not user:
            attrs['message'] = "Bunday inson yo'q"
        else:
            attrs['message'] = "Topildi"
        return attrs


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
        ]

    def validate(self, attrs):
        if attrs.get('phone_number'):
            request = self.context['request']
            user = User.objects.get(phone_number=attrs.get('phone_number'))
            if not user:
                raise serializers.ValidationError("Bunaqa inson topilmadi")
            token, _ = Token.objects.get_or_create(user=user)
            attrs['user'] = user
            attrs['token'] = token
            return attrs


class MobileLoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)
    code = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = [
            "phone_number",
        ]

    def validate(self, attrs):
        if attrs.get('phone_number'):
            request = self.context['request']
            user = User.objects.get(phone_number=attrs.get('phone_number'))
            if not user:
                raise serializers.ValidationError("Bunaqa inson topilmadi")
            token, _ = Token.objects.get_or_create(user=user)
            attrs['user'] = user
            attrs['token'] = token
            return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "chat_id"

        ]
        extra_kwargs = {"id": {"read_only": True}}

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                "Bunaqa telefon nomerli inson bizda bor iltimos boshqa nomerdan foydalaning yoki login qismiga o'ting"
            )
        if 10 >= len(phone_number) >= 12:
            raise ValidationError("Iltimos telefon nomerni to'g'ri kiriting")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                {
                    "Bunaqa inson bizning ro'yxatda bor"
                })
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        chat_id = validated_data.get('chat_id')
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        phone_number = validated_data.get('phone_number')
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            chat_id=chat_id
        )
        user.save()
        return user


class LoginTokenUserSerializer(ModelSerializer):
    token = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "token",
        ]

    def validate(self, attrs):
        user = User.objects.get(auth_token=attrs.get('token'))
        if not user:
            raise serializers.ValidationError("Bunaqa inson topilmadi")
        attrs['user'] = user
        return attrs


class DistrictAuthorizationSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = [
            "id",
            "name"
        ]


class CityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            "name"
        ]


class DistrictGetOneForCity(serializers.ModelSerializer):
    city = CityModelSerializer(many=True)

    class Meta:
        model = District
        fields = [
            "id",
            "name",
            "city"
        ]


# class UserDistrictSerializer(serializers.ModelSerializer):
#     user = UserAllSerializer(many=True)
#
#     class Meta:
#         model = District
#         fields = [
#             'user'
#         ]


class UpdateInActiveSerializer(serializers.ModelSerializer):
    is_member = serializers.BooleanField()
    role = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            "is_member",
            'role'
        ]
