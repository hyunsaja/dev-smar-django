import json
import os.path
import time
# import numpy as np
# import cv2
import requests
import socket, threading
from pypylon import genicam
from pypylon import pylon

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
        recvstr = data.decode('utf-8').split(',')
        # print(recvstr)

        # RPCM I/F 문자열 파싱
        cmd = recvstr[0]  # 응답시 OK or NG
        work_size = recvstr[1]   # NG 일때는 애러 메세지, OK이면 정상 파싱할것
        stan_value_X = recvstr[2]
        stan_value_Y = recvstr[3]
        stan_value_Z = recvstr[4]
        stan_adjust_X = recvstr[5]
        stan_adjust_Y = recvstr[6]
        stan_adjust_Z = recvstr[7]
        size_adjust_A = recvstr[8]
        size_adjust_B = recvstr[9]
        size_adjust_C = recvstr[10]
        size_adjust_D = recvstr[11]
        beam_adjust_MH = recvstr[12]

        # camera.ExposureTimeAbs.SetValue(int(expos))

        if camera.IsGrabbing():
            print('step1')
            if grabResult.GrabSucceeded():
                g_grabResult = grabResult
                image = converter.Convert(g_grabResult)
                img = image.GetArray()
                print(img.shape)
                try:
                    if 'camshot' in cmd:

                        posturl = 'http://127.0.0.1:8000/code_master/rpcm_camshot/'
                        header = {
                            'Content-Type': 'application/json; charset=utf-8'}
                        image = {'image': img}
                        data = {'user': 'miju_agcut_machine', 'cmd': 'camshot'}
                        msg = requests.post(posturl, headers=header, data=data,
                                            files=image, timeout=50).text
                    else:
                        msg = 'Key_Error'
                        client_socket.sendall(msg.encode())
                        print(msg)

                    return
                except:
                    msg = 'NG, Except_Error'
                    client_socket.sendall(msg.encode())
                    return


if __name__ == '__main__':
    while True:
        try:
            tlFactory = pylon.TlFactory.GetInstance()
            devices = tlFactory.EnumerateDevices()
            if len(devices) == 0:
                msg = 'NG, No camera present'
                client_socket.sendall(msg.encode())

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
            camera.TriggerSource.SetValue('Software')

            camera.StartGrabbing(pylon.GrabStrategy_OneByOne,
                                 pylon.GrabLoop_ProvidedByInstantCamera)

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
                    th = threading.Thread(
                        target=camera.ExecuteSoftwareTrigger(),
                        args=(client_socket, addr))
                    th.start()
                except:
                    print("Server_Error")
                    pass

        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.GetDescription())