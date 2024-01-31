import io
from os.path import join
import pandas as pd

import xlwt
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.order_excel import OrderExcelModelSerializer
from apps.users.models import OrderExcel
from utils import EXCEL_PATH


class OrderExcelModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderExcelModelSerializer
    queryset = OrderExcel.objects.all()


STUDENT_DATA_FILE_HEADERS = ["Viloyat", "Shaxar", "LPU", "Doktor ismi", "Mutaxasisligi", "Kategoriyasi",
                             'Doktor telefoni', 'Izoh']

#
# def download_excel_data(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet("sheet1")
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4', ]
#
#     # write column headers in sheet
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     # Sheet body, remaining r
#     font_style = xlwt.XFStyle()
#     data = get_data()  # dummy method to fetch data.
#     for my_row in data:
#         row_num = row_num + 1
#         ws.write(row_num, 0, my_row.name, font_style)
#         ws.write(row_num, 1, my_row.start_date_time, font_style)
#         ws.write(row_num, 2, my_row.end_date_time, font_style)
#         ws.write(row_num, 3, my_row.notes, font_style)
#     wb.save(response)
#     return response


# def download_excel(request):
#     with io.BytesIO() as b:
#         # data = pd.get_analytics_data()
#         path = join(EXCEL_PATH, 'obshi_vizit_excel_Samarqand.xlsx')
#         with pd.ExcelWriter(path) as writer:
#             data.to_excel(writer, sheet_name="Data", index=False)
#         filename = f"analytics_data.xlsx"
#         res = HttpResponse(
#             b.getvalue(),
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
#         res['Content-Disposition'] = f'attachment; filename={filename}'
#         return res
#

class DownloadView(APIView):
    def get(self, request, format=None):
        path = join(EXCEL_PATH, 'obshi_vizit_excel_Samarqand.xlsx')
        # excel = open(path, "rb")
        with open(path, "rb") as excel:
            data = excel.read()
        response = HttpResponse(data,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'Samarqand'
        return response

#
# class DownloadView(APIView):
#     # renderer_classes = [ExcelStudentDataRenderer]
#
#     def get(self, request, format=None):
#         path = join(EXCEL_PATH, 'obshi_vizit_excel_Samarqand.xlsx')
#         return Response(
#             headers={"Content-Disposition": f'attachment; filename="{path}"'})
