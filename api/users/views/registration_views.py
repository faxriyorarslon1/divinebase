import random
from datetime import datetime
from os.path import join

import requests
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token

from DivineBase.settings import MEDIA_ROOT
from api.users.serializers.authorization import RegistrationSerializer, LoginUserSerializer, \
    DistrictAuthorizationSerializer, \
    UserSerializer, UserExistSerializer, UserLoginExistSerializer, DistrictGetOneForCity, UpdateInActiveSerializer, \
    UserChatIdSerializer, UserDistrictUpdate, UserDataAndPhoneNumberSerializer, MobileLoginUserSerializer, \
    LoginTokenUserSerializer, UserDistrictVizitSerializer, VillageSerializer
from apps.users.models import User, District


class UserModelViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def get_all_not_active(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(is_member=False).all()
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all_user_for_location(self, request, *args, **kwargs):
        district = self.request.query_params.get('district')
        self.queryset = User.objects.filter(Q(district=district) & (Q(role='manager') | Q(role='agent')))
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all_agent(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(role='admin')
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all_agent_vizit(self, request, *args, **kwargs):
        district = self.request.query_params.get('district')
        self.queryset = User.objects.filter(district=district, role='agent')
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all_office_manager(self, request, *args, **kwargs):
        # district = self.request.query_params('district')
        self.queryset = User.objects.filter(role='office_manager')
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def put_user_data_and_phone_number(self, request, *args, **kwargs):
        self.serializer_class = UserDataAndPhoneNumberSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def district_update(self, request, *args, **kwargs):
        self.serializer_class = UserDistrictUpdate
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def mp_agent_order(self, request):
        role = self.request.query_params.get('role')
        district = self.request.query_params.get('district')
        user = User.objects.filter(role=role, district=district)
        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def admin_district_manager_user(self, request, *args, **kwargs):
        district = self.request.query_params.get('district')
        user = User.objects.filter(role='manager', district=district)
        page = self.paginate_queryset(user)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False)
    def mp_agent_all(self, request, *args, **kwargs):
        first_name = self.request.query_params.get('first_name')
        district = self.request.query_params.get('district')
        last_name = self.request.query_params.get('last_name')
        user = User.objects.filter(role="agent", district=district)
        if first_name:
            user = user.filter(first_name__startswith=first_name)
        if last_name:
            user = user.filter(last_name__startswith=last_name)
        if first_name and last_name:
            user = user.filter(first_name__startswith=first_name, last_name__startswith=last_name)
        page = self.paginate_queryset(user)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_role_user(self, request):
        role = self.request.query_params.get('role')
        self.queryset = User.objects.filter(role=role, is_member=True)
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def user_chat_id(self, request):
        serializer = UserChatIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get('message')
        role = serializer.validated_data.get('role')
        user_id = serializer.validated_data.get('id')
        token = serializer.validated_data.get('token')
        if user_id:
            return Response({
                "message": message,
                'id': user_id,
                'role': role,
                'token': token.key,
                'district': serializer.validated_data.get('district').id,
                'first_name': serializer.validated_data.get('first_name'),
                'last_name': serializer.validated_data.get('last_name'),
                'phone_number': serializer.validated_data.get('phone_number')
            })
        return Response(
            {
                "message": message
            }
        )

    @action(methods=['get'], detail=False)
    def user_district_vizit(self, request, *args, **kwargs):
        district = self.request.query_params.get("district")
        queryset = User.objects.filter(district=district).all()
        serializer = UserDistrictVizitSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=False)
    def user_exist(self, request):
        serializer = UserExistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get('message')
        user = serializer.validated_data.get("user")
        if user:
            return Response(
                {
                    "message": message,
                    "user_id": user.pk,
                    "is_member": user.is_member
                }
            )
        return Response(
            {
                "message": message
            }
        )

    def get_queryset(self):
        district = self.request.query_params.get('district')
        if district:
            self.queryset = User.objects.filter(district=district, role="agent")
            return self.queryset
        self.queryset = User.objects.all()
        return self.queryset

    @action(methods=['post'], detail=False)
    def login_exist_user(self, request):
        serializer = UserLoginExistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']
        return Response(
            {
                "message": message
            }

        )


class RegistrationModelViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateInActiveSerializer
        return super(RegistrationModelViewSet, self).update(request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        role = user.role
        return Response({
            'user_id': user.pk,
            'token': token.key,
            'role': role if role else None
        })

    @action(methods=['post'], detail=False)
    def mobile_login(self, request):
        phone_number = request.data.get('phone_number')
        new_phone_number = phone_number if phone_number[0] == '+' else f'+{phone_number[1:]}'
        user = User.objects.filter(phone_number=str(new_phone_number)).first()
        if not user:
            raise ValidationError(
                {
                    "message": "Bunaqa inson topilmadi telegramdan registratsiyadan o'ting",
                    "url": 'https://telegram.me/future_world_group_bot/'
                }
            )
        # LOCAL = "http://127.0.0.1:8000/"
        # BASE = "https://dzokirov20.pythonanywhere.com/"
        token, _ = Token.objects.get_or_create(user=user)
        text = f"Marxamat sizga havola berildi berilgan havola orqali mobil ilovamizga o'tishingiz mumkin \n<a href='https://divines.uz/version1/index?token={token}'><b>Mobile Appga O'tish</b></a>"
        url = f'https://api.telegram.org/bot5562028031:AAHhwjOM66h1ZKZxfq3naS77PZwq7_3a7BM/sendMessage?chat_id={user.chat_id}&parse_mode=HTML&text={text}'
        try:

            requests.post(url)
            return Response(
                {
                    "message": "Muvaffaqiyatli yakunlandi",
                    "url": 'https://telegram.me/future_world_group_bot/'
                }
            )
        except Exception:
            return Response(
                {
                    "message": "Sizda telegramda muommo bor"
                }
            )

        # https: // api.telegram.org / botXXtokenxx / sendMessage?chat_id = chat_id & text = text

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": {
                "uz": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
                "уз": "Муваффақиятли рўйхатдан ўтдингиз",
                "ru": "Вы успешно зарегистрированы",
            }})

    # https: // api.telegram.org / botXXtokenxx / sendMessage?chat_id = chat_id & text = text
    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": {
                "uz": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
                "уз": "Муваффақиятли рўйхатдан ўтдингиз",
                "ru": "Вы успешно зарегистрированы",
            }})

    @action(methods=['get'], detail=False)
    def village_agent_manager(self, request):
        role = self.request.query_params.get('role')
        village = self.request.query_params.get('village')
        queryset = User.objects.filter(role=role, district=village)
        serializer = VillageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def send_token(self, request):
        serializer = LoginTokenUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        district = user.district
        role = user.role
        return Response({
            'user_id': user.pk,
            'district': district.id,
            'role': role if role else None
        })


class VillageModelApiViewSet(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = District.objects.all()
    serializer_class = DistrictAuthorizationSerializer

    @action(methods=['get'], detail=True)
    def city(self, request, *args, **kwargs):
        self.serializer_class = DistrictGetOneForCity
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    #
    # @action(methods=['get'], detail=False)
    # def district_user(self, request, *args, **kwargs):
    #     self.serializer_class = UserDistrictSerializer
