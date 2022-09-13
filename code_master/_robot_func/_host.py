import json
import os.path
import time
# import numpy as np
# import cv2
import requests
import socket, threading
from pypylon import genicam
from pypylon import pylon
import Hi5_SEND_UDP
import py_rpcm_func
import py_axl_status
import py_AXL_dll


key = 0
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_Mono8 
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

global gGrabOk
gGrabOk = False
global gImg
global g_grabResult

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):        

        print('Connected by', addr)
        data = client_socket.recv(1024)
        recvstr = data.decode('utf-8').split('#')
        # print(recvstr)

        # 용도에 맞게 설정할 것
        command = recvstr[0]
        expos = recvstr[1]
        # exfun = recvstr[2]
        
        # camera.ExposureTimeAbs.SetValue(int(expos))
        
        if camera.IsGrabbing():
            print('step1')
            if grabResult.GrabSucceeded():
                g_grabResult = grabResult
                image = converter.Convert(g_grabResult)
                img = image.GetArray()                
                print(img.shape)
                try:          
                    if 'camshot' in command:
                        camera.ExposureTimeAbs.SetValue(int(expos))

                        posturl = 'http://127.0.0.1:8000/biz_master/camshot/'
                        header = {'Content-Type': 'application/json; charset=utf-8'}
                        image = {'image': img}  
                        data = {'user':'miju_agcut_machine', 'cmd':'camshot'}  
                        msg = requests.post(posturl, headers=header, data=data, files=image, timeout = 50).text
                    
                    elif 'test' in command: 
                        print(command)
                        geturl = 'http://127.0.0.1:8000/biz_master/blkcp_list/'
                        header = {'Content-Type': 'application/json; charset=utf-8'}
                        msg = requests.get(geturl, timeout = 50).text
                        client_socket.sendall(msg.encode())
                    
                    # 함수 추가해서 사용...
                    # elif 'jobcreate' in command:       
                    #     pass

                    ## =================================================================================== ##
                    elif 'C_ROBOT' in command:          # 로봇 관련 함수 호출
                        # if expos == 'SEND':       # josn 아니므로 구분 필요X
                        # 그러나 SEND 명령에 http용 통신 문자열 추가 #UserID, MachineID, MachineKey
                        # 그러므로 다른 C_ROBOT 명령끝에 # 추가
                        R_Result = Hi5_SEND_UDP.hi5_send(recvstr[1], recvstr[2], recvstr[3])
                        client_socket.sendall(('C_ROBOT,' + R_Result).encode())      # cmd 리턴
                   
                    elif 'C_FUNC' in command:           #일반 함수 관련 호출 : 작업중
                        F_Result = py_rpcm_func.rpcm_Func(recvstr[1], recvstr[2])   # 결과 = 'OK,로봇가공거리,콘베어이동거리,BlankArea'
                        client_socket.sendall(('C_FUNC,' + F_Result).encode())      # cmd 리턴
                    
                    elif 'C_STATUS_RUN' in command:     #아진 DLL 상태(DI, DO, 모션) 모니터링 실행
                        py_axl_status.axl_status(recvstr[1], recvstr[2])       # "S_RUN", "0/1"
                        client_socket.sendall(('C_STATUS_RUN,OK').encode())

                    elif 'C_DLL' in command:            # 아진 DLL(DI, DO, 모션) 관련 함수 호출 : 작업중
                        D_Result = py_AXL_dll.axl_func(recvstr[1], recvstr[2])
                        client_socket.sendall(('C_DLL,' + D_Result).encode())       # cmd 리턴
                    ## =================================================================================== ##

                    else:
                        msg = 'NotKey,'
                        client_socket.sendall(msg.encode()) 
                        print(msg) 
                        
                    return
                except:
                    msg='Err,'
                    client_socket.sendall(msg.encode())  
                    return
               
if __name__ == '__main__':
    while True:
        try:        
            tlFactory = pylon.TlFactory.GetInstance()
            devices = tlFactory.EnumerateDevices()
            if len(devices) == 0:
                raise pylon.RUNTIME_EXCEPTION("No camera present.")

            for i in range(len(devices)):
                if devices[i].GetSerialNumber() == '23683422':
                    camera = pylon.InstantCamera(tlFactory.CreateDevice(devices[i]))
                    camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

            camera.Open()
            camera.TriggerMode.SetValue('On')
            camera.TriggerSource.SetValue('Software')

            camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)

            time.sleep(0.05)
            HOST = '127.0.0.1'
            PORT = 9999
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()

            while camera.IsGrabbing():
                try:
                    print('Listen...')
                    time.sleep(0.05)
                    # 아진 함수 호출
                    client_socket, addr = server_socket.accept()
                    th = threading.Thread(target=camera.ExecuteSoftwareTrigger(), args = (client_socket,addr))
                    th.start()
                except:
                    print("Server_Error")  
                    pass  
                             
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.GetDescription())        