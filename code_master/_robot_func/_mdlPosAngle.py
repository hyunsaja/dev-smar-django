import math
import json


    # # HH7용
    # # 최종 리턴에서 str(roune(????, 3)).zfill(8) + ' '
    # return_arr.append("JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7) + ' ' + func_Set_Vel(Ang_T))           #7자리
    # for pose_buf in return_buf:         # 기준값 적용 및 로봇 자세 변환
    #     a1 = str(round(pose_buf[0] + stan_pos[0], 3)).zfill(8) + ' '
    #     a2 = str(round((-1 * pose_buf[1]) + stan_pos[1], 3)).zfill(8) + ' '
    #     a3 = str(round(pose_buf[2] + stan_pos[2], 3)).zfill(8) + ' '
    #     a4 = str(round(pose_buf[3] + stan_pos[3], 3)).zfill(8) + ' '
    #     a5 = str(round(pose_buf[4] + stan_pos[4], 3)).zfill(8) + ' '
    #     a6 = str(round(pose_buf[5] + stan_pos[5], 3)).zfill(8)     # 로봇 자세값은 기준값에서 얻는다!
    #     return_arr.append(a1 + a2 + a3 + a4 + a5 + a6)

    # # # print(return_buf[0])

    # # # HP6 & TEST용 
    # # # 최종 리턴에서 str(roune(????, 3)).zfill(8) + ' '
    # # return_arr.append("JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7) + ' ' + func_Set_Vel(Ang_T))           #7자리
    # # for pose_buf in return_buf:         # 기준값 적용 및 로봇 자세 변환        
    # #     a1 = str(round((-1 * pose_buf[2]) + stan_pos[0], 3)).zfill(8) + ' '
    # #     a2 = str(round(pose_buf[1] + stan_pos[1], 3)).zfill(8) + ' '
    # #     a3 = str(round(pose_buf[0] + stan_pos[2], 3)).zfill(8) + ' '
    # #     a4 = str(round((-1 * pose_buf[5]) + stan_pos[3], 3)).zfill(8) + ' '
    # #     a5 = str(round(pose_buf[4] + stan_pos[4], 3)).zfill(8) + ' '
    # #     a6 = str(round(pose_buf[3] + stan_pos[5], 3)).zfill(8)     # 로봇 자세값은 기준값에서 얻는다!
    # #     return_arr.append(a1 + a2 + a3 + a4 + a5 + a6)

    # return return_arr

# 앵글(EA, UA) 로봇 가공 pose 생성 함수
# GEdgeAdd: 사각귀 보정값
def func_ang_pose(DLL_VAL, GEdgeAdd):

    global JOB_NO
    global Pos_Num
    
    #===================================================================
    # "SEND", "0.0 0.0 500.0 180.0 0.0 -180.0,EA 50*50*6T,294 EA015 90 43 0 0 12,3,45,45,False,0,40,0"
    # SEND "0.0,0.0,500.0,180.0,0.0,-180.0$EA 50*50*6T$294,EA015,90,43,0,0,12$ 등

    VAL_buf = str(DLL_VAL).split('$')
    
    if VAL_buf[1].startswith('EA'):
        # Size_buf = VAL_buf[1].replace('EA ','')
        Size_buf = VAL_buf[1][3:]               # 'EA ', 'UA ' 제거
        Size_buf = Size_buf.split('*')
        Ang_S = float(Size_buf[0])
        Ang_L = float(Size_buf[1])
        Ang_T = float(Size_buf[2].replace('T',''))
        Ang_T2 = Ang_T
    else:
        Size_buf = VAL_buf[1][3:]               # 'EA ', 'UA ' 제거
        Size_buf2 = Size_buf.split('/')
        Size_buf = Size_buf2[0].split('*')
        Ang_S = float(Size_buf[0])
        Ang_L = float(Size_buf[1])
        Ang_T = float(Size_buf[2])
        Ang_T2 = float(Size_buf2[1].replace('T',''))

    A_Code = str(VAL_buf[2]).split(',')         # ~> ["294","EA015","90","43","0","0","12"]    
    c_code = A_Code[1][2:]                      # EA, UA 제거 <~ (A_Code[1]).replace(find_size,'') 
    Ang_a = float(A_Code[2])
    Ang_b = float(A_Code[3])
    Ang_c = float(A_Code[4])
    Ang_d = float(A_Code[5])
    Ang_Lenth = float(A_Code[0])
    
    # GCutLoss = float(VAL_buf[3])
    # Calc_DegreeH = float(VAL_buf[4])
    # Calc_DegreeL = float(VAL_buf[5])
    # GWorkEnd = VAL_buf[6]
    # GE_CutLast = float(VAL_buf[7])    
    # GRobotLen = float(VAL_buf[8])
    # GDblJobExecCode = int(VAL_buf[9])

    Calc_DegreeH = float(VAL_buf[3])
    Calc_DegreeL = float(VAL_buf[4])
    GSizeAdjustA = float(VAL_buf[5])
    GSizeAdjustB = float(VAL_buf[6])
    GWorkEnd = int(VAL_buf[7])
    GVCutTAdj = int(VAL_buf[8])
    GVCutGapAdj = float(VAL_buf[9])
    GV_Remain = int(VAL_buf[10])
    GRobotLen = float(VAL_buf[11])
    GDblJobExecCode = int(VAL_buf[12])
    GWorkPosition = int(VAL_buf[13])
    GE_CutLast = float(VAL_buf[14])
    # 재질 = [15]

    #===================================================================    
    #===================================================================
   
    # 스닙 보정값
    SNIP_Adj = 0.4          #스닙의 깨끗한 절단을 위해 0.5=>0.4 보정 [11.03.15]
    EDGE_C_Rate = 0.1       # 사각귀의 C값 0.6 + 0.1 되는 형태로
    
    # 사각귀 관련 : 비사용 형태 대응
    GES_Use = False    
    GES_Shift = Ang_T       #??
    GES_Adjust = 0
    GES_Angle = 30

    GCutLoss = 3            # 절단손실:고정값
    GCircleLoss2 = 1.3
    GCircleLoss = 2
    

    # 옆면 가공 로봇 자세 설정값[사각귀S개선에서 사용[13.05.30]
    H_RZ_1 = 45            # 로봇 옆면 가공 RZ_1 각도
    H_RZ_2 = -45           # 로봇 옆면 가공 RZ_2 각도

    C_RadianH = round(Calc_DegreeH * math.pi / 180, 3)      #라디안 =  각도 * 파이(PI)/180
    C_RadianL = round(Calc_DegreeL * math.pi / 180, 3)

    GPlasmaP_H = 9      #피어싱 높이

    #피어싱 띄우기(상부)    
    PlasmaP_H_Y = (GPlasmaP_H - 6) * math.sin(C_RadianH)    #6:TCPGAP
    PlasmaP_H_Z = (GPlasmaP_H - 6) * math.cos(C_RadianH)

    #피어싱 띄우기(하부)    
    PlasmaP_L_Y = (GPlasmaP_H - 6) * math.sin(C_RadianL)    #6:TCPGAP
    PlasmaP_L_Z = (GPlasmaP_H - 6) * math.cos(C_RadianL)
    
    #프라즈마 절단 Loss
    PlasmaCutLoss = GCutLoss / 2

    Margin_Y = 50
    Margin_Z = 70
    EDGE_M_Adj = (Ang_T * 0.2)        # HI5 : 사각귀 등반 중심점 보정용 (T*0.2) [11.03.15]
    EDGE_IN_Degree = 8      #37<~30

    # PlasmaGAP_HY = 0    #0 * math.sin(C_RadianH)     #비사용
    # PlasmaGAP_HZ = 0    #0 * math.cos(C_RadianH)     #비사용
    # PlasmaGAP_LY = 0    #0 * math.sin(C_RadianL)     #비사용
    # PlasmaGAP_LZ = 0    #0 * math.cos(C_RadianL)     #비사용

    # 자재 실제 크기 보정 (A & B)
    Ang_S = Ang_S + GSizeAdjustA
    Ang_L = Ang_L + GSizeAdjustB
    
    pose_Arr=[]     #빈 리스트 생성

    cal_robx = 0.0
    cal_roby = 0.0
    cal_robz = 0.0
    cal_rx = 0.0
    cal_ry = 0.0
    cal_rz = 0.0

    try:

        if c_code == "000":         #수직절단

            if GWorkEnd == True and GE_CutLast > 999:    # 우 사각귀 하 일 때 : 4       ##SW 작업중 ~ 조건 점검
                JOB_NO = "4051 "
                Pos_Num = 4

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 앵글 마지막 피스 수직 절단 보상용 계산
                GE_CutLast = (GE_CutLast - 999)

                cal_roby = -(GE_CutLast - 2) * math.cos(C_RadianH)
                cal_robz = -(GE_CutLast - 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = 20       # X+20위치
                cal_roby = -(GE_CutLast - 2) * math.cos(C_RadianL) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            else:           # 그 외의 수직 절단 : 일반
                JOB_NO = "4000 "
                Pos_Num = 13

                #시작 이동 중간점(0)
                cal_robx = 0.0 
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #시작점
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -(Ang_T2 * 1.5) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 1.5) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 20
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -(Ang_T2 * 1.2) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 1.2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 25
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -(Ang_T2 * 0.9) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 0.9) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 30
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -(Ang_T2 / 2) * math.cos(C_RadianH) - 1
                cal_robz = -(Ang_T2 / 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 35
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Ang_T / 3) * math.cos(C_RadianL) + 1
                cal_robz = -(Ang_T / 3) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 35
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Ang_T * 0.9) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 0.9) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 30
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Ang_T * 1.2) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 1.2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 25
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Ang_T * 1.5) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 1.5) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 20
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Ang_L) * math.cos(C_RadianL) + 2           # 최종 절단은 좀더 아래로
                cal_robz = -(Ang_L) * math.sin(C_RadianL) - 2          # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = 20.0          # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

        elif c_code == "005" or c_code == "025":       #대각절단: 좌, 우        ##SW 작업중 ~ 대각절단....
            JOB_NO = "4005 "

            # 제일 긴 값:Calc_Cen
            if Ang_a <= Ang_b:
                if Ang_b <= Ang_c:
                    Calc_Cen = Ang_c
                else:
                    Calc_Cen = Ang_b                
            elif Ang_a <= Ang_c:
                Calc_Cen = Ang_c
            else:
                Calc_Cen = Ang_a            

            # 우 대각 절단은 크기가 반대가 되므로 그 이전에 구한다.
            if (Ang_a >= Ang_b):   # T만큼 각도값도 보정한다.
                SP1_OK = True
                Ang_a = Ang_a - (Ang_a - Ang_b) * Ang_T2 / Ang_S
            else:
                SP1_OK = False      # 값이 유지 되는 에러 발생 : IF 문에 대한 False 꼭 추가 [11.03.18]
            
            if (Ang_c >= Ang_b):
                SP2_OK = True
                Ang_c = Ang_c - (Ang_c - Ang_b) * Ang_T / Ang_L
            else:
                SP2_OK = False     # 값이 유지 되는 에러 발생 : IF 문에 대한 False 꼭 추가 [11.03.18]

            # 25 : 우 절단 구분은 각각 아래에서....

            # 두 점이 0인 것에 대한 구분
            if (Ang_a == 0 and Ang_b == 0):

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # 두 점이 0인 것의 0아닌 부분만 짜른다. 우 절단의 마무리는 수직절단으로 한다.
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                Pos_Num = 8

                if c_code == "025":   # 우 절단
                    PlasmaCutLoss = 0   #우 대각은 절단손실 적용은 콘베어 이동에서
                    Ang_a = Calc_Cen - Ang_a
                    Ang_b = Calc_Cen - Ang_b
                    Ang_c = Calc_Cen - Ang_c
                else:    # 좌 절단
                    Ang_L = Ang_S
                    C_RadianL = C_RadianH                


                # 시작 이동 중간점(0)
                cal_robx = -Ang_c + PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Ang_c + PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL)
                cal_robz = -(Ang_L) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 수직으로 각도 변화 없는 행정으로...
                ##if (Ang_c >= Ang_b):
                if SP2_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T * 1.0) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                
                cal_roby = (Ang_T * 1.0) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 1.0) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL   ##+ 20
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##if (Ang_c >= Ang_b):
                if SP2_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T * 0.7) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                
                cal_roby = (Ang_T * 0.7) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 10  #25
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##if (Ang_c >= Ang_b):
                if SP2_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T * 0.5) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                
                cal_roby = (Ang_T * 0.5) * math.cos(C_RadianL)
                cal_robz = -(Ang_T * 0.5) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 20  #30
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##if (Ang_c >= Ang_b):
                if SP2_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T * 0.3) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                
                cal_roby = (Ang_T * 0.3) * math.cos(C_RadianL)    # /2 -> /3 : 좀 더 위로..
                cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + 30
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -Ang_b + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = -Calc_DegreeL + 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -Ang_b + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            else:

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # 두 점이 0인 것의 0아닌 부분만 짜른다. 우 절단의 마무리는 수직절단으로 한다.
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if (Ang_b == 0 and Ang_c == 0):
                    Pos_Num = 8
                else:
                    Pos_Num = 13
                
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                if c_code == "025":   # 우 절단
                    PlasmaCutLoss = 0   #우 대각은 절단손실 적용은 콘베어 이동에서
                    Ang_a = Calc_Cen - Ang_a
                    Ang_b = Calc_Cen - Ang_b
                    Ang_c = Calc_Cen - Ang_c

                # 시작 이동 중간점(0)
                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y        #Y-50위치
                cal_robz = Margin_Z        #Z+50위치

                # 시작점
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # 좌 대각절단 중에 시작점(a)이 "0"인 경우 [09.07.14]
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if c_code == "005" and Ang_a == 0:
                    cal_robx = 0.0       # 플라즈마 불꽃 꺼짐 현상을 위한 보정(PlasmaCutLoss를 빼지 않는다.)
                    # PlasmaCutLoss에 대한 등변값을 계산하여 빼준다.(Ang_b>0이다)
                    ##cal_roby = -(Ang_S - (PlasmaCutLoss * Ang_S / Ang_b)) * math.cos(C_RadianH)
                    ##cal_robz = -(Ang_S - (PlasmaCutLoss * Ang_S / Ang_b)) * math.sin(C_RadianH)

                    # 수정 [11.03.16]
                    if (PlasmaCutLoss * math.tan(math.atan(Ang_S / Ang_b))) < (Ang_S - Ang_T2):
                        cal_roby = -(Ang_S - (PlasmaCutLoss * math.tan(math.atan(Ang_S / Ang_b)))) * math.cos(C_RadianH)
                        cal_robz = -(Ang_S - (PlasmaCutLoss * math.tan(math.atan(Ang_S / Ang_b)))) * math.sin(C_RadianH)
                    else:
                        cal_roby = -(Ang_T2) * math.cos(C_RadianH)
                        cal_robz = -(Ang_T2) * math.sin(C_RadianH)

                else:
                    cal_robx = -Ang_a + PlasmaCutLoss
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 수직으로 각도 변화 없는 행정으로...
                ##if (Ang_a >= Ang_b):
                if SP1_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T2 * 1.0) / (Ang_S / (Ang_a - Ang_b)) + PlasmaCutLoss   # /Tan 각도=(Ang_S / Ang_a)
                
                cal_roby = -(Ang_T2 * 1.0) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 1.0) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH    ##- 20
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##if (Ang_a >= Ang_b):
                if SP1_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T2 * 0.7) / (Ang_S / (Ang_a - Ang_b)) + PlasmaCutLoss  # /Tan 각도=(Ang_S / Ang_a)
                
                cal_roby = -(Ang_T2 * 0.7) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 0.7) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 10   #25
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##if (Ang_a >= Ang_b):
                if SP1_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss
                else:
                    cal_robx = -Ang_b - (Ang_T2 * 0.5) / (Ang_S / (Ang_a - Ang_b)) + PlasmaCutLoss  # /Tan 각도=(Ang_S / Ang_a)
                
                cal_roby = -(Ang_T2 * 0.5) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 0.5) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 20   #30
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # 좌 대각절단 중에 a,c > 0 and b=0인 경우도 플라즈마 꺼짐 현상에 대한 보정(-1mm) - 아래 4곳
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #V_Thinkness = IIf((Val(Mid(WorkCode, 2, 2)) == 5 and Ang_a > 0 and Ang_c > 0 and Ang_b == 0), 1, 0)   
                if (c_code == "005" and Ang_a > 0 and Ang_c > 0 and Ang_b == 0):
                    V_Thinkness = 1     # 변수 활용
                else:
                    V_Thinkness = 0
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                ##if (Ang_a >= Ang_b):
                if SP1_OK:
                    cal_robx = -Ang_b + PlasmaCutLoss - (V_Thinkness)      # 꺼짐 현상에 대한 보정
                else:
                    cal_robx = -Ang_b - (Ang_T2 * 0.3) / (Ang_S / (Ang_a - Ang_b)) + PlasmaCutLoss # /Tan 각도=(Ang_S / Ang_a)
                
                cal_roby = -(Ang_T2 * 0.3) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2 * 0.3) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - 30       #15     # 부등변을 위해 수정 [11.06.20]
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -Ang_b + PlasmaCutLoss - (V_Thinkness)      # 꺼짐 현상에 대한 보정
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45       #0     # 부등변을 위해 수정 [11.06.20]
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##if (Ang_b == 0 and Ang_c == 0):
                # if Pos_Num == 8:    # 수정 [11.03.16] : 우 대각 절단은 연산에 의해 위의 조건이 바뀌므로...
                #     # cal_pl_acc = P_OFF_PA      # PL=0/A=0
                #     # cal_P_state = 2      # 플라즈마 OFF
                #     # P_NO = P_NO + 1
                # else:
                
                if Pos_Num != 8:
                    JOB_NO = "4061 "

                    ##if (Ang_c >= Ang_b):
                    if SP2_OK:
                        cal_robx = -Ang_b + PlasmaCutLoss - (V_Thinkness)      # 꺼짐 현상에 대한 보정
                    else:
                        cal_robx = -Ang_b - (Ang_T * 0.3) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.3) * math.cos(C_RadianL)    # /2 -> /3 : 좀 더 위로..
                    cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 30      #-15     # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    ##if (Ang_c >= Ang_b):
                    if SP2_OK:
                        cal_robx = -Ang_b + PlasmaCutLoss - (V_Thinkness)      # 꺼짐 현상에 대한 보정
                    else:
                        cal_robx = -Ang_b - (Ang_T * 0.5) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.5) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.5) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 20
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    ##if (Ang_c >= Ang_b):
                    if SP2_OK:
                        cal_robx = -Ang_b + PlasmaCutLoss
                    else:
                        cal_robx = -Ang_b - (Ang_T * 0.7) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.7) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정으로...
                    ##if (Ang_c >= Ang_b):
                    if SP2_OK:
                        cal_robx = -Ang_b + PlasmaCutLoss
                    else:
                        cal_robx = -Ang_b - (Ang_T * 1.0) / (Ang_S / (Ang_c - Ang_b)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 1.0) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 1.0) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -Ang_c + PlasmaCutLoss
                    cal_roby = (Ang_L) * math.cos(C_RadianL) + 1            # 최종 절단은 좀더 아래로
                    cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1           # 최종 절단은 좀더 아래로
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # 복귀 이동 중간점(1)
                cal_robx = -Ang_c + PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

        else:       #상(좌 가공 ... 중간가공 .... 우 가공 ...) / 하(좌 가공 ... 중간가공 .... 우 가공 ...)

            # ===========================================================================
            # 상부 가공
            # ===========================================================================

            # 좌 가공 : 상 --------------------------------------------------------------
            if c_code == "001":         # 좌 스닙
                JOB_NO = "4001 "
                Pos_Num = 4
                
                # 시작 이동 중간점(0)
                #cal_robx = 0.0
                cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = SNIP_Adj
                cal_roby = -((Ang_S - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -((Ang_S - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Ang_a + 1) - PlasmaCutLoss)
                cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a + 1) - PlasmaCutLoss) + 20     # X+20위치
                cal_roby = -(Ang_S + 1) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "002":       # 좌 각모
                JOB_NO = "4002 "
                Pos_Num = 6

                # 시작 이동 중간점(0)
                # cal_robx = 0.0
                cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Ang_c == 0: 
                    Ang_c = Ang_b 
                    Ang_d = 0

                if Ang_d >= 500:     # 사선형 각모
                    Ang_d = Ang_d - 500

                    # 시작점
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a - Ang_d) - PlasmaCutLoss)
                    cal_roby = -((Ang_S - Ang_c) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_c) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:

                    # 시작점
                    cal_roby = -((Ang_S - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_d) - PlasmaCutLoss)   #/ Sqrt(2)
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)   #/ Sqrt(2)
                    cal_roby = -((Ang_S - Ang_c) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_c) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a) - PlasmaCutLoss) + 20     # X+20위치
                cal_roby = -(Ang_S + 1) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "003":       # 좌 사각귀
                JOB_NO = "4003 "
                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30]
                    if Ang_a > Ang_b:       #중심에 수직으로 세우는 형태로 수정 : 2P 추가 [13.07.24]
                        Pos_Num = 12
                    else:
                        Pos_Num = 10
                else:
                    Pos_Num = 11

                # 사각귀 안쪽 1mm 작게(+1mm) 추가 [08.10.21]
                Ang_a = Ang_a + 1 
                Ang_b = Ang_b + 1
                #+++++++++++++++++++++++++++++++++++++++++++
                # 사각귀 안쪽 스닙 부분 조금 더 작게 [08.10.21]
                # (비율 0.7 => 0.6)   ' 안 스닙 더 작게
                #+++++++++++++++++++++++++++++++++++++++++++

                if (Ang_b - Ang_a) == 0:
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Ang_S + Ang_T) / (Ang_b - Ang_a)

                # 민사각귀 구분 및 오류 방지
                if Ang_d > 100:
                    DirectEdge = True
                    Ang_d = float(A_Code[5])        #float(A_Code[13:15])        # <~ str(Ang_d)[1:2]
                else:
                    DirectEdge = False
                    if Ang_d == 0: 
                        Ang_d = Ang_c     # 이전 자료 보완 # Ang_d = Ang_d


                # 시작 이동 중간점(0)
                # cal_robx = 0.0
                cal_roby = (Ang_c + Ang_c * 0.7) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if DirectEdge:      # 민사각귀
                    # 시작점
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree   #-37<--30    ' 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                else:
                    # 시작점
                    cal_roby = (Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_c * (0.6 + EDGE_C_Rate))
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # 확장형 상수d 적용
                cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                cal_roby = (Ang_d * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                cal_robz = -(Ang_d * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용
                    # 개선에 대한 사선 형태 : TOP까지 : GES_Shift ~ 70%:약간 작게
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss - (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:    # a>b : 중심에 수직으로 세우는 형태로 수정 [13.07.24]
                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                        cal_roby = (Ang_d * 0.3) * math.cos(C_RadianL)
                        cal_robz = -(Ang_d * 0.3) * math.sin(C_RadianL)
                        cal_rx = -Calc_DegreeL + 30
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.7)      # 마지막은 b 방향으로 직선
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    # 종료 중간점[추가]
                    cal_robx = -(Ang_a) + PlasmaCutLoss
                    cal_roby = Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #=======================================================================================================

                    #시작 중간점[추가]
                    cal_robx = -(Ang_a) + PlasmaCutLoss
                    cal_roby = 0.0
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss - GES_Shift
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 1) / Calc_Cen)) + PlasmaCutLoss - GES_Shift
                    
                    cal_roby = -(Ang_T * 1) * math.cos(C_RadianH) - (GES_Adjust * math.sin(C_RadianH))  # ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianH) + (GES_Adjust * math.cos(C_RadianH))  # ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                    cal_rx = Calc_DegreeH
                    cal_ry = GES_Angle       #40도~>30도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #cal_robx = -(Ang_b) + PlasmaCutLoss
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_S) + PlasmaCutLoss - GES_Shift
                    else:
                        cal_robx = -(Ang_b) + PlasmaCutLoss - GES_Shift
                    
                    cal_roby = -(Ang_S) * math.cos(C_RadianH) - (GES_Adjust * math.sin(C_RadianH)) - 1
                    cal_robz = -(Ang_S) * math.sin(C_RadianH) + (GES_Adjust * math.cos(C_RadianH)) - 1
                    cal_rx = Calc_DegreeH
                    cal_ry = GES_Angle
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)


                    # 복귀 이동 중간점(1) ~ cal_robx = -GRobotLen + 20     # X+20위치
                    if (Ang_a <= Ang_b):
                        cal_robx = -Ang_b + 20
                    else:
                        cal_robx = -Ang_a + 20

                    cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:

                    # 확장형 상수d 적용
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_d * 0.3) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_d * 0.3) * math.cos(C_RadianL)
                    cal_robz = -(Ang_d * 0.3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 30
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 중심' 확장형 상수d 적용 ( + EDGE_M_Adj 보정) : 좌 수정 + ~> - [13.11.04~>07]:NO ~> +
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss + EDGE_M_Adj
                    else:
                        cal_robx = -((Ang_a) + (Ang_d / Calc_Cen)) + PlasmaCutLoss + EDGE_M_Adj - ((Ang_a - Ang_b) * 0.08)
                    
                    cal_roby = 0.0
                    cal_robz = 0.0
                    cal_rx = -Calc_DegreeL + 45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 0.3) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = -(Ang_T * 0.3) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 30
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 0.7) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = -(Ang_T * 0.7) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 15
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):        # Ang_T * 1.2 => * 1 수정 [2019.07.25]
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 1) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = -(Ang_T * 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # cal_robx = -(Ang_b) + PlasmaCutLoss          'T 만큼
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_S) + PlasmaCutLoss
                    else:
                        cal_robx = -(Ang_b) + PlasmaCutLoss
                    
                    cal_roby = -(Ang_S) * math.cos(C_RadianH) - 1
                    cal_robz = -(Ang_S) * math.sin(C_RadianH) - 1
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)


                    # 복귀 이동 중간점(1)
                    cal_robx = -(Ang_b) + PlasmaCutLoss + 20     # X+20위치
                    cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

            elif c_code == "004":       # 좌 C절단
                JOB_NO = "4004 "
                Pos_Num = 8

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_a) + PlasmaCutLoss
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Ang_a) + PlasmaCutLoss
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # Ang_c>0 : 입력에서 막는다.
                cal_robx = -(Ang_c - (Ang_T2) / ((Ang_S - Ang_b) / (Ang_c))) + PlasmaCutLoss   # tan각도=((Ang_S - Ang_B) / (Ang_C))
                cal_roby = -(Ang_T2) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = (Ang_T) * math.cos(C_RadianL)
                cal_robz = -(Ang_T) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 1           # 최종 절단은 좀더 아래로
                cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1          # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_c) + PlasmaCutLoss + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 중간 가공 : 상 ------------------------------------------------------------
            elif c_code == "011":       # 원(Hole)
                JOB_NO = "4011 "
                Pos_Num = 13        # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...) <== 6T 이하는 일반 절단 손실 적용
                if Ang_T > 6 and Ang_a <= 12:                
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                Cir_R = 0.0     #반지름
                Calc_Deg_A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]
                Calc_Deg_B = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]

                #Cen_X = -Ang_a / 2:     Cen_Y = -(Ang_S - Ang_b)
                Cir_R = (Ang_a / 2 - PlasmaCutLoss)
                Calc_Deg_A[2] = Cir_R * math.sin(20 * round(math.pi / 180, 9))
                Calc_Deg_A[7] = Cir_R * math.sin(70 * round(math.pi / 180, 9))
                Calc_Deg_A[8] = Cir_R * math.sin(80 * round(math.pi / 180, 9))
                
                Calc_Deg_B[2] = Cir_R * math.cos(20 * round(math.pi / 180, 9))
                Calc_Deg_B[7] = Cir_R * math.cos(70 * round(math.pi / 180, 9))
                Calc_Deg_B[8] = Cir_R * math.cos(80 * round(math.pi / 180, 9))

                #피어싱 방향 상부
                
                # 시작 이동 중간점(0)
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y     # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z     # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Ang_a / 4
                cal_roby = -((Ang_S - Ang_b) - (Ang_a / 4)) * math.cos(C_RadianH)
                cal_robz = -((Ang_S - Ang_b) - (Ang_a / 4)) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                cal_robx = -Ang_a / 2 + Calc_Deg_A[8]
                cal_roby = -((Ang_S - Ang_b) + Calc_Deg_B[8]) * math.cos(C_RadianH)
                cal_robz = -((Ang_S - Ang_b) + Calc_Deg_B[8]) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Ang_a / 2 + Calc_Deg_B[7]
                cal_roby = -((Ang_S - Ang_b) - Calc_Deg_A[7]) * math.cos(C_RadianH)
                cal_robz = -((Ang_S - Ang_b) - Calc_Deg_A[7]) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : L
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 0.5) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 0.5) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 원래값에서 아래로 3mm->2mm
                cal_robx = -Ang_a / 2 - Calc_Deg_A[2]
                cal_roby = -((Ang_S - Ang_b) - Calc_Deg_B[2] + 2) * math.cos(C_RadianH) - 0.5
                cal_robz = -((Ang_S - Ang_b) - Calc_Deg_B[2] + 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                # 'cal_robx = -Ang_a / 2 - 1
                # 'cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.cos(C_RadianH) - 1
                # 'cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.sin(C_RadianH)
                #============================
                cal_robx = -Ang_a * 0.75
                cal_roby = -((Ang_S - Ang_b) - (Ang_a / 4)) * math.cos(C_RadianH)
                cal_robz = -((Ang_S - Ang_b) - (Ang_a / 4)) * math.sin(C_RadianH)
                #============================
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "013":       # 평 타원
                JOB_NO = "4013 "
                Pos_Num = 13

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...) <== 6T 이하는 일반 절단 손실 적용
                if Ang_T > 6 and Ang_a <= 12:                
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y        # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z        # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Ang_a / 2) + Ang_c)
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + Ang_c) + PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Ang_a / 2) + Ang_c)
                cal_roby = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                cal_robx = -(Ang_a + Ang_c) / 2 - 1
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "014":       # 직 타원
                JOB_NO = "4014 "
                Pos_Num = 13

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...) <== 6T 이하는 일반 절단 손실 적용
                if Ang_T > 6 and Ang_a <= 12:                
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점(0)
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y        # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z        # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b - Ang_c / 2) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - Ang_c / 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b - (Ang_a + Ang_c) / 2 + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - (Ang_a + Ang_c) / 2 + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b - Ang_c / 2) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - Ang_c / 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b + Ang_c / 2) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + Ang_c / 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = -(Ang_S - Ang_b + (Ang_a + Ang_c) / 2 - PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + (Ang_a + Ang_c) / 2 - PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b + Ang_c / 2) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b + Ang_c / 2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                cal_robx = -PlasmaCutLoss - 2
                cal_roby = -(Ang_S - Ang_b - 1) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - 1) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -PlasmaCutLoss
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "015":       # V 컷팅
                JOB_NO = "4015 "
                Pos_Num = 6
                
                # V 컷팅 상부(두께) 비율(GVCutTAdj:1) : V_Thinkness = GVCutTAdj + IIf(Ang_T2 >= 9, 0.15, 0.21)      
                if(Ang_T2 >= 9):
                    V_Thinkness = GVCutTAdj + 0.15
                else:
                    V_Thinkness = GVCutTAdj + 0.21

                # 거리 상수b값 재 계산
                Ang_b = float((Ang_S - (Ang_T2 * V_Thinkness)) * (math.tan(Ang_a / 2 * round(math.pi / 180, 9))))
                VCutGapAdjust = (Ang_T * 0.12) + (GVCutGapAdj / 2)       # V Cut 내부 간격(GAP) : T에대한 비율값(상수b에 포함한) + 보정값 ~ 기본2mm+보정0mm

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_b + VCutGapAdjust) * 2
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
            

                #작업포인트
                if GV_Remain:   # 가공길이 - V 컷팅 영역 끝 < 배출 핸드 끝단

                    # 시작점 (5mm 남기기:피어싱)
                    cal_robx = -(Ang_b + VCutGapAdjust) * 2 + (5 * math.tan(Ang_a / 2 * round(math.pi / 180, 9)))
                    cal_roby = -(Ang_S - 5) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - 5) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_b + VCutGapAdjust * 2)
                    cal_roby = -(Ang_T2 * V_Thinkness) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T2 * V_Thinkness) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 겹치는 위 수평 부분
                    cal_robx = -(Ang_b)
                    cal_roby = -(Ang_T2 * V_Thinkness) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T2 * V_Thinkness) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # (3mm 남기기:피어싱)
                    cal_robx = -(3 * math.tan(Ang_a / 2 * round(math.pi / 180, 9)))
                    cal_roby = -(Ang_S - 3) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - 3) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:    # 기존의 일반 V 컷팅

                    # 시작점
                    cal_robx = -(Ang_b + VCutGapAdjust) * 2
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_b + VCutGapAdjust * 2)
                    cal_roby = -(Ang_T2 * V_Thinkness) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T2 * V_Thinkness) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 겹치는 위 수평 부분
                    cal_robx = -(Ang_b)
                    cal_roby = -(Ang_T2 * V_Thinkness) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T2 * V_Thinkness) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_b + VCutGapAdjust) * 2 + 20        # X+20위치
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "016":       # ㄷ 컷팅
                JOB_NO = "4016 "
                # Pos_Num ~ 아래에서 정의            

                # 시작 이동 중간점(0)
                cal_robx = -((Ang_a) - PlasmaCutLoss)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -((Ang_a) - PlasmaCutLoss)
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # ---------------------------------------------------------------------
                # 상수 d에 의한 가공 형태 구분
                # ---------------------------------------------------------------------
                if int(Ang_d) == 0 or int(Ang_d) == 1:
                    Pos_Num = 6         # 일반형(c=0), 측면 사선형

                    cal_robx = -((Ang_a - Ang_c) - PlasmaCutLoss)
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -Ang_c - PlasmaCutLoss
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -PlasmaCutLoss
                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                elif int(Ang_d) == 2 or int(Ang_d) == 3:
                    Pos_Num = 8         # 상부 반원(b=0), 일반 + 상부 반원

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R1
                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = -((Ang_S - Ang_b - Ang_c) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b - Ang_c) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R2
                    cal_robx = -(Ang_a / 2)
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R3
                    cal_robx = -PlasmaCutLoss
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # R3 종료점 : 중복 Point 제거

                    cal_robx = -PlasmaCutLoss
                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    Pos_Num = 10        #측면 원호(r)

                    V_Thinkness = (Ang_c - PlasmaCutLoss) / math.sqrt(2)      # 변수활용

                    #R1
                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R2
                    cal_robx = -(Ang_a - Ang_c + V_Thinkness)
                    cal_roby = -(Ang_S - V_Thinkness) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - V_Thinkness) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R3
                    cal_robx = -((Ang_a - Ang_c) - PlasmaCutLoss)
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # R3 종료점 : 중복 Point 제거

                    # 수평 직선
                    cal_robx = -Ang_c - PlasmaCutLoss
                    cal_roby = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # R1 :중복 Point 제거

                    #R2
                    cal_robx = -Ang_c + V_Thinkness
                    cal_roby = -((Ang_S - V_Thinkness) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -((Ang_S - V_Thinkness) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #R3
                    cal_robx = -PlasmaCutLoss
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # R3 종료점 : 중복 Point 제거

                    cal_robx = -PlasmaCutLoss - 1
                    cal_roby = -(Ang_S + 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S + 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # ---------------------------------------------------------------------

                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a) - PlasmaCutLoss) + 20        # X+20위치
                cal_roby = -(Ang_S + 1) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 우 가공 : 상 --------------------------------------------------------------
            elif c_code == "021":       # 우 스닙
                JOB_NO = "4001 "
                Pos_Num = 4

                # 시작 이동 중간점(0)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 시작점
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + SNIP_Adj)
                cal_roby = -(Ang_S - (Ang_b + SNIP_Adj) + PlasmaCutLoss) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - (Ang_b + SNIP_Adj) + PlasmaCutLoss) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_S - (Ang_b + 1) + PlasmaCutLoss) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                
            elif c_code == "022":       # 우 각모
                JOB_NO = "4002 "
                Pos_Num = 6

                # 시작 이동 중간점(0)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Ang_c == 0: 
                    Ang_c = Ang_b 
                    Ang_d = 0

                if Ang_d >= 500:     # 사선형 각모
                    Ang_d = Ang_d - 500

                    # 시작점
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_d)
                    cal_roby = -(Ang_S - (Ang_c) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - (Ang_c) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a)          #- PlasmaCutLoss       '(Ang_a + 1)를 조금 작게 - 다음 앵글에 흔적이 남는다.
                    cal_roby = -(Ang_S - (Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - (Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:

                    # 시작점
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_roby = -(Ang_S - (Ang_c) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - (Ang_c) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a - Ang_d)         #- PlasmaCutLoss       '(Ang_a + 1)를 조금 작게 - 다음 앵글에 흔적이 남는다.
                    cal_roby = -(Ang_S - (Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - (Ang_b) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a)          #- PlasmaCutLoss       '(Ang_a + 1)를 조금 작게 - 다음 앵글에 흔적이 남는다.
                    cal_roby = -(Ang_S - (Ang_b + Ang_d) + PlasmaCutLoss) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S - (Ang_b + Ang_d) + PlasmaCutLoss) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                
                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_S - (Ang_b) + PlasmaCutLoss) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
            
            elif c_code == "023":       # 우 사각귀
                JOB_NO = "4003 "
                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30]
                    if Ang_a > Ang_b:       #중심에 수직으로 세우는 형태로 수정 : 2P 추가 [13.07.24]
                        Pos_Num = 12
                    else:
                        Pos_Num = 10
                else:
                    Pos_Num = 11

                # 사각귀 안쪽 1mm 작게(+1mm) 추가 [08.10.21]
                Ang_a = Ang_a + 1 
                Ang_b = Ang_b + 1
                #+++++++++++++++++++++++++++++++++++++++++++
                # 사각귀 안쪽 스닙 부분 조금 더 작게 [08.10.21]
                # (비율 0.7 => 0.6)   ' 안 스닙 더 작게
                #+++++++++++++++++++++++++++++++++++++++++++

                if (Ang_b - Ang_a) == 0:
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Ang_S + Ang_T) / (Ang_b - Ang_a)

                # 민사각귀 구분 및 오류 방지
                if Ang_d > 100:
                    DirectEdge = True
                    Ang_d = float(A_Code[5])        #float(A_Code[13:15])
                else:
                    DirectEdge = False
                    if Ang_d == 0: 
                        Ang_d = Ang_c     # 이전 자료 보완 # Ang_d = Ang_d


                # 시작 이동 중간점(0)
                cal_robx = -(Ang_Lenth - Ang_b)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용

                    #=======================================================================================================
                    #=======================================================================================================

                    # 시작점
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_Lenth - (Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_S)) + GES_Shift
                    else:
                        cal_robx = -(Ang_Lenth - Ang_b) + GES_Shift
                    
                    cal_roby = -(Ang_S) * math.cos(C_RadianH) - (GES_Adjust * math.sin(C_RadianH))
                    cal_robz = -(Ang_S) * math.sin(C_RadianH) + (GES_Adjust * math.cos(C_RadianH))
                    cal_rx = Calc_DegreeH
                    cal_ry = -GES_Angle      #40도(-)
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + GES_Shift
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 1) / Calc_Cen) + GES_Shift
                    
                    cal_roby = -(Ang_T * 1) * math.cos(C_RadianH) - (GES_Adjust * math.sin(C_RadianH))
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianH) + (GES_Adjust * math.cos(C_RadianH))
                    cal_rx = Calc_DegreeH
                    cal_ry = -GES_Angle      #40도(-)
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #종료 중간점[추가]
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.7) / Calc_Cen)
                    
                    cal_roby = 0.0
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #시작 중간점[추가]
                    cal_robx = -(Ang_Lenth - Ang_a)
                    cal_roby = Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #개선에 대한 사선 형태 : TOP까지 : GES_Shift ~ 70%:약간 작게
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:    #a>b : 중심에 수직으로 세우는 형태로 수정 [13.07.24]

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL + 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                        cal_roby = (Ang_d * 0.3 + GEdgeAdd) * math.cos(C_RadianL)
                        cal_robz = -(Ang_d * 0.3 + GEdgeAdd) * math.sin(C_RadianL)
                        cal_rx = -Calc_DegreeL + 30
                        cal_ry = 0.0
                        cal_rz = 0.0
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    #=======================================================================================================
                    #=======================================================================================================

                else:

                    # 시작점
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_Lenth - (Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_S))
                    else:
                        cal_robx = -(Ang_Lenth - Ang_b)
                    
                    cal_roby = -(Ang_S) * math.cos(C_RadianH)
                    cal_robz = -(Ang_S) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 1) / Calc_Cen)
                    
                    cal_roby = -(Ang_T * 1) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.7) / Calc_Cen)

                    cal_roby = -(Ang_T * 0.7) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 15
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.3) / Calc_Cen) + EDGE_M_Adj
                    
                    cal_roby = -(Ang_T * 0.3) * math.cos(C_RadianH)
                    cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 30
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 중심' 확장형 상수d 적용 ( + EDGE_M_Adj 보정)
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        ## cal_robx = -((Ang_Lenth - Ang_a) + (Ang_d / Calc_Cen)) + EDGE_M_Adj - ((Ang_a - Ang_b) * 0.08)
                        cal_robx = -((Ang_Lenth - Ang_a) + (Ang_T / Calc_Cen)) + EDGE_M_Adj - ((Ang_a - Ang_b) * 0.08)

                    cal_roby = 0.0
                    cal_robz = 0.0
                    cal_rx = Calc_DegreeH - 45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 확장형 상수d 적용    '( + EDGE_M_Adj 보정) 추가 [14.01.16]
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_d * 0.3) / Calc_Cen) + EDGE_M_Adj
                    
                    cal_roby = (Ang_d * 0.3) * math.cos(C_RadianL)
                    cal_robz = -(Ang_d * 0.3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 30
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 확장형 상수d 적용
                cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                cal_roby = (Ang_d * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                cal_robz = -(Ang_d * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if DirectEdge:      # 민사각귀
                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                else:
                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a) + (Ang_c * (0.6 + EDGE_C_Rate))
                    cal_roby = (Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)
                    cal_roby = (Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.cos(C_RadianL)
                    cal_robz = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)            
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a) + 20     # X+20위치
                cal_roby = (Ang_c + Ang_c * 0.9) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "024":       # 우 C절단
                JOB_NO = "4004 "
                Pos_Num = 8

                if Ang_a <= Ang_c:
                    Calc_Cen = Ang_c
                else:
                    Calc_Cen = Ang_a
                
                # 시작 이동 중간점(0)
                cal_robx = -(Calc_Cen - Ang_a)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Calc_Cen - Ang_a)
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Calc_Cen
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # Ang_c>0 : 입력에서 막는다.
                cal_robx = -((Calc_Cen - Ang_c) + (Ang_T2) / ((Ang_S - Ang_b) / (Ang_c)))
                cal_roby = -(Ang_T2) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = (Ang_T) * math.cos(C_RadianL)
                cal_robz = -(Ang_T) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 1          # 최종 절단은 좀더 아래로
                cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1         # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Calc_Cen - Ang_c) + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 2 + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            # 선1,2,3,4 : 상 ------------------------------------------------------------

            elif c_code == "031":       # 선1 상
                JOB_NO = "4031 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y        # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z        # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "032":       # 선2 상
                JOB_NO = "4032 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y       # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z       # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b - Ang_a) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - Ang_a) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = 20        # X+20위치
                cal_roby = -(Ang_S - Ang_b - Ang_a) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "033":       # 선3 상
                JOB_NO = "4033 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b - Ang_c) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b - Ang_c) * math.cos(C_RadianH) - PlasmaP_H_Y       # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b - Ang_c) * math.sin(C_RadianH) + PlasmaP_H_Z       # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b - Ang_c) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - Ang_c) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "034":       # 선4 상
                JOB_NO = "4034 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH) - PlasmaP_H_Y        # 피어싱 띄우기
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH) + PlasmaP_H_Z        # 피어싱 띄우기
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -(Ang_S - Ang_b) * math.cos(C_RadianH)
                ##cal_robz = -(Ang_S - Ang_b - Ang_c) * math.sin(C_RadianH)
                cal_robz = -(Ang_S - Ang_b) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = -(Ang_S - Ang_b - Ang_c) * math.cos(C_RadianH)
                cal_robz = -(Ang_S - Ang_b - Ang_c) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_S - Ang_b - Ang_c) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
            


            # ===========================================================================
            # 하부 가공
            # ===========================================================================

            # 좌 가공 : 하 --------------------------------------------------------------
            elif c_code == "101":       # 좌 스닙
                JOB_NO = "4001 "
                Pos_Num = 4

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = SNIP_Adj
                cal_roby = ((Ang_L - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Ang_a + 1) - PlasmaCutLoss)
                cal_roby = (Ang_L + 1) * math.cos(C_RadianL)
                cal_robz = -(Ang_L + 1) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a + 1) - PlasmaCutLoss) + 20     # X+20위치
                cal_roby = (Ang_L + 1) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "102":       # 좌 각모
                JOB_NO = "4002 "
                Pos_Num = 6

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Ang_c == 0: 
                    Ang_c = Ang_b 
                    Ang_d = 0

                if Ang_d >= 500:     # 사선형 각모
                    Ang_d = Ang_d - 500

                    # 시작점
                    cal_robx = 0.0
                    cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a - Ang_d) - PlasmaCutLoss)
                    cal_roby = ((Ang_L - Ang_c) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - Ang_c) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = (Ang_L + 1) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L + 1) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                else:

                    # 시작점
                    cal_robx = 0.0
                    cal_roby = ((Ang_L - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_d) - PlasmaCutLoss)
                    cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = ((Ang_L - Ang_c) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - Ang_c) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Ang_a) - PlasmaCutLoss)
                    cal_roby = (Ang_L + 1) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L + 1) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a) - PlasmaCutLoss) + 20     # X+20위치
                cal_roby = (Ang_L + 1) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)           
                pose_Arr.append(cal_pose)

            elif c_code == "103":       # 좌 사각귀
                JOB_NO = "4003 "
                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30]
                    if Ang_a > Ang_b:       #중심에 수직으로 세우는 형태로 수정 : 2P 추가 [13.07.24]
                        Pos_Num = 12
                    else:
                        Pos_Num = 10
                else:
                    Pos_Num = 11

                # 사각귀 안쪽 1mm 작게(+1mm) 추가 [08.10.21]
                Ang_a = Ang_a + 1 
                Ang_b = Ang_b + 1

                if (Ang_b - Ang_a) == 0:
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Ang_L + Ang_T) / (Ang_b - Ang_a)

                # 민사각귀 구분 및 오류 방지
                if Ang_d > 100:
                    DirectEdge = True
                    Ang_d = float(A_Code[5])        #float(A_Code[13:15])
                else:
                    DirectEdge = False
                    if Ang_d == 0: 
                        Ang_d = Ang_c     # 이전 자료 보완 # Ang_d = Ang_d

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = -(Ang_c + Ang_c * 0.7) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if DirectEdge:      # 민사각귀
                    # 시작점
                    cal_robx = 0.0
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                else:
                    # 시작점
                    cal_robx = 0.0
                    cal_roby = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_c * (0.6 + EDGE_C_Rate))
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # 확장형 상수d 적용
                cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                cal_roby = -(Ang_d * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                cal_robz = -(Ang_d * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - EDGE_IN_Degree
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용
                    #개선에 대한 사선 형태 : TOP까지 : GES_Shift ~ 70%:약간 작게
                    if (Ang_a <= Ang_b):        #

                        cal_robx = -(Ang_a) + PlasmaCutLoss - (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - EDGE_IN_Degree
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:    #a>b : 중심에 수직으로 세우는 형태로 수정 [13.07.24]

                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                        cal_roby = -(Ang_d * 0.3 + GEdgeAdd) * math.cos(C_RadianH)
                        cal_robz = -(Ang_d * 0.3 + GEdgeAdd) * math.sin(C_RadianH)
                        cal_rx = Calc_DegreeH - 30      #15
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.3)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_a) + PlasmaCutLoss + (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    #종료 중간점[추가]
                    cal_robx = -(Ang_a) + PlasmaCutLoss
                    cal_roby = -Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    #=======================================================================================================

                    #시작 중간점[추가]
                    cal_robx = -(Ang_a) + PlasmaCutLoss
                    cal_roby = 0.0
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    ##NO #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):    #Ang_T * 1.2 => * 1 수정 [2019.07.25]
                        cal_robx = -(Ang_a) + PlasmaCutLoss - GES_Shift
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 1) / Calc_Cen)) + PlasmaCutLoss - GES_Shift   # ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                    
                    cal_roby = (Ang_T * 1) * math.cos(C_RadianL) + (GES_Adjust * math.sin(C_RadianL))
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianL) + (GES_Adjust * math.cos(C_RadianL))
                    cal_rx = -Calc_DegreeL
                    cal_ry = GES_Angle       #40도
                    ##NO #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_L) + PlasmaCutLoss - GES_Shift
                    else:
                        cal_robx = -(Ang_b) + PlasmaCutLoss - GES_Shift
                    
                    cal_roby = (Ang_L) * math.cos(C_RadianL) + (GES_Adjust * math.sin(C_RadianL)) + 1         # 최종 절단은 좀더 아래로
                    cal_robz = -(Ang_L) * math.sin(C_RadianL) + (GES_Adjust * math.cos(C_RadianL)) - 1        # 최종 절단은 좀더 아래로
                    cal_rx = -Calc_DegreeL
                    cal_ry = GES_Angle       #40도
                    ##NO #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점(1) ~ cal_robx = -GRobotLen + 20     # X+20위치
                    if (Ang_a <= Ang_b):
                        cal_robx = -Ang_b + 20
                    else:
                        cal_robx = -Ang_a + 20

                    cal_roby = (Ang_L) * math.cos(C_RadianL) + 2 + Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

                else:

                    # 확장형 상수d 적용
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_d * 0.3) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = -(Ang_d * 0.3) * math.cos(C_RadianH)
                    cal_robz = -(Ang_d * 0.3) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 30      #15     # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 중심# 확장형 상수d 적용 ( + EDGE_M_Adj 보정) : 좌 수정 + ~> - [13.11.04~>07]:NO ~> +
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss + EDGE_M_Adj
                    else:
                        cal_robx = -((Ang_a) + (Ang_d / Calc_Cen)) + PlasmaCutLoss + EDGE_M_Adj - ((Ang_a - Ang_b) * 0.08)
                    
                    cal_roby = 0.0
                    cal_robz = 0.0
                    cal_rx = Calc_DegreeH - 45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 0.3) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.3) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 30
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 0.7) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.7) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 15
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_a) + PlasmaCutLoss
                    else:
                        cal_robx = -((Ang_a) + ((Ang_T * 1) / Calc_Cen)) + PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 1) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_L) + PlasmaCutLoss    
                    else:
                        cal_robx = -(Ang_b) + PlasmaCutLoss
                    
                    cal_roby = (Ang_L) * math.cos(C_RadianL) + 1         # 최종 절단은 좀더 아래로
                    cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1        # 최종 절단은 좀더 아래로
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점(1)
                    cal_robx = -(Ang_b) + PlasmaCutLoss + 20     # X+20위치
                    cal_roby = (Ang_L) * math.cos(C_RadianL) + 2 + Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                    pose_Arr.append(cal_pose)

            elif c_code == "104":       # 좌 C절단
                JOB_NO = "4004 "
                Pos_Num = 8

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = -(Ang_T2) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -(Ang_c) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # Ang_c>0 : 입력에서 막는다.
                cal_robx = -(Ang_c - (Ang_T) / ((Ang_L - Ang_b) / (Ang_c))) + PlasmaCutLoss
                cal_roby = (Ang_T) * math.cos(C_RadianL)
                cal_robz = -(Ang_T) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a) + PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 1           # 최종 절단은 좀더 아래로
                cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1          # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + PlasmaCutLoss + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 2 + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)


            # 중간 가공 : 하 ------------------------------------------------------------
            elif c_code == "111":       # 원(Hole)
                JOB_NO = "4011 "
                Pos_Num = 13

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...) <== 6T 이하는 일반 절단 손실 적용
                if Ang_T > 6 and Ang_a <= 12:
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                Cir_R = 0.0     #반지름
                Calc_Deg_A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]
                Calc_Deg_B = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]

                #Cen_X = -Ang_a / 2:     Cen_Y = -(Ang_S - Ang_b)
                Cir_R = (Ang_a / 2 - PlasmaCutLoss)
                Calc_Deg_A[2] = Cir_R * math.sin(20 * round(math.pi / 180, 9))
                Calc_Deg_A[7] = Cir_R * math.sin(70 * round(math.pi / 180, 9))
                Calc_Deg_A[8] = Cir_R * math.sin(80 * round(math.pi / 180, 9))

                Calc_Deg_B[2] = Cir_R * math.cos(20 * round(math.pi / 180, 9))
                Calc_Deg_B[7] = Cir_R * math.cos(70 * round(math.pi / 180, 9))
                Calc_Deg_B[8] = Cir_R * math.cos(80 * round(math.pi / 180, 9))

                #피어싱 방향 상부

                # 시작 이동 중간점(0)
                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y        # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z       # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Ang_a * 0.75
                cal_roby = ((Ang_L - Ang_b) - (Ang_a / 4)) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) - (Ang_a / 4)) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                
                cal_robx = -Ang_a / 2
                cal_roby = ((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                cal_robx = -PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                cal_robx = -Ang_a / 2 - Calc_Deg_A[8]
                cal_roby = ((Ang_L - Ang_b) + Calc_Deg_B[8]) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) + Calc_Deg_B[8]) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Ang_a / 2 - Calc_Deg_B[7]
                cal_roby = ((Ang_L - Ang_b) - Calc_Deg_A[7]) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) - Calc_Deg_A[7]) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : L
                cal_robx = -Ang_a / 2
                cal_roby = ((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss + 0.5) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss + 0.5) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Ang_a / 2 + Calc_Deg_A[2]
                cal_roby = ((Ang_L - Ang_b) - Calc_Deg_B[2] + 2) * math.cos(C_RadianL) + 0.5
                cal_robz = -((Ang_L - Ang_b) - Calc_Deg_B[2] + 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                #cal_robx = -Ang_a / 2 + 1
                #cal_roby = ((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss + 2) * math.cos(C_RadianL) + 1
                #cal_robz = -((Ang_L - Ang_b) - (Ang_a / 2) + PlasmaCutLoss + 2) * math.sin(C_RadianL)
                #============================
                cal_robx = -Ang_a / 4
                cal_roby = ((Ang_L - Ang_b) - (Ang_a / 4)) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) - (Ang_a / 4)) * math.sin(C_RadianL)
                #============================
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "113":       # 평 타원
                JOB_NO = "4013 "
                Pos_Num = 13

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Ang_T2 > 6 and Ang_a <= 12:
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y          # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z         # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -((Ang_a / 2) + Ang_c)
                cal_roby = (Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + (Ang_a / 2) - PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -(Ang_a + Ang_c) + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Ang_a / 2) + Ang_c)
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                # 리턴 (4, )
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                cal_robx = -(Ang_a + Ang_c) / 2 + 1
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss + 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a + Ang_c) / 2
                cal_roby = (Ang_L - Ang_b - (Ang_a / 2) + PlasmaCutLoss) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "114":       # 직 타원
                JOB_NO = "4014 "
                Pos_Num = 13

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Ang_T2 > 6 and Ang_a <= 12:
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점(0)
                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y         # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z        # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b - Ang_c / 2) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - Ang_c / 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b - (Ang_a + Ang_c) / 2 + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - (Ang_a + Ang_c) / 2 + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b - Ang_c / 2) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - Ang_c / 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b + Ang_c / 2) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + Ang_c / 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                cal_robx = -Ang_a / 2
                cal_roby = (Ang_L - Ang_b + (Ang_a + Ang_c) / 2 - PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + (Ang_a + Ang_c) / 2 - PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b + Ang_c / 2) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b + Ang_c / 2) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거

                # 리턴 (4, )
                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                cal_robx = -Ang_a + PlasmaCutLoss + 2
                cal_roby = (Ang_L - Ang_b - 1) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - 1) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -Ang_a + PlasmaCutLoss
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "115":       # V 타원
                JOB_NO = "4015 "
                Pos_Num = 6

                # V 컷팅 상부(두께) 비율(GVCutTAdj:1) : V_Thinkness = GVCutTAdj + IIf(Ang_T >= 9, 0.15, 0.21)      
                if(Ang_T >= 9):
                    V_Thinkness = GVCutTAdj + 0.15
                else:
                    V_Thinkness = GVCutTAdj + 0.21

                # 거리 상수b값 재 계산
                Ang_b = float((Ang_L - (Ang_T * V_Thinkness)) * (math.tan(Ang_a / 2 * round(math.pi / 180, 9))))
                VCutGapAdjust = (Ang_T2 * 0.12) + (GVCutGapAdj / 2)       # V Cut 내부 간격(GAP) : T에대한 비율값(상수b에 포함한) + 보정값 ~ 기본2mm+보정0mm

                # 시작 이동 중간점(0)
                cal_robx = -(Ang_b + VCutGapAdjust) * 2 
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if GV_Remain:
                    # 시작점 (5mm 남기기:피어싱)
                    cal_robx = -(Ang_b + VCutGapAdjust) * 2 + (5 * math.tan(Ang_a / 2 * round(math.pi / 180, 9)))
                    cal_roby = (Ang_L - 5) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L - 5) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_b + VCutGapAdjust * 2)
                    cal_roby = (Ang_T * V_Thinkness) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * V_Thinkness) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 겹치는 위 수평 부분
                    cal_robx = -(Ang_b) 
                    cal_roby = (Ang_T * V_Thinkness) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * V_Thinkness) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # (3mm 남기기:피어싱)
                    cal_robx = -(3 * math.tan(Ang_a / 2 * round(math.pi / 180, 9)))
                    cal_roby = (Ang_L - 3) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L - 3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    # 시작점
                    cal_robx = -(Ang_b + VCutGapAdjust) * 2 
                    cal_roby = (Ang_L) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_b + VCutGapAdjust * 2)
                    cal_roby = (Ang_T * V_Thinkness) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * V_Thinkness) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 겹치는 위 수평 부분
                    cal_robx = -(Ang_b) 
                    cal_roby = (Ang_T * V_Thinkness) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * V_Thinkness) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = (Ang_L + 1) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L + 1) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_b + VCutGapAdjust) * 2 + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "116":       # ㄷ 타원
                JOB_NO = "4016 "
                Pos_Num = 6

                # 시작 이동 중간점(0)
                cal_robx = -((Ang_a) - PlasmaCutLoss)
                cal_roby = (Ang_L + 1) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -((Ang_a) - PlasmaCutLoss)
                cal_roby = (Ang_L + 1) * math.cos(C_RadianL)
                cal_robz = -(Ang_L + 1) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # ---------------------------------------------------------------------
                # 상수 d에 의한 가공 형태 구분 ~ 없음!!
                # ---------------------------------------------------------------------
                # if int(Ang_d) == 0 or int(Ang_d) == 1:

                cal_robx = -((Ang_a) - PlasmaCutLoss)
                cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = ((Ang_L - Ang_b) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - Ang_b) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Ang_L) * math.cos(C_RadianL)
                cal_robz = -(Ang_L) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -((Ang_a) - PlasmaCutLoss) + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)


            # 우 가공 : 하 --------------------------------------------------------------
            elif c_code == "121":       # 우 스닙
                JOB_NO = "4001 "
                Pos_Num = 4

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = (Ang_L) * math.cos(C_RadianL)
                cal_robz = -(Ang_L) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a + SNIP_Adj)       #0.4 보정 [11.03.15]    #- PlasmaCutLoss      #(Ang_a + 1)를 조금 작게 - 다음 앵글에 흔적이 남는다.
                cal_roby = ((Ang_L - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.cos(C_RadianL)
                cal_robz = -((Ang_L - (Ang_b + SNIP_Adj)) + PlasmaCutLoss) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = ((Ang_L - (Ang_b + 1)) + PlasmaCutLoss) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # 앵글 마지막 피스 수직 절단 보상용
                if GWorkEnd: GE_CutLast = (Ang_b) - PlasmaCutLoss
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++

            elif c_code == "122":       # 우 각모
                JOB_NO = "4002 "
                Pos_Num = 6

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Ang_c == 0: 
                    Ang_c = Ang_b
                    Ang_d = 0

                if Ang_d >= 500:     # 사선형 각모
                    Ang_d = Ang_d - 500

                    # 시작점
                    cal_robx = 0.0
                    cal_roby = (Ang_L) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = (Ang_L) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_d)
                    cal_roby = ((Ang_L - (Ang_c)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_c)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a)
                    cal_roby = ((Ang_L - (Ang_b)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_b)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 앵글 마지막 피스 수직 절단 보상용
                    if GWorkEnd: GE_CutLast = (Ang_b) - PlasmaCutLoss
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

                else:

                    # 시작점
                    cal_robx = 0.0
                    cal_roby = (Ang_L) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = ((Ang_L - (Ang_c)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_c)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a - Ang_d)
                    cal_roby = ((Ang_L - (Ang_b)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_b)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_a)
                    cal_roby = ((Ang_L - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.cos(C_RadianL)
                    cal_robz = -((Ang_L - (Ang_b + Ang_d)) + PlasmaCutLoss) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 앵글 마지막 피스 수직 절단 보상용
                    if GWorkEnd: GE_CutLast = (Ang_b + Ang_d) - PlasmaCutLoss
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = ((Ang_L - (Ang_b)) + PlasmaCutLoss) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "123":       # 우 사각귀
                JOB_NO = "4003 "
                
                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30]
                    if Ang_a > Ang_b:       #중심에 수직으로 세우는 형태로 수정 : 2P 추가 [13.07.24]
                        Pos_Num = 12
                    else:
                        Pos_Num = 10
                else:
                    Pos_Num = 11

                # 사각귀 안쪽 1mm 작게(+1mm) 추가 [08.10.21]
                Ang_a = Ang_a + 1 
                Ang_b = Ang_b + 1

                if Ang_b - Ang_a == 0:
                    Calc_Cen = 0
                else:
                    ##Calc_Cen = (Ang_L + Ang_c) / (Ang_b - Ang_a)    # tan 각도
                    Calc_Cen = (Ang_L + Ang_T) / (Ang_b - Ang_a)    # tan 각도 ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                
                if Ang_b <= Ang_a:
                    Ang_Lenth = Ang_a
                else:
                    Ang_Lenth = Ang_b

                # 민사각귀 구분 및 오류 방지
                if Ang_d > 100:
                    DirectEdge = True
                    Ang_d = float(A_Code[5])        #float(A_Code[13:15])
                else:
                    DirectEdge = False
                    if Ang_d == 0: 
                        Ang_d = Ang_c     # 이전 자료 보완 # Ang_d = Ang_d
                
                # 시작 이동 중간점(0)
                cal_robx = -(Ang_Lenth - Ang_b)
                cal_roby = (Ang_L) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if GES_Use:     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용

                    #=======================================================================================================
                    #=======================================================================================================

                    # 시작점
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_Lenth - (Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_L)) + GES_Shift  # ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                    else:
                        cal_robx = -(Ang_Lenth - Ang_b) + GES_Shift
                    
                    cal_roby = (Ang_L) * math.cos(C_RadianL) + (GES_Adjust * math.sin(C_RadianL))
                    cal_robz = -(Ang_L) * math.sin(C_RadianL) + (GES_Adjust * math.cos(C_RadianL))
                    cal_rx = -Calc_DegreeL
                    cal_ry = -GES_Angle      #40도(-)
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + GES_Shift
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 1) / Calc_Cen) + GES_Shift
                    
                    cal_roby = (Ang_T * 1) * math.cos(C_RadianL) + (GES_Adjust * math.sin(C_RadianL))
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianL) + (GES_Adjust * math.cos(C_RadianL))
                    cal_rx = -Calc_DegreeL
                    cal_ry = -GES_Angle      #40도(-)
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #종료 중간점[추가]
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.7) / Calc_Cen)
                    
                    cal_roby = 0.0
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #시작 중간점[추가]
                    cal_robx = -(Ang_Lenth - Ang_a)
                    cal_roby = -Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #개선에 대한 사선 형태 : TOP까지 : GES_Shift ~ 70%:약간 작게
                    if (Ang_a <= Ang_b):

                        cal_robx = -(Ang_Lenth - Ang_a) + (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - EDGE_IN_Degree
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:    #a>b : 중심에 수직으로 세우는 형태로 수정 [13.07.24]

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.7)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                        cal_roby = 0.0
                        cal_robz = 0.0
                        cal_rx = Calc_DegreeH - 45
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                        cal_roby = -(Ang_d * 0.3 + GEdgeAdd) * math.cos(C_RadianH)
                        cal_robz = -(Ang_d * 0.3 + GEdgeAdd) * math.sin(C_RadianH)
                        cal_rx = Calc_DegreeH - 30
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    #=======================================================================================================
                    #=======================================================================================================

                else:
                    # 시작점
                    if (Ang_a < Ang_b):     # 각도를 위해
                        cal_robx = -(Ang_Lenth - (Ang_b - (Ang_b - Ang_a) * Ang_T / Ang_L))  # ~ 사선사각귀 Ang_c=>자재T 적용 [2019.07.25]
                    else:
                        cal_robx = -(Ang_Lenth - Ang_b)
                    
                    cal_roby = (Ang_L) * math.cos(C_RadianL)
                    cal_robz = -(Ang_L) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 수직으로 각도 변화 없는 행정 위해 추가
                    if (Ang_a <= Ang_b):    #Ang_T * 1.2 => * 1 수정 [2019.07.25]
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 1) / Calc_Cen)  #- PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 1) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 1) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a)
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.7) / Calc_Cen)  #- PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.7) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.7) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 15      #-30     # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if (Ang_a <= Ang_b):    #( + EDGE_M_Adj 보정) 추가 [14.01.16]
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_T * 0.3) / Calc_Cen) + EDGE_M_Adj    #- PlasmaCutLoss
                    
                    cal_roby = (Ang_T * 0.3) * math.cos(C_RadianL)
                    cal_robz = -(Ang_T * 0.3) * math.sin(C_RadianL)
                    cal_rx = -Calc_DegreeL + 30      #-15     # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 중심# 확장형 상수d 적용 ( + EDGE_M_Adj 보정)
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        cal_robx = -((Ang_Lenth - Ang_a) + (Ang_d / Calc_Cen)) + EDGE_M_Adj - ((Ang_a - Ang_b) * 0.08)
                    
                    cal_roby = 0.0
                    cal_robz = 0.0
                    cal_rx = -Calc_DegreeL + 45      #0       # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 확장형 상수d 적용    #( + EDGE_M_Adj 보정) 추가 [14.01.16]
                    if (Ang_a <= Ang_b):
                        cal_robx = -(Ang_Lenth - Ang_a) + EDGE_M_Adj
                    else:
                        cal_robx = -(Ang_Lenth - Ang_a) + ((Ang_d * 0.3) / Calc_Cen) + EDGE_M_Adj
                    
                    cal_roby = -(Ang_d * 0.3) * math.cos(C_RadianH)
                    cal_robz = -(Ang_d * 0.3) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - 30      #15     # 부등변을 위해 수정 [11.06.20]
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 확장형 상수d 적용
                cal_robx = -(Ang_Lenth - Ang_a) - (GES_Shift * 0.3)
                cal_roby = -(Ang_d * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                cal_robz = -(Ang_d * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH - EDGE_IN_Degree
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if DirectEdge:      # 민사각귀
                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)         #- PlasmaCutLoss       #T 만큼      #T 만큼
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)                      #T 만큼     #T 만큼
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 앵글 마지막 피스 수직 절단 보상용
                    if GWorkEnd: GE_CutLast = Ang_c * 0.8 + 999 #(우사각귀 하 구분용 임의의 값 999)
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

                else:

                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a) + (Ang_c * (0.6 + EDGE_C_Rate))      #(Ang_c * 0.6)         #- PlasmaCutLoss       #T 만큼      #T 만큼
                    cal_roby = -(Ang_c * 0.8 + GEdgeAdd) * math.cos(C_RadianH)
                    cal_robz = -(Ang_c * 0.8 + GEdgeAdd) * math.sin(C_RadianH)
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a)                      #T 만큼     #T 만큼
                    cal_roby = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.cos(C_RadianH)     # 안 스닙 더 작게
                    cal_robz = -(Ang_c + Ang_c * (0.8 + EDGE_C_Rate)) * math.sin(C_RadianH)     # 안 스닙 더 작게
                    cal_rx = Calc_DegreeH - EDGE_IN_Degree
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 앵글 마지막 피스 수직 절단 보상용
                    if GWorkEnd: GE_CutLast = Ang_c + Ang_c * 0.8 + 999 #(우사각귀 하 구분용 임의의 값 999)
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_Lenth - Ang_a) - (Ang_a) + 20     # X+20위치
                cal_roby = -(Ang_c + Ang_c * 0.9) * math.cos(C_RadianH) - Margin_Y       #Y-50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "124":       # 우 C절단
                JOB_NO = "4004 "
                Pos_Num = 8

                if Ang_a <= Ang_c:
                    Calc_Cen = Ang_c
                else:
                    Calc_Cen = Ang_a
                
                # 시작 이동 중간점(0)
                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = -(Ang_S) * math.cos(C_RadianH) - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = -(Ang_S) * math.cos(C_RadianH)
                cal_robz = -(Ang_S) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = -(Ang_T2) * math.cos(C_RadianH)
                cal_robz = -(Ang_T2) * math.sin(C_RadianH)
                cal_rx = Calc_DegreeH
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중심
                cal_robx = -(Calc_Cen - Ang_c)
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH - 45
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # Ang_c>0 : 입력에서 막는다.
                cal_robx = -((Calc_Cen - Ang_c) + (Ang_T) / ((Ang_L - Ang_b) / (Ang_c)))
                cal_roby = (Ang_T) * math.cos(C_RadianL)
                cal_robz = -(Ang_T) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Calc_Cen
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Calc_Cen - Ang_a)
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 1           # 최종 절단은 좀더 아래로
                cal_robz = -(Ang_L) * math.sin(C_RadianL) - 1          # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Calc_Cen - Ang_a) + 20     # X+20위치
                cal_roby = (Ang_L) * math.cos(C_RadianL) + 2 + Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            # 선1,2,3,4 : 하 ------------------------------------------------------------

            elif c_code == "131":       # 선1 하
                JOB_NO = "4031 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y         # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z        # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "132":       # 선2 하
                JOB_NO = "4032 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y        # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z       # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b - Ang_a) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - Ang_a) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = 20       # X+20위치
                cal_roby = (Ang_L - Ang_b - Ang_a) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                    
                pose_Arr.append(cal_pose)

            elif c_code == "133":       # 선3 하
                JOB_NO = "4033 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + PlasmaP_L_Y         # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL) + PlasmaP_L_Z        # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = (Ang_L - Ang_b - Ang_c) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - Ang_c) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = (Ang_L - Ang_b - Ang_c) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

            elif c_code == "134":       # 선4 하
                JOB_NO = "4034 "
                Pos_Num = 5

                # 시작 이동 중간점(0)
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b - Ang_c) * math.cos(C_RadianL) + Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b - Ang_c) * math.cos(C_RadianL) + PlasmaP_L_Y        # 피어싱 띄우기
                cal_robz = -(Ang_L - Ang_b - Ang_c) * math.sin(C_RadianL) + PlasmaP_L_Z       # 피어싱 띄우기
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Ang_L - Ang_b - Ang_c) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b - Ang_c) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Ang_a)
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL)
                cal_robz = -(Ang_L - Ang_b) * math.sin(C_RadianL)
                cal_rx = -Calc_DegreeL
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점(1)
                cal_robx = -(Ang_a) + 20     # X+20위치
                cal_roby = (Ang_L - Ang_b) * math.cos(C_RadianL) + Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

        pose_Arr.insert(0, "JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7))        #첫번째에 구분자,번호,P수를 전달
    except:
        pose_Arr = ["Error Return"]

    return pose_Arr
