import io
import json

from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import CamMaster
from .serializers import CamMasterSerializer
from . import camshot_rpcm_agcut, camshot_plate_chamfer
from PIL import Image, ImageGrab
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def result_img(request, format=None):
    UserID = request.GET['UserID']
    MachineID = request.GET['MachineID']
    data = CamMaster.objects.filter(UserID=UserID, MachineID=MachineID).last()
    result_image = data.result_image
    return render(request, 'cam_master/result_img.html',
                  {'result_image': result_image})

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def ncfile(request, format=None):
    machine_id = request.GET['MachineID']
    try:
        camdata = CamMaster.objects.filter(machine_id=machine_id).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except CamMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        machine_id = request.data['MachineID']
        ShotPostion = request.data['ShotPostion']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if machine_id == 'miju_rpcm_agcut':
            # --------------------------------------------------------
            uploaddata = {'machine_id': machine_id, 'origin_image': origin_image}
            serializer = CamMasterSerializer(data=uploaddata)
            if serializer.is_valid():
                serializer.save()
                # db delete--------------
                if CamMaster.objects.all().count() > 3:
                    obs = CamMaster.objects.all().first()
                    if obs:
                        obs.delete()
                resdata = camshot_rpcm_agcut.camshot(UserID, MachineID)
                return Response(resdata)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------------------------------------------------------------------------------
        elif machine_id == 'miju_plate_chamfer':
            # -------------------------------------------------------------------------------
            uploaddata = {'machine_id': machine_id, 'origin_image': origin_image}
            serializer = CamMasterSerializer(data=uploaddata)
            if serializer.is_valid():
                serializer.save()
                # db delete : 일정 수량만 저장--------------
                if CamMaster.objects.all().count() > 3:
                    obs = CamMaster.objects.all().first()
                    if obs:
                        obs.delete()
                resdata = camshot_plate_chamfer.camshot(machine_id)
                # 마지막 데이터의 ncfile 주소 구하기
                lastdata = CamMaster.objects.all().last()
                ncfile = lastdata.ncfile
                # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
                ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
                return Response(ncurl)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'Not_Machine'})

    except:
        return Response({'message': 'views_Error'})

#
# @api_view(['GET', 'PUT', 'DELETE'])
# def camshot_detail(request, pk, format=None):
#     try:
#         camdata = CamMaster.objects.get(pk=pk)
#     except CamMaster.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = CamMasterSerializer(camdata)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CamMasterSerializer(camdata, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         camdata.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
