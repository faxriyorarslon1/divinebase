import datetime

import openpyxl
from rest_framework import serializers
from apps.double_vizit.models import HospitalVizitOrder, HospitalVizitResidueExcel
from os.path import join as join_path

from apps.order.models import Company
from apps.users.models import User, District
from utils import HOSPITAL_EXCEL_PATH


def create_hospital_all_excel(created_at: object, created_by: object, director_phone_number: object = "",
                              village: object = "",
                              hospital_name: object = "", inn: object = "", bron_created_at: object = '',
                              director_name: object = '', pharmacist_name: object = '',
                              pharmacist_phone_number: object = '', summa: object = 0, aknel_gel: object = 0,
                              actaracson_tz_1125: object = 0, actaracson_tz_562: object = 0, astariyus=0, intrizol=0,
                              livomed_tab=0, livomed_sirop=0, renum_caps=0, stresson=0, tavamed=0, x_plays=0,
                              seprazon=0,
                              entro_d_caps=0, entro_d_sashe=0, lamino_100=0, lamino_200=0) -> object:
    excel_path = "Qoldiq.xlsx"
    book = openpyxl.load_workbook(f'{join_path(HOSPITAL_EXCEL_PATH, excel_path)}')
    sheet = book.active
    row = (
        created_at, created_by, village, inn, hospital_name, bron_created_at, aknel_gel,
        actaracson_tz_1125, actaracson_tz_562, astariyus, intrizol,
        livomed_tab, livomed_sirop, renum_caps, stresson, tavamed, x_plays, seprazon,
        entro_d_caps, entro_d_sashe, lamino_100, lamino_200,
        summa, director_name, director_phone_number, pharmacist_name,
        pharmacist_phone_number
    )
    sheet.append(row)
    book.save(f'{join_path(HOSPITAL_EXCEL_PATH, excel_path)}')
    return "Juda ajoyib"


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number'
        ]


class DistrictHospitalVizitSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id',
            'name'
        ]


class CompanyHospitalVizitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'company_name',
            'company_director_name',
            'company_director_phone_number',
            'company_provider_name',
            'company_provider_phone_number',
            'bank_name',
            'inn'
        ]


class HospitalVizitOrderOneSerializer(serializers.ModelSerializer):
    created_by = CreatedBySerializer()
    district = DistrictHospitalVizitSerializer()
    company = CompanyHospitalVizitSerializer()

    class Meta:
        model = HospitalVizitOrder
        fields = [
            'id',
            'created_at',
            'created_by',
            'district',
            'company',
            'status',
            'aknel_gel',
            'astarakson_1125',
            'astarakson_562',
            'astaryus',
            'intrizol',
            'livomed_tab',
            'livomed_sirop',
            'renum_cap',
            'stresson_cap',
            'tavamed',
            'x_payls_maz',
            'seprazon',
            'entro_d_cap',
            'entro_d_sashe',
            'lamino_100',
            'lamino_200'

        ]


# class UpdateVizitOrder

class HospitalVizitOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalVizitOrder
        fields = '__all__'

    def update(self, instance: HospitalVizitOrder, validated_data: dict):
        instance.created_at = str(datetime.datetime.now())
        instance.company = validated_data.get('company', instance.company)
        instance.aknel_gel = validated_data.get('aknel_gel', instance.aknel_gel)
        instance.astarakson_1125 = validated_data.get('astarakson_1125', instance.astarakson_1125)
        instance.astarakson_562 = validated_data.get('astarakson_562', instance.astarakson_562)
        instance.astaryus = validated_data.get('astaryus', instance.astaryus)
        instance.intrizol = validated_data.get('intrizol', instance.intrizol)
        instance.livomed_tab = validated_data.get('livomed_tab', instance.livomed_tab)
        instance.livomed_sirop = validated_data.get('livomed_sirop', instance.livomed_sirop)
        instance.renum_cap = validated_data.get('renum_cap', instance.renum_cap)
        instance.stresson_cap = validated_data.get('stresson_cap', instance.stresson_cap)
        instance.tavamed = validated_data.get('tavamed', instance.tavamed)
        instance.x_payls_maz = validated_data.get('x_payls_maz', instance.x_payls_maz)
        instance.seprazon = validated_data.get('seprazon', instance.seprazon)
        instance.district = validated_data.get('district', instance.district)
        instance.entro_d_cap = validated_data.get('entro_d_cap', instance.entro_d_cap)
        instance.entro_d_sashe = validated_data.get('entro_d_sashe', instance.entro_d_sashe)
        instance.lamino_100 = validated_data.get('lamino_100', instance.lamino_100)
        instance.lamino_200 = validated_data.get('lamino_200', instance.lamino_200)
        instance.save()
        created_at = str(datetime.datetime.now())
        first_last = validated_data.get('created_by')
        created_by = validated_data.get('created_by').first_name
        hospital_name = validated_data.get('company').company_name
        if validated_data.get('created_by').last_name:
            created_by = f'{first_last.first_name} {first_last.last_name}'
        director_phone_number = None
        director_name = None
        pharmacist_name = None
        pharmacist_phone_number = None
        if validated_data.get('company').company_director_name:
            director_name = validated_data.get('company').company_director_name
        if validated_data.get('company').company_director_phone_number:
            director_phone_number = validated_data.get('company').company_director_phone_number
        if validated_data.get('company').company_provider_name:
            pharmacist_name = validated_data.get('company').company_provider_name
        if validated_data.get('company').company_provider_phone_number:
            pharmacist_phone_number = validated_data.get('company').company_provider_phone_number
        village = instance.district
        inn = validated_data.get('company').inn
        aknel_gel = validated_data.get('aknel_gel')
        actaracson_tz_1125 = validated_data.get('astarakson_1125')
        actaracson_tz_562 = validated_data.get('astarakson_562')
        astariyus = validated_data.get('astaryus')
        intrizol = validated_data.get('intrizol')
        livomed_tab = validated_data.get('livomed_tab')
        livomed_sirop = validated_data.get('livomed_sirop')
        renum_caps = validated_data.get('renum_cap')
        stresson = validated_data.get('stresson_cap')
        tavamed = validated_data.get('tavamed')
        x_plays = validated_data.get('x_payls_maz')
        seprazon = validated_data.get('seprazon')
        entro_d_caps = validated_data.get('entro_d_cap')
        entro_d_sashe = validated_data.get('entro_d_sashe')
        lamino_100 = validated_data.get('lamino_100')
        lamino_200 = validated_data.get('lamino_200')
        create_hospital_all_excel(created_at=created_at,
                                  created_by=created_by,
                                  director_phone_number=director_phone_number,
                                  village=village.name, hospital_name=hospital_name, inn=inn,
                                  director_name=director_name,
                                  pharmacist_name=pharmacist_name, pharmacist_phone_number=pharmacist_phone_number,
                                  aknel_gel=aknel_gel, actaracson_tz_1125=actaracson_tz_1125,
                                  actaracson_tz_562=actaracson_tz_562, astariyus=astariyus, intrizol=intrizol,
                                  livomed_tab=livomed_tab, livomed_sirop=livomed_sirop, renum_caps=renum_caps,
                                  stresson=stresson, tavamed=tavamed, x_plays=x_plays, seprazon=seprazon,
                                  entro_d_caps=entro_d_caps, entro_d_sashe=entro_d_sashe, lamino_100=lamino_100,
                                  lamino_200=lamino_200)
        return instance

    def create(self, validated_data):
        created_at = str(datetime.datetime.now())
        first_last = validated_data.get('created_by')
        created_by = validated_data.get('created_by').first_name
        hospital_name = validated_data.get('company').company_name
        if validated_data.get('created_by').last_name:
            created_by = f'{first_last.first_name} {first_last.last_name}'
        director_phone_number = None
        director_name = None
        pharmacist_name = None
        pharmacist_phone_number = None
        if validated_data.get('company').company_director_name:
            director_name = validated_data.get('company').company_director_name
        if validated_data.get('company').company_director_phone_number:
            director_phone_number = validated_data.get('company').company_director_phone_number
        if validated_data.get('company').company_provider_name:
            pharmacist_name = validated_data.get('company').company_provider_name
        if validated_data.get('company').company_provider_phone_number:
            pharmacist_phone_number = validated_data.get('company').company_provider_phone_number
        inn = validated_data.get('company').inn
        anken_gel = validated_data.get('aknel_gel')
        actaracson_tz_1125 = validated_data.get('astarakson_1125')
        actaracson_tz_562 = validated_data.get('astarakson_562')
        astariyus = validated_data.get('astariyus')
        intrizol = validated_data.get('intrizol')
        livomed_tab = validated_data.get('livomed_tab')
        livomed_sirop = validated_data.get('livomed_sirop')
        renum_caps = validated_data.get('renum_cap')
        stresson = validated_data.get('stresson')
        tavamed = validated_data.get('tavamed')
        x_plays = validated_data.get('x_plays')
        seprazon = validated_data.get('seprazon')
        entro_d_caps = validated_data.get('entro_d_caps')
        entro_d_sashe = validated_data.get('entro_d_sashe')
        lamino_100 = validated_data.get('lamino_100')
        village = validated_data.get('district')
        lamino_200 = validated_data.get('lamino_200')
        HospitalVizitOrder.objects.create(**validated_data)
        create_hospital_all_excel(created_at=created_at,
                                  created_by=created_by,
                                  director_phone_number=director_phone_number,
                                  village=village.name, hospital_name=hospital_name, inn=inn,
                                  director_name=director_name,
                                  pharmacist_name=pharmacist_name, pharmacist_phone_number=pharmacist_phone_number,
                                  aknel_gel=anken_gel, actaracson_tz_1125=actaracson_tz_1125,
                                  actaracson_tz_562=actaracson_tz_562, astariyus=astariyus, intrizol=intrizol,
                                  livomed_tab=livomed_tab, livomed_sirop=livomed_sirop, renum_caps=renum_caps,
                                  stresson=stresson, tavamed=tavamed, x_plays=x_plays, seprazon=seprazon,
                                  entro_d_caps=entro_d_caps, entro_d_sashe=entro_d_sashe, lamino_100=lamino_100,
                                  lamino_200=lamino_200)
        return validated_data


class HospitalVizitOrderExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalVizitResidueExcel
        fields = '__all__'
