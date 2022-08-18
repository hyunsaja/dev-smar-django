# import sys
# import math
# from django.contrib.auth.models import User
# from .xlparse import xlparse
# from datetime import datetime, date, timedelta
# from django.utils.dateformat import DateFormat
# from rest_framework.decorators import api_view

import json
import openpyxl
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView


# ==============================================================================
# mark_machine
# ==============================================================================
from django.contrib.auth.models import User
from machine.models import Machine
from machine.models import MachineOperator
from .models import AutoMarkMachine
from .serializers import AutoMarkSerializer
json_file = './result.json'

class MarkMachine(APIView):
    def get(self, request, **kwargs):
        if self.kwargs.get('pk') is None:
            queryset = AutoMarkMachine.objects.all()  # .filter(status=5)   #ref code table
            serializer = AutoMarkSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                queryset = AutoMarkMachine.objects.get(id=self.kwargs.get('pk'))
                # queryset = AutoMarkMachine.objects.get(machine_id=self.kwargs.get('pk')).first()
                print(queryset)
                serializer = AutoMarkSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return HttpResponse(None)


# mark_machine excel upload ----------------------------------------------------

from openpyxl import load_workbook

class UploadExcelData(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file_excel']
            # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
            wb = openpyxl.load_workbook(file, read_only=True)
            sheet = wb.worksheets[0]

            author = request.user
            key_list = ['temp', 'ship_no', 'por_no', 'seq_no', 'block_no', 'pcs_no', 'paint_code', 'lot_no']
            data_list = []
            low_count = 0
            for row in sheet.rows:
                if low_count == 0:
                    low_count = low_count + 1  # 제목행 pass
                    continue
                tmp_dict = {}
                count = 0  # No 컬럼 건너뛰기
                col_count = 0
                for cell in row:
                    tmp_dict[key_list[count]] = cell.value
                    count = count + 1
                tmp_dict['author'] = str(author)
                tmp_dict['machine_id'] = '미주라벨자동마킹기'
                del tmp_dict['temp']  # No 항목 삭제

                data_list.append(tmp_dict)
                print(data_list)
            wb.close()

            serializer = AutoMarkSerializer(data=data_list, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'save_ok'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'excel_Parse_Error'})

