import io
import json

from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import PlateChamferMachine, RpcmS300Machine, RpcmAgcutMachine, CoamingMachine, MijuRobotWeldingMachine
from .serializers import PlateChamferSerializer, RpcmS300Serializer, RpcmAgcutSerializer, CoamingSerializer, MijuRobotWeldingSerializer
from . import camshot_rpcm_agcut, camshot_plate_chamfer, camshot_rpcm_s300, camshot_coaming, camshot_miju_robot_welding
from PIL import Image, ImageGrab
from django.views.decorators.csrf import csrf_exempt

# ==============================================================================
# Plate Chamfer Machine --------------------------------------------------------
# ==============================================================================

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def plate_chamfer_result_img(request, format=None):
    try:
        # cam_name = request.GET['cam_name']
        cam_name = 'plate_chamfer_machine'
        data = PlateChamferMachine.objects.filter(cam_name=cam_name).last()
        result_image = data.result_image
        return render(request, 'cam_master/plate_chamfer/result_img.html',
                      {'result_image': result_image})
    except PlateChamferMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def plate_chamfer_ncfile(request, format=None):
    try:
        cam_name = request.data['camName']
        machineKey = request.data['machineKey']
        if machineKey != 'smart-robot-007':
            return Response('Error')
        camdata = PlateChamferMachine.objects.filter(cam_name=cam_name).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except PlateChamferMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def plate_chamfer_camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        cam_name = request.data['camName']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------------------------
        uploaddata = {'cam_name': cam_name, 'origin_image': origin_image}
        serializer = PlateChamferSerializer(data=uploaddata)
        if serializer.is_valid():
            serializer.save()
            # db delete : 일정 수량만 저장--------------
            if PlateChamferMachine.objects.all().count() > 1000:
                obs = PlateChamferMachine.objects.all().first()
                if obs:
                    obs.delete()
            resdata = camshot_plate_chamfer.camshot(cam_name)
            # 마지막 데이터의 ncfile 주소 구하기
            lastdata = PlateChamferMachine.objects.all().last()
            ncfile = lastdata.ncfile
            # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
            ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
            return Response(ncurl)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response('Error')


# ==============================================================================
# RPCM S300 Machine --------------------------------------------------------
# ==============================================================================

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def rpcm_s300_result_img(request, format=None):
    try:
        # cam_name = request.GET['cam_name']
        cam_name = 'rpcm_s300_machine'
        data = RpcmS300Machine.objects.filter(cam_name=cam_name).last()
        result_image = data.result_image
        return render(request, 'cam_master/rpcm_s300/result_img.html',
                      {'result_image': result_image})
    except RpcmS300Machine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def rpcm_s300_ncfile(request, format=None):
    try:
        cam_name = request.data['camName']
        machineKey = request.data['machineKey']
        if machineKey != 'smart-robot-007':
            return Response('Error')
        camdata = RpcmS300Machine.objects.filter(cam_name=cam_name).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except RpcmS300Machine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def rpcm_s300_camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        cam_name = request.data['camName']
        material = request.data['material']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'smart-robot-007':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------------------------
        uploaddata = {'cam_name': cam_name, 'origin_image': origin_image}
        serializer = RpcmS300Serializer(data=uploaddata)
        if serializer.is_valid():
            serializer.save()
            # db delete : 일정 수량만 저장--------------
            if RpcmS300Machine.objects.all().count() > 1000:
                obs = RpcmS300Machine.objects.all().first()
                if obs:
                    obs.delete()
            resdata = camshot_rpcm_s300.camshot(cam_name)
            # 마지막 데이터의 ncfile 주소 구하기
            lastdata = RpcmS300Machine.objects.all().last()
            ncfile = lastdata.ncfile
            # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
            ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
            return Response(ncurl)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response('Error')



# ==============================================================================
# RPCM Agcut Machine -----------------------------------------------------------
# ==============================================================================

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def rpcm_agcut_result_img(request, format=None):
    try:
        # cam_name = request.GET['cam_name']
        cam_name = 'rpcm_agcut_machine'
        data = RpcmAgcutMachine.objects.filter(cam_name=cam_name).last()
        result_image = data.result_image
        return render(request, 'cam_master/rpcm_agcut/result_img.html',
                      {'result_image': result_image})
    except RpcmAgcutMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def rpcm_agcut_ncfile(request, format=None):
    try:
        cam_name = request.data['camName']
        machineKey = request.data['machineKey']
        if machineKey != 'smart-robot-007':
            return Response('Error')
        camdata = RpcmAgcutMachine.objects.filter(cam_name=cam_name).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except RpcmAgcutMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def rpcm_agcut_camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        cam_name = request.data['camName']
        material = request.data['material']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'smart-robot-007':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------------------------
        uploaddata = {'cam_name': cam_name, 'origin_image': origin_image}
        serializer = RpcmAgcutSerializer(data=uploaddata)
        if serializer.is_valid():
            serializer.save()
            # db delete : 일정 수량만 저장--------------
            if RpcmAgcutMachine.objects.all().count() > 1000:
                obs = RpcmAgcutMachine.objects.all().first()
                if obs:
                    obs.delete()
            resdata = camshot_rpcm_agcut.camshot(cam_name)
            # 마지막 데이터의 ncfile 주소 구하기
            lastdata = RpcmAgcutMachine.objects.all().last()
            ncfile = lastdata.ncfile
            # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
            ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
            return Response(ncurl)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response('Error')



# ==============================================================================
# Coaming Machine -----------------------------------------------------------
# ==============================================================================

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def coaming_result_img(request, format=None):
    try:
        # cam_name = request.GET['cam_name']
        cam_name = 'coaming_machine'
        data = CoamingMachine.objects.filter(cam_name=cam_name).last()
        result_image = data.result_image
        return render(request, 'cam_master/coaming/result_img.html',
                      {'result_image': result_image})
    except CoamingMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def coaming_ncfile(request, format=None):
    try:
        cam_name = request.data['camName']
        machineKey = request.data['machineKey']
        if machineKey != 'smart-robot-007':
            return Response('Error')
        camdata = CoamingMachine.objects.filter(cam_name=cam_name).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except CoamingMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def coaming_camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        cam_name = request.data['camName']
        material = request.data['material']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'smart-robot-007':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------------------------
        uploaddata = {'cam_name': cam_name, 'origin_image': origin_image}
        serializer = CoamingSerializer(data=uploaddata)
        if serializer.is_valid():
            serializer.save()
            # db delete : 일정 수량만 저장--------------
            if CoamingMachine.objects.all().count() > 1000:
                obs = CoamingMachine.objects.all().first()
                if obs:
                    obs.delete()
            resdata = camshot_coaming.camshot(cam_name)
            # 마지막 데이터의 ncfile 주소 구하기
            lastdata = CoamingMachine.objects.all().last()
            ncfile = lastdata.ncfile
            # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
            ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
            return Response(ncurl)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response('Error')



# ==============================================================================
# Miju Robot Welding Machine -----------------------------------------------------------
# ==============================================================================

# 결과 이미지 보기 ----------------------------------------------
@api_view(['GET'])
def miju_robot_welding_result_img(request, format=None):
    try:
        # cam_name = request.GET['cam_name']
        cam_name = 'coaming_machine'
        data = MijuRobotWeldingMachine.objects.filter(cam_name=cam_name).last()
        result_image = data.result_image
        return render(request, 'cam_master/miju_robot_welding/result_img.html',
                      {'result_image': result_image})
    except MijuRobotWeldingMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# NC file 보기 ----------------------------------------------
@api_view(['POST'])  # Error 발생, 원인 파악요
def miju_robot_welding_ncfile(request, format=None):
    try:
        cam_name = request.data['camName']
        machineKey = request.data['machineKey']
        if machineKey != 'smart-robot-007':
            return Response('Error')
        camdata = MijuRobotWeldingMachine.objects.filter(cam_name=cam_name).order_by('-id')[0]
        ncfile = camdata.ncfile
        return Response(ncfile.url)
    except MijuRobotWeldingMachine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 이미지 처리 기본 ----------------------------------------------------
@api_view(['POST'])
def miju_robot_welding_camshot(request, format=None):
    try:
        origin_image = request.FILES['origin_image']
        cam_name = request.data['camName']
        material = request.data['material']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'smart-robot-007':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------------------------
        uploaddata = {'cam_name': cam_name, 'origin_image': origin_image}
        serializer = MijuRobotWeldingSerializer(data=uploaddata)
        if serializer.is_valid():
            serializer.save()
            # db delete : 일정 수량만 저장--------------
            if MijuRobotWeldingMachine.objects.all().count() > 1000:
                obs = MijuRobotWeldingMachine.objects.all().first()
                if obs:
                    obs.delete()
            resdata = camshot_miju_robot_welding.camshot(cam_name)
            # 마지막 데이터의 ncfile 주소 구하기
            lastdata = MijuRobotWeldingMachine.objects.all().last()
            ncfile = lastdata.ncfile
            # ncurl = 'http://127.0.0.1:8000' + ncfile.url  # 로컬 서버 테스트
            ncurl = 'http://smart-robot.kr' + ncfile.url  # 클라우드 서버 환경
            return Response(ncurl)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response('Error')


