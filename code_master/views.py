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
from django.db.models import Q


# ==============================================================================
# mark_machine
# ==============================================================================
from django.contrib.auth.models import User
from machine.models import Machine
from machine.models import MachineOperator
from .models import AutoMarkMachine
from .serializers import AutoMarkSerializer
json_file = './result.json'

# ==============================================================================
# mark_machine excel upload ----------------------------------------------------
# ==============================================================================

from openpyxl import load_workbook

class UploadExcelData(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file_excel']
            machine_id = request.data['extra_machineID']
            print(machine_id)
            # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
            wb = openpyxl.load_workbook(file, read_only=True)
            sheet = wb.worksheets[0]

            author = request.user.id
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
                #-------------------------------------
                for cell in row:
                    tmp_dict[key_list[count]] = cell.value
                    count = count + 1
                # -------------------------------------
                tmp_dict['author'] = author
                tmp_dict['machine_id'] = machine_id
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
            return Response({'message': 'Error'})


# ==============================================================================
# 마킹 머신 공통 -----------------------------------------------------------------
# ==============================================================================
# 미주 마킹기 : 2
machine_id = 2  # 추후 자동으로 처리


# ==============================================================================
#  마킹 그룹 조회 ----------------------------------------------------------------
# ==============================================================================

class MarkList(APIView):
    def post(self, request, *args, **kwargs):
        try:
            machine_id = request.data['extra_machineID']
            MachineKey = request.data['extra_machineKey']
            if MachineKey != 'smart_robot_007':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                mark_list = AutoMarkMachine.objects.filter(machine_id=machine_id,
                                                           status=False,
                                                           work_select=True)
            except AutoMarkMachine.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            print('a')

            tmp_dict = {}
            for obj in mark_list:
                group = obj.ship_no + ',' + obj.por_no + ',' + obj.seq_no
                tmp_dict[group] = tmp_dict.get(group, 0) + obj.work_quantity
            print(tmp_dict)

            mark_dict = {}
            mark_list = []
            tmp = tmp_dict.keys()
            # print(tmp)
            for k in tmp:
                k_list = k.split(',')
                mark_dict['ship_no'] = k_list[0]
                mark_dict['por_no'] = k_list[1]
                mark_dict['seq_no'] = k_list[2]
                mark_dict['work_quantity'] = tmp_dict[k]
                mark_list.append(mark_dict)
                mark_dict = {}  # 비워주지 않으면 마지막 데이터로 리스트가 다 채워짐
            return Response(mark_list)
        except:
            return Response({'massage': 'Error'})


# ==============================================================================
#  마킹 그룹 작업 선택 ----------------------------------------------------------------
# ==============================================================================

class MarkGselect(APIView):
    def post(self, request, *args, **kwargs):
        try:
            machine_id = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'smart_robot_007':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            ship_no = request.data['project']
            por_no = request.data['por']
            seq_no = request.data['seq']
            print(ship_no)

            try:
                select_fields = AutoMarkMachine.objects.filter(machine_id=machine_id,
                                                                ship_no=ship_no,
                                                                por_no=por_no,
                                                                seq_no=seq_no)
                select_fields.update(work_select=True) # 일괄수정
                # select_fields.save() # 개별 수정시 적용
                return Response('Ok')

            except AutoMarkMachine.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'massage': 'Error'})


# ==============================================================================
#  마킹 그룹 선택 해제 ----------------------------------------------------------------
# ==============================================================================

class MarkGcancle(APIView):
    def post(self, request, *args, **kwargs):
        try:
            machine_id = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'smart_robot_007':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                select_fields = AutoMarkMachine.objects.filter(machine_id=machine_id,
                                                                status=True,
                                                               work_select=False)
                select_fields.update(work_select=False) # 일괄수정
                # select_fields.save() # 개별 수정시 적용
                return Response('Ok')

            except AutoMarkMachine.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except:
            return Response('Error')


# ==============================================================================
#  마킹 데이터 내려받기------------------------------------------------------------
# ==============================================================================

class MarkDataLoad(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # machine_id = request.data['MachineID']
            # MachineKey = request.data['MachineKey']
            # if MachineKey != 'smart_robot_007':
            #     return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                markdatas = AutoMarkMachine.objects.filter(machine_id=machine_id,
                                                            status=False,
                                                            work_select=True)
                print(markdatas)
                mark_list = []
                mark_dict = {}
                for m in markdatas:
                    if m.lot_no != None:
                        mark_dict['markdata'] = m.paint_code + ' ' + m.ship_no + ' ' + m.por_no + '-' + m.seq_no + \
                                ' ' + m.block_no + ' ' + m.pcs_no + ' ' + m.lot_no
                    else:
                        mark_dict['markdata'] = m.paint_code + ' ' + m.ship_no + ' ' + m.por_no + '-' + m.seq_no \
                                                + ' ' + m.block_no + ' ' + m.pcs_no
                    mark_dict['work_quantity'] = m.work_quantity
                    mark_dict['worked_quantity'] = m.worked_quantity
                    mark_list.append(mark_dict)
                    m.mark_data = mark_dict['markdata']
                    m.save()
                    mark_dict = {}

                return Response(mark_list)

            except AutoMarkMachine.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response('Error')


# ==============================================================================
#  마킹 실적 등록------------------------------------------------------------
# ==============================================================================

class MarkedData(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # machine_id = request.data['MachineID']
            # MachineKey = request.data['MachineKey']
            # if MachineKey != 'smart_robot_007':
            #     return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                markdatas = AutoMarkMachine.objects.filter(machine_id=machine_id,
                                                            status=False,
                                                            work_select=True)
                print(markdatas)
                mark_list = []
                mark_dict = {}
                for m in markdatas:
                    if m.lot_no != None:
                        mark_dict['markdata'] = m.paint_code + ' ' + m.ship_no + ' ' + m.por_no + '-' + m.seq_no + \
                                ' ' + m.block_no + ' ' + m.pcs_no + ' ' + m.lot_no
                    else:
                        mark_dict['markdata'] = m.paint_code + ' ' + m.ship_no + ' ' + m.por_no + '-' + m.seq_no \
                                                + ' ' + m.block_no + ' ' + m.pcs_no
                    mark_dict['work_quantity'] = m.work_quantity
                    mark_dict['worked_quantity'] = m.worked_quantity
                    mark_list.append(mark_dict)
                    mark_dict = {}

                return Response(mark_list)

            except AutoMarkMachine.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response('Error')


