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
        try:      

            print('Connected by', addr)
            recvdata = client_socket.recv(1024)
            recvstr = recvdata.decode('utf-8').split(',')
            print(recvstr)
            # 용도에 맞게 설정할 것
            command = recvstr[0]
            print(command)

            # camera.ExposureTimeAbs.SetValue(int(expos))
            
            if camera.IsGrabbing():
                print('step1')
                if grabResult.GrabSucceeded():
                    g_grabResult = grabResult
                    image = converter.Convert(g_grabResult)
                    img = image.GetArray()            
                    print(img.shape)
                    # cv2.imwrite('./image/cam.bmp', img)    
                    try:     
                        if 'camshot' in command: 
                            posturl = 'http://smart-robot.kr/code_master/rpcm_camshot/'
                            header = {'Content-Type': 'application/json; charset=utf-8'}
                            files = {'image': img}
                            data = {'m_data': recvdata,
                                    'machineKey': 'smart-robot-007'}
                            msg = requests.post(posturl, data=data, files=files, timeout = 50).text
                            client_socket.sendall(msg.encode())          
                
                        elif 'cmd_robot' in command:   
                            R_Result = Hi5_SEND_UDP.hi5_send(recvstr[1], recvstr[2], recvstr[3])
                            client_socket.sendall(('C_ROBOT,' + R_Result).encode())      # cmd 리턴                                           
                            
                        else:
                            msg='NG,not_command'
                            client_socket.sendall(msg.encode())        
                    except:
                        msg='NG,function_error'
                        client_socket.sendall(msg.encode())  
        except:
            msg='Err,'
            client_socket.sendall(msg.encode())  
            return
               
if __name__ == '__main__':
    while True:
        try:        
            HOST = '127.0.0.1'
            PORT = 9999
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print('Listen...')
            client_socket, addr = server_socket.accept()
            
            tlFactory = pylon.TlFactory.GetInstance()
            devices = tlFactory.EnumerateDevices()
            if len(devices) == 0:  # 카메라가 검색이 안될때
                try:
                    print('Connected by', addr)
                    recvdata = client_socket.recv(1024)
                    recvstr = recvdata.decode('utf-8').split(',')
                    # recvstr = command, 절대원점, 측정위치(현재위치), 자재정보(작업물정보), 매크로정보(작업정보)
                    # 측정위치(현재위치)는 먼저 로봇에게 받아서 사용
                    # 절대원점과 자재와의 위치관계, 카메라(빔) 스케일, 로봇 TCP와 카메라와의 위치관계
                    print(recvstr)
                    command = recvstr[0]
                    
                    if 'camshot' in command: 
                        posturl = 'http://smart-robot.kr/cam_master/rpcag_nocamshot/'
                        header = {'Content-Type': 'application/json; charset=utf-8'}
                        
                        data = {'m_data': recvdata,
                                'machineKey': 'smart-robot-007'}
                        msg = requests.post(posturl, data=data, timeout= 50).text
                        
                        R_Result = Hi5_SEND_UDP.hi5_send(recvstr[1], recvstr[2], recvstr[3])
                        client_socket.sendall(('C_ROBOT,' + R_Result).encode())                    
                    
                    elif 'cmd_robot' in command:
                        R_Result = Hi5_SEND_UDP.hi5_send(recvstr[1], recvstr[2], recvstr[3])
                        client_socket.sendall(('C_FUNC,' + R_Result).encode())
                                            
                    else:
                        msg='NG,not_command'
                        client_socket.sendall(msg.encode())                            
                    # continue   
                except:
                    msg='NG,function_error'
                    client_socket.sendall(msg.encode())  
            else:
                for i in range(len(devices)):
                    if devices[i].GetSerialNumber() == '24044362':
                        camera = pylon.InstantCamera(tlFactory.CreateDevice(devices[i]))
                        camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

                camera.Open()
                camera.TriggerMode.SetValue('On')
                camera.TriggerSource.SetValue('Software')

                camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)

                if camera.IsGrabbing():
                    try:
                        time.sleep(0.05)
                        th = threading.Thread(target=camera.ExecuteSoftwareTrigger(), args = (client_socket,addr))
                        # th = threading.Thread(target=function(), args = (client_socket,addr))
                        th.start()
                    except:
                        msg='NG,threading_error'
                        client_socket.sendall(msg.encode())  
                        pass  
                                
        except genicam.GenericException as e:
            msg='NG,camError'
            client_socket.sendall(msg.encode()) 
            pass   
            # Error handling...
            # print("An exception occurred.", e.GetDescription())   