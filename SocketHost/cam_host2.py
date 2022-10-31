import json
import os.path
import time
import numpy as np
import cv2
import requests
import socket, threading
from pypylon import genicam
from pypylon import pylon
import uuid

# from PIL import image


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
        recvdata = client_socket.recv(1024)
        recvstr = recvdata.decode('utf-8').split(',')
        print(recvstr)
        # 용도에 맞게 설정할 것
        command = recvstr[0]

        if camera.IsGrabbing():
            if grabResult.GrabSucceeded():
                g_grabResult = grabResult
                image = converter.Convert(g_grabResult)
                img = image.GetArray()

                myUUID = uuid.uuid1()
                cv2.imwrite(f'./image/{myUUID}.bmp', img)

                try:
                    if 'camshot' in command:
                        posturl = 'http://smart-robot.kr/code_master/rpcm_camshot/'
                        header = {
                            'Content-Type': 'application/json; charset=utf-8'}

                        image = open(f'./image/{myUUID}.bmp', 'rb')

                        files = {'image': image}
                        data = {'m_data': recvdata,
                                'machineKey': 'smart-robot-007'}
                        msg = requests.post(posturl, data=data, files=files,
                                            timeout=5).text
                        image.close()
                        os.remove(f'./image/{myUUID}.bmp')
                        client_socket.sendall(msg.encode())
                        print(msg)

                    else:
                        msg = 'NG,key_Error'
                        client_socket.sendall(msg.encode())
                        print(msg)
                    return
                except:
                    msg = 'Err,'
                    client_socket.sendall(msg.encode())
                    return
            else:
                msg = 'NG,Grab error'
                client_socket.sendall(msg.encode())
                print(msg)


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
                msg = 'NG,camera_Error'
                client_socket.sendall(msg.encode())
                continue
                # raise pylon.RUNTIME_EXCEPTION("No camera present.")

            for i in range(len(devices)):
                if devices[i].GetSerialNumber() == '23683422':
                    camera = pylon.InstantCamera(
                        tlFactory.CreateDevice(devices[i]))
                    camera.RegisterImageEventHandler(SampleImageEventHandler(),
                                                     pylon.RegistrationMode_Append,
                                                     pylon.Cleanup_Delete)

            camera.Open()
            camera.TriggerMode.SetValue('On')
            camera.ExposureTimeAbs.SetValue(30000)
            camera.TriggerSource.SetValue('Software')

            camera.StartGrabbing(pylon.GrabStrategy_OneByOne,
                                 pylon.GrabLoop_ProvidedByInstantCamera)

            if camera.IsGrabbing():
                try:
                    # time.sleep(0.05)
                    th = threading.Thread(
                        target=camera.ExecuteSoftwareTrigger(),
                        args=(client_socket, addr))
                    th.start()
                except:
                    print("NG,host_Error")
                    pass

        except genicam.GenericException as e:
            msg = 'camError'
            client_socket.sendall(msg.encode())
            pass
            # Error handling.
            # print("An exception occurred.", e.GetDescription())