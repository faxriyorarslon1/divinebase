import pandas as pd
from django.http import HttpResponse
from django.http import FileResponse
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.users.models import District
from django.http import JsonResponse
from datetime import datetime


@csrf_exempt
@api_view(['POST'])
def create_excel(request):
    # Request'ten Lpu, district ve comment verilerini al
    lpu = request.data.get('lpu')
    district = request.data.get('district')
    tuman = request.data.get('tuman')
    comment = request.data.get('comment')
    current_datetime = datetime.now()
    if not (lpu and district and comment and tuman):
        return HttpResponse("Iltimos to'g'ri malumot yuboring.")

    try:
        district = District.objects.get(pk=int(district)).name
        district = district.replace(' ','_')
    except Exception as e:
        pass
    data = {'Sana':[current_datetime],'Lpu': [lpu], 'Viloyat': [district], 'Tuman': [tuman], 'Izoh': [comment]}
    df = pd.DataFrame(data)

    # Excel dosyasına yaz
    file_path = f'media/{district}_district_comment.xlsx'  # Dosya yolunu belirtin
    
    if os.path.exists(file_path):
    # Var olan Excel dosyasını oku
        existing_df = pd.read_excel(file_path)

        # Yeni verileri mevcut verilere eklemek için sütun adlarını eşleştir
        df.columns = existing_df.columns

        # Mevcut verilere yeni verileri ekleyin
        updated_df = pd.concat([existing_df, df], ignore_index=True)

        # Güncellenmiş dosyayı kaydet
        updated_df.to_excel(file_path, index=False)
    else:
        # Dosya yoksa, yeni dosya oluştur
        df.to_excel(file_path, index=False)

    response = {
        "results":"Your data is created",
        "message":{
            "status":"200",
            "language":"en"
        }
    }

    return JsonResponse(response)



@csrf_exempt
@api_view(['POST'])
def download_excel(request):
    district = request.data.get('district')
    if district:
        try:
            district = District.objects.get(pk=int(district)).name
            district = district.replace(' ','_')
        except Exception as e:
            pass
        file_path = f'media/{district}_district_comment.xlsx'   # Excel dosyasının yolunu belirtin
        if os.path.exists(file_path):
            link = f"http://divines.uz/{file_path}"
            response = {
                "results":{
                    "file_url":link
                },
                "message":{
                    "status":"400",
                    "language":"en"
                }
            }
            return JsonResponse(response)
            
        else:
            response = {
                "results":"File does not found",
                "message":{
                    "status":"400",
                    "language":"en"
                }
            }
            return JsonResponse(response)
    else:
        return HttpResponse("Iltimos to'g'ri malumot yuboring.")

