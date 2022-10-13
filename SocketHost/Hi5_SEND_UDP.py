import socket
import time
import json
# import mdlPosAngle      # ~> To Web
import requests


# "HOME#620.0,0.0,400.0,0.0,0.0,0.0"     #"&H0609"
# "STAN#620.0,0.0,400.0,0.0,0.0,0.0"
# "TIP#620.0,0.0,400.0,0.0,0.0,0.0"
# "VISION#"620.0,0.0,400.0,0.0,0.0,0.0"

# "CONNECTED   #0"   # 0은 사용을 위한 대응값(의미X)
# "DISCONNECTED#0"   # 0은 사용을 위한 대응값(의미X)

# "SEND#0.0,0.0,500.0,180.0,0.0,-180.0$EA 50*50*6T$294,EA015,90,43,0,0,12$45$45$"+"0$1$0$1$0$1$0$1$0$1$SS400"


def hi5_send(R_CMD, R_VALUE, UserStr):
    
    try:

        Result_Str = ""         # 결과 송부
        CK_Listen = True        # JOB 생성 작업 구분 ~ 이벤트 대응 : True 최초 실행이 되도록!

        bufsize = 1024
        udpserver_addr = ("192.168.100.100", 8100)
        hi5_addr=('192.168.100.11', 8100)

        # server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # TCP : socket.SOCK_STREAM
        sock.bind(udpserver_addr)

        resOK = True
        d_Num = 1        #일반(1) / 수직(13)
        d_count = 0
        err_count = 0

        if R_CMD == "SEND":
            # -------------------------------------
            # http 통신용 문자열
            # -------------------------------------
            user_buf = UserStr.split(',')
            UserID = user_buf[0]
            MachineID = user_buf[1]
            MachineKey = user_buf[2]
            # -------------------------------------
            return_buf = []     #빈 리스트 생성
            dataArr = []        #빈 리스트 생성
            VAL_buf = str(R_VALUE).split('$')
            stan_pos = list(map(float, VAL_buf[0].split(',')))    #자재기준 : 각 원소들을 float로 변경
            worksize = VAL_buf[1]       # 자재 종류
            texture = VAL_buf[15]       # 재질
            sizekind = str(VAL_buf[1])[0:2]        # 자재 종류 : EA 고정

            if sizekind == 'PI':
                Size_buf = worksize.split('-')
                worksize = 'PI ' + str(int(Size_buf[2].replace('T','')))        # int 처리
            elif sizekind == 'SP':
                Size_buf = worksize.split('*')
                worksize = 'SP ' + str(Size_buf[2].replace('T',''))

            #===================================================================
            # Velocity_buf = "00250.0 00022.0 00018.0 00018.0 00020.0 00018.0 00000.5 00000.5 00000.3 00000.1 00022.0 00018.0"
            # 속도값 Web DB에서 로드하기 ~ #7자리 .zfill(7)       
            header = {'Content-Type': 'application/json; charset=utf-8'}
            posturl = 'http://smart-robot.kr/biz_master/speed_list/'
            data = { "UserID": UserID, "MachineID": MachineID, "MachineKey": MachineKey, "cmd": "RD_velocity", "worksize": worksize, "texture": texture }
            msg = requests.post(posturl, headers=header, data=json.dumps(data), timeout = 50).text
            # -----------
            #  V_Buf = ["400", "22", "18", "18", "20", "18", "0.5", "0.5", "0.3", "0.1", "22", "18", "0.7"]
            V_Buf = json.JSONDecoder().decode(json.loads(msg))
            Velocity_buf=''
            for vv in V_Buf[0:12]:    #range(0,12):
                Velocity_buf = Velocity_buf + ' ' + vv.zfill(7)
            edgeadd = float(V_Buf[12])      # 사각귀 보정값
            #===================================================================
            #dataArr = mdlPosAngleEA.func_ang_pose(R_VALUE)     # JOB 생성 <~ DLL_VAL    # ~> To Web
            # Web 함수에서 내용 받기 ~ #8자리
            posturl = 'http://smart-robot.kr/biz_master/macro_list/'
            data = { "UserID": UserID, "MachineID": MachineID, "MachineKey": MachineKey, "cmd": "FN_mdlPos", "sizekind": sizekind, "r_value": R_VALUE, "edgeadd": edgeadd }
            msg = requests.post(posturl, headers=header, data=json.dumps(data), timeout = 50).text
            # -----------
            # return_buf = ["JOBMAKE_RES= 0004001 0000004","0,0,0,0,0,0","0,0,0,0,0,0","0,0,0,0,0,0","0,0,0,0,0,0"]
            return_buf = json.loads(msg)    
            #===================================================================

            dataArr.append(return_buf[0] + ' ' + Velocity_buf)           #7자리     
            # return_buf.remove(return_buf[0])   # 첫번째 항목 제거
            for pose_buf in return_buf[1:]:         # 기준값 적용 = 로봇 자세값은 기준값에서 얻는다! (U1:유저 좌표계)
                a1 = str(round(pose_buf[0] + stan_pos[0], 3)).zfill(8) + ' '
                # a2 = str(round((-1 * pose_buf[1]) + stan_pos[1], 3)).zfill(8) + ' '
                a2 = str(round(pose_buf[1] + stan_pos[1], 3)).zfill(8) + ' '
                a3 = str(round(pose_buf[2] + stan_pos[2], 3)).zfill(8) + ' '
                a4 = str(round(pose_buf[3] + stan_pos[3], 3)).zfill(8) + ' '
                a5 = str(round(pose_buf[4] + stan_pos[4], 3)).zfill(8) + ' '
                a6 = str(round(pose_buf[5] + stan_pos[5], 3)).zfill(8)
                dataArr.append(a1 + a2 + a3 + a4 + a5 + a6)

            d_Num = int(dataArr[0][21:28])      # Pose수
                    
            while CK_Listen==True:
                if d_Num < d_count :
                    CK_Listen = False
                    Result_Str = "OK,end_SEND"
                else:
                    if resOK == True:
                        send_str = dataArr[d_count] + "\n"
                        sock.sendto(send_str.encode(), hi5_addr)
                        time.sleep(0.02) # 시간지연
                        resOK = False
                    else:
                        L_data, hi5_addr = sock.recvfrom(bufsize)
                        L_data = L_data.decode()

                        if L_data.startswith(send_str) == True:
                            # print(L_data)
                            d_count += 1
                            resOK = True
                        else:
                            if err_count >= 10:
                                CK_Listen = False
                                Result_Str = "NG,error pose SEND"
                            else :
                                err_count += 1

        elif (R_CMD == "HOME") or (R_CMD == "STAN") or (R_CMD == "TIP") or (R_CMD == "VISION"):
            dataArr = []     #빈 리스트 생성
            dataArr.append("JOBMAKE_RES= 000" + '4101' + '0000001' + ' ' + '00250.0 00030.0 00025.0 00025.0 00025.0 00018.0 00000.3 00000.5 00000.3 00000.1 00030.0 00025.0')
            p_buf = str(R_VALUE).split(',')     # '620.0,0.0,1300.0,0.0,0.0,0.0'
            a1 = p_buf[0].zfill(8) + ' '
            a2 = p_buf[1].zfill(8) + ' '
            a3 = p_buf[2].zfill(8) + ' '
            a4 = p_buf[3].zfill(8) + ' '
            a5 = p_buf[4].zfill(8) + ' '
            a6 = p_buf[5].zfill(8)
            dataArr.append(a1 + a2 + a3 + a4 + a5 + a6)

            while CK_Listen==True:
                if d_Num < d_count :
                    CK_Listen = False
                    Result_Str = "OK,end_" + R_CMD
                else:
                    if resOK == True:
                        send_str = dataArr[d_count] + "\n"
                        sock.sendto(send_str.encode(), hi5_addr)
                        time.sleep(0.02) # 시간지연
                        resOK = False
                    else:
                        L_data, hi5_addr = sock.recvfrom(bufsize)
                        L_data = L_data.decode()

                        if L_data.startswith(send_str) == True:
                            # print(L_data)
                            d_count += 1
                            resOK = True
                        else:
                            if err_count >= 10:
                                CK_Listen = False
                                Result_Str = "NG,error pose" + R_CMD
                            else :
                                err_count += 1

        else:
            send_str = R_CMD + "\n"         # <~ "CONNECTED   ", "DISCONNECTED" :12자리
            sock.sendto(send_str.encode(), hi5_addr)
            Result_Str = 'OK,end_' + R_CMD

        sock.close()
        # print(Result_Str)
        return (Result_Str)     #결과 리턴        

    except:
        # print("error occured")       # 에러 메시지
        return 'NG,error occured'



# def Result_send(result_msg):      # 비사용 제거
#     sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock2.connect(("127.0.0.1", 9998))
#     sock2.send(result_msg.encode())
#     sock2.close()


# Test용
# hi5_send("HOME","000620.0 000000.0 001300.0 000000.0 000000.0 000000.0")