import math
import json


    # # HP6
    # # 최종 리턴에서 str(roune(????, 3)).zfill(8) + ' '
    # return_arr.append("JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7) + ' ' + func_Set_Vel2(Work_T, Work_T2))           #7자리
    # for pose_buf in return_buf:         # 기준값 적용 및 로봇 자세 변환
    #     a1 = str(round(pose_buf[0] + stan_pos[0], 3)).zfill(8) + ' '
    #     a2 = str(round(pose_buf[1] + stan_pos[1], 3)).zfill(8) + ' '
    #     a3 = str(round(pose_buf[2] + stan_pos[2], 3)).zfill(8) + ' '
    #     a4 = str(round(pose_buf[3] + stan_pos[3], 3)).zfill(8) + ' '
    #     a5 = str(round(pose_buf[4] + stan_pos[4], 3)).zfill(8) + ' '
    #     a6 = str(round(pose_buf[5] + stan_pos[5], 3)).zfill(8)     # 로봇 자세값은 기준값에서 얻는다!
    #     return_arr.append(a1 + a2 + a3 + a4 + a5 + a6)

    # return return_arr


def func_channel_pose(DLL_VAL, GEdgeAdd):

    global JOB_NO
    global Pos_Num

    #===================================================================
    # "SEND", "0.0,0.0,500.0,180.0,0.0,-180.0$CH 100*50*6/8.5T,294,CH011,20,30,0,0,0$ 등

    VAL_buf = str(DLL_VAL).split('$')

    Size_buf = VAL_buf[1][3:]                   # CH 제거
    Size_buf2 = Size_buf.split('/')
    Size_buf = Size_buf2[0].split('*')
    Work_H = float(Size_buf[0])
    Work_B = float(Size_buf[1])
    Work_T = float(Size_buf[2])
    Work_T2 = float(Size_buf2[1].replace('T',''))

    WorkCode = str(VAL_buf[2]).split(',')       # ~> ["294","CH002","30","30","0","0","0"]
    c_code = WorkCode[1][2:]                    # CH 제거
    Wval_a = float(WorkCode[2])
    Wval_b = float(WorkCode[3])
    Wval_c = float(WorkCode[4])
    Wval_d = float(WorkCode[5])
    # Wval_Lenth = float(WorkCode[0])
    
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
   
    GES_Use = False
    GES_Shift = Work_T
    GES_Adjust = 0.0
    GES_Angle = 30
    GES_TIP_R = 6

    GCutLoss = 3            # 절단손실:고정값
    GCircleLoss2 = 1.3
    GCircleLoss = 2

    CUT_OUT = 2         # 4mm/2 : 노찌 방지용


    # 옆면 가공 로봇 자세 설정값
    C_RZ_1 = [45, 30, 15, 0]
    C_RZ_2 = [-45, -30, -15, 0]
    
    C_MoveRZ_1 = 20       # 옆면 이동 중간 각도
    C_MoveRZ_2 = -20      # 옆면 이동 중간 각도

    SideRZADJ = 100
    # GRobotLen에 따라서 계산
    if SideRZADJ > GRobotLen :
        SideRZADJ = SideRZADJ - GRobotLen       #100
    else:
        SideRZADJ = 0       #GRobotLen
        

    # C_RadianH = round(Calc_DegreeH * math.pi / 180, 3)      #라디안 =  각도 * 파이(PI)/180
    # C_RadianL = round(Calc_DegreeL * math.pi / 180, 3)


    GPlasmaGap = 6      # 플라즈마 GAP
    PlasmaGAP = GPlasmaGap
    TCPGAP = 6

    # GPlasmaP_H = 9      #피어싱 띄우기 높이
    PlasmaP_H = 9       #피어싱 띄우기 높이

    #프라즈마 절단 Loss
    PlasmaCutLoss = GCutLoss / 2

    # 시작/복귀점에 대한 Y,Z 여유값(기본:50mm)
    Margin_Y = 50
    ##Margin_Z = 60       #50  #Z+60위치 [08.02.21]수정 : 작은 자재 75*40이 그리퍼에 걸린다
    if(Work_B >= 75): 
        Margin_Z= 50
    else:
        Margin_Z = 125 - Work_B      # 토치의 대기 높이를 그리퍼 핸드(h:115)+10 =125 으로 한다.(충돌방지)

    # 자재 실제 크기 보정 (A & B)
    Work_H = Work_H + GSizeAdjustA
    Work_B = Work_B + GSizeAdjustB

    pose_Arr=[]     #빈 리스트 생성

    cal_robx = 0.0
    cal_roby = 0.0
    cal_robz = 0.0
    cal_rx = 0.0
    cal_ry = 0.0
    cal_rz = 0.0

    try:

        if c_code == "000":         #수직절단

            ####    Pos_Num = 14:
            ####
            ####    #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
            ####    ##if (Wval_a + Wval_b + Wval_c) == 0 :       # 수직절단
            ####
            ####    # 시작 이동 중간점1
            ####    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            ####    cal_roby = -PlasmaGAP - Margin_Y
            ####    cal_robz = Margin_Z
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 시작 이동 중간점2
            ####    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            ####    cal_roby = -PlasmaGAP - Margin_Y
            ####    cal_robz = Margin_Z
            ####    cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            ####    cal_rz = C_MoveRZ_2              # 이동 중간 각도
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 시작점
            ####    #cal_robx = 0
            ####    cal_roby = 0.0
            ####    cal_robz = -Work_B
            ####    cal_rx = Calc_DegreeH
            ####    cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    #cal_robx = 0
            ####    cal_roby = 0.0
            ####    cal_robz = -(Work_T * 1.5)
            ####    cal_rx = Calc_DegreeH
            ####    cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 곡직부
            ####    #cal_robx = 0
            ####    cal_roby = 0.0
            ####    cal_robz = 0
            ####    cal_rx = Calc_DegreeH / 2
            ####    cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 곡직부(각도턴)
            ####    #cal_robx = 0
            ####    ##cal_roby = (Work_T2 * 0.25)
            ####    cal_roby = 0.0
            ####    cal_robz = 0
            ####    cal_rx = Calc_DegreeH / 2
            ####    #[08.06.19삭제##
            ####    #cal_rz = C_RZ_2[3]   #0                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 중앙 기준값으로 ...
            ####    #cal_robx = 0
            ####    cal_roby = (Work_T2 * 1.5)
            ####    cal_robz = 0
            ####    #cal_rx = 0
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 중앙 직선부...
            ####    #cal_robx = 0
            ####    cal_roby = Work_H - (Work_T2 * 1.5)
            ####    cal_robz = 0
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 곡직부
            ####    #cal_robx = 0
            ####    ##cal_roby = Work_H - (Work_T2 * 0.25)
            ####    cal_roby = Work_H + PlasmaGAP - TCPGAP
            ####    cal_robz = 0
            ####    cal_rx = -Calc_DegreeL / 2
            ####    ##cal_rz = C_RZ_1[3]   #0
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 곡직부(각도턴)
            ####    #cal_robx = 0
            ####    cal_roby = Work_H + PlasmaGAP - TCPGAP
            ####    cal_robz = 0
            ####    cal_rx = -Calc_DegreeL / 2
            ####    cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    #cal_robx = 0
            ####    cal_roby = Work_H + PlasmaGAP - TCPGAP
            ####    cal_robz = -(Work_T * 1.5)
            ####    cal_rx = -Calc_DegreeL
            ####    cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    #cal_robx = 0
            ####    cal_roby = Work_H + PlasmaGAP - TCPGAP
            ####    cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
            ####    cal_rx = -Calc_DegreeL
            ####    cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 복귀 이동 중간점1
            ####    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            ####    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            ####    cal_robz = Margin_Z
            ####    cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            ####    cal_rz = C_MoveRZ_1             # 이동 중간 각도
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####
            ####    # 복귀 이동 중간점2
            ####    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            ####    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            ####    cal_robz = Margin_Z
            ####    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            ####    pose_Arr.append(cal_pose)
            ####    #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
            

            # 3면 분할 수직 절단 [09.05.26]
            JOB_NO = "4200 "
            Pos_Num = 15       # 곡직부(각도턴) 변경 [11.11.17]

            # 시작 이동 중간점1
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z         #[08.02.21]수정 : 작은 자재 75*40이 그리퍼에 걸린다.
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
            pose_Arr.append(cal_pose)

            # 시작 이동 중간점2
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z
            cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            cal_rz = C_MoveRZ_2              # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
            pose_Arr.append(cal_pose)

            cal_robx = 0.0
            cal_roby = 0.0
            cal_robz = -Work_B
            cal_rx = Calc_DegreeH
            cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            cal_robx = 0.0
            cal_roby = 0.0
            ##cal_robz = 0 + 2   #0   #-10     ###-(Work_T * 1.2)      ##0.9)
            ##cal_robz = -(Work_T + 3.5)         ## 3.5 겹치는 부분에 대한 값 #* 1.5)     ##  1.2)
            cal_robz = -(Work_T + 3.5) + 2       # [11.04.25] 임시 보정 2mm 더
            cal_rx = Calc_DegreeH
            cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 플라즈마 OFF

            #-------------------------------------------------
            # ###   # 곡직부(각도턴1)
            # ###   #cal_robx = 0
            # ###   cal_roby = 0.0 - 5       # -5 각도 턴을 위해
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = Calc_DegreeH / 4 * 3
            # ###   cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴2)
            # ###   #cal_robx = 0
            # ###   cal_roby = 0.0 #(Work_T2)
            # ###   cal_robz = 0 + 10      # +10 각도 턴을 위해
            # ###   cal_rx = Calc_DegreeH / 2
            # ###   cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴3)
            # ###   #cal_robx = 0
            # ###   cal_roby = 0.0
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = Calc_DegreeH / 4
            # ###   cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴4)
            # ###   #cal_robx = 0
            # ###   cal_roby = 0.0 #(Work_T2)
            # ###   cal_robz = 0
            # ###   cal_rx = 0
            # ###   cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴5)
            # ###   #cal_robx = 0
            # ###   cal_roby = 0.0
            # ###   cal_robz = 0
            # ###   cal_rx = 0
            # ###   cal_rz = 0
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   
            # ###   pose_Arr.append(cal_pose)

            # 곡직부(각도턴1)
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z
            cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            cal_rz = C_MoveRZ_2              # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부(각도턴2)
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)
            #-------------------------------------------------

            # 플라즈마 ON - Timer(T=I006)를 쓰지 않는다.
            # 중앙 직선부...
            cal_robx = 0.0
            cal_roby = 0.0
            cal_robz = 0.0
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            cal_robx = 0.0
            cal_roby = Work_H - (Work_T2)
            cal_robz = 0.0
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 플라즈마 OFF

            #-------------------------------------------------
            ####    # 곡직부(각도턴1)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H - (Work_T2)
            # ###   cal_robz = 0
            # ###   cal_rx = 0
            # ###   cal_rz = C_RZ_1[0] / 2 #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴1-2)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H - (Work_T2)
            # ###   cal_robz = 0
            # ###   cal_rx = 0
            # ###   cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴2)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H + PlasmaGAP - TCPGAP - 5       # -5 각도 턴을 위해
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = -Calc_DegreeL / 4
            # ###   cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴3)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = -Calc_DegreeL / 2
            # ###   cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴4)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H + PlasmaGAP - TCPGAP + 5       # +5 각도 턴을 위해
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = -Calc_DegreeL / 4 * 3
            # ###   cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)
            # ###
            # ###   # 곡직부(각도턴5)
            # ###   #cal_robx = 0
            # ###   cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###   cal_robz = 0 + 5       # +5 각도 턴을 위해
            # ###   cal_rx = -Calc_DegreeL
            # ###   cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            # ###   cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###   pose_Arr.append(cal_pose)

            # 곡직부(각도턴1)
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부(각도턴1-2)
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = C_MoveRZ_1             # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부(각도턴2)
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            cal_rz = C_MoveRZ_1             # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            #-------------------------------------------------

            cal_robx = 0.0
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = 0.0   ##1.5       ##-(Work_T * 1.2)     ##0.9)
            cal_rx = -Calc_DegreeL
            cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            cal_robx = 0.0
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
            cal_rx = -Calc_DegreeL
            cal_rz = C_RZ_1[0]   #45                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 복귀 이동 중간점1
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            cal_rz = C_MoveRZ_1             # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 복귀 이동 중간점2
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

        elif c_code == "005" or c_code == "025":       #대각절단: 좌, 우 ~ Case 5, 25    # 특수 대각귀(좌/우)
            JOB_NO = "4205 "
            Pos_Num = 14

            # 25 : 우
            if c_code == "025":   #가공 형태 코드      #if Work_Lenth > 0 :       # 우

                # 제일 긴 값:Calc_Cen
                if Wval_a <= Wval_b :
                    Calc_Cen = Wval_b
                else:
                    Calc_Cen = Wval_a
                
                if Wval_c <= Wval_d :
                    V_Thinkness = Wval_d
                else:
                    V_Thinkness = Wval_c
                
                if Calc_Cen <= V_Thinkness :
                    Calc_Cen = V_Thinkness                

                PlasmaCutLoss = 0   #우 대각은 절단손실 적용은 콘베어 이동에서

                Wval_a = Calc_Cen - Wval_a
                Wval_b = Calc_Cen - Wval_b
                Wval_c = Calc_Cen - Wval_c
                Wval_d = Calc_Cen - Wval_d

                ####        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                ####        # 우 절단에 두점이 0인 것의 마무리는 수직절단으로 하고, 0아닌 부분만 짜른다.
                ####        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                ####        if (Wval_b = 0 and Wval_c = 0) : ##GJobName = "CSPEDGE2.JBI"
                ####
                ####        if (Wval_b = 0 and Wval_a = 0) :
                ####
                ####            ##GJobName = "CSPEDGE2.JBI"
                ####
                ####            Wval_a = Calc_Cen - Wval_a
                ####            Wval_b = Calc_Cen - Wval_b
                ####            Wval_c = Calc_Cen - Wval_c
                ####
                ####            # 시작 이동 중간점
                ####
                ####            cal_robx = - Wval_c + PlasmaCutLoss
                ####            cal_roby = + (Work_B) * math.cos(C_RadianL) + PlasmaGAP - Margin_Y 
                ####            cal_robz = Margin_Z
                ####            rc = BscPutVarData(nCid, 4, 97, MidPosH(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####
                ####            cal_robx = - Wval_c + PlasmaCutLoss
                ####            cal_roby = + (Work_B) * math.cos(C_RadianL) + PlasmaGAP
                ####            cal_robz = + (Work_B) * math.sin(C_RadianL) - PlasmaGAP
                ####            cal_rx = - Calc_DegreeL
                ####            rc = BscPutVarData(nCid, 4, 1, MovePos4(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####
                ####            if (Wval_c == Wval_b) :
                ####                cal_robx = - Wval_b + PlasmaCutLoss
                ####            else:
                ####                cal_robx = - Wval_b - (Work_T * 1.5) / (Work_B / (Wval_c - Wval_b)) + PlasmaCutLoss # /math.tan 각도=(Work_B / Wval_c)
                ####            
                ####            cal_roby = + (Work_T * 1.5) * math.cos(C_RadianL) + PlasmaGAP
                ####            cal_robz = + (Work_T * 1.5) * math.sin(C_RadianL) - PlasmaGAP
                ####            cal_rx = - 15
                ####            rc = BscPutVarData(nCid, 4, 2, MovePos3(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####
                ####            if (Wval_c == Wval_b) :
                ####                cal_robx = - Wval_b + PlasmaCutLoss
                ####            else:
                ####                cal_robx = - Wval_b - (Work_T / 3) / (Work_B / (Wval_c - Wval_b)) + PlasmaCutLoss # /math.tan 각도=(Work_B / Wval_c)
                ####            
                ####            cal_roby = + (Work_T / 3) * math.cos(C_RadianL) + PlasmaGAP     # /2 -> /3 : 좀 더 위로..
                ####            cal_robz = + (Work_T / 3) * math.sin(C_RadianL) - PlasmaGAP
                ####            cal_rx = - 5
                ####            rc = BscPutVarData(nCid, 4, 3, MovePos6(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####            # 중앙 기준값으로 ...
                ####
                ####            cal_robx = - Wval_b + PlasmaCutLoss
                ####            cal_robz = - 0
                ####            rc = BscPutVarData(nCid, 4, 4, MovePos2(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####
                ####            # 작업 대기점
                ####            MidPosC = PointCPos
                ####            MidPosC(, 2) = - 50
                ####            MidPosC(, 1) = + (Work_H / 2)      #Y+Work_H/2 위치
                ####            MidPosC(, 0) = - Margin_Z        #Z-60위치
                ####            rc = BscPutVarData(nCid, 4, 99, MidPosC(0))
                ####            if rc <> 0 :
                ####                RPosChannel = False
                ####                Exit Function
                ####            
                ####
                ####
                ####            RPosChannel = True
                ####            Exit Function
                ####        
                ####        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            

            # 시작 이동 중간점1
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 시작 이동 중간점2
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = -PlasmaGAP - Margin_Y
            cal_robz = Margin_Z
            cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            cal_rz = C_MoveRZ_2              # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            cal_robx = -Wval_a + PlasmaCutLoss
            cal_roby = 0.0
            cal_robz = -(Work_B)
            cal_rx = Calc_DegreeH
            cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            if (Wval_a == Wval_b):
                cal_robx = -Wval_b + PlasmaCutLoss
            else:
                cal_robx = -Wval_b - (Work_T * 1.5) / (Work_B / (Wval_a - Wval_b)) + PlasmaCutLoss  # /math.tan 각도=(Work_B / Wval_a)
            
            cal_roby = 0.0
            cal_robz = -(Work_T * 1.5)
            cal_rx = Calc_DegreeH
            cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부
            cal_robx = -Wval_b + PlasmaCutLoss
            cal_roby = 0.0
            cal_robz = 0.0
            cal_rx = Calc_DegreeH / 2
            cal_rz = C_RZ_2[0]   #-45                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부(각도턴)
            cal_robx = -Wval_b + PlasmaCutLoss
            cal_roby = 0.0
            cal_robz = 0.0
            cal_rx = Calc_DegreeH / 2
            cal_rz = C_RZ_2[3]   #0                  # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 중앙 기준값으로 ...
            if (Wval_b == Wval_c) :
                cal_robx = -Wval_b + PlasmaCutLoss
            else:
                cal_robx = -Wval_b + (Work_T * 1.5) / (Work_H / (Wval_b - Wval_c)) + PlasmaCutLoss   # /math.tan 각도=(Work_B / Wval_c)
            
            cal_roby = (Work_T2 * 1.5)
            cal_robz = 0.0
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 중앙 직선부...
            if (Wval_b == Wval_c) :
                cal_robx = -Wval_c + PlasmaCutLoss
            else:
                #(Wval_c - Wval_b) <~ (Wval_b - Wval_c) : 오타 수정 [14.03.28]
                cal_robx = -Wval_c - (Work_T * 1.5) / (Work_H / (Wval_c - Wval_b)) + PlasmaCutLoss   # /math.tan 각도=(Work_B / Wval_c)
            
            cal_roby = Work_H - (Work_T2 * 1.5)
            cal_robz = 0.0
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부
            cal_robx = -Wval_c + PlasmaCutLoss
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = 0.0
            cal_rx = -Calc_DegreeL / 2
            ##cal_rz = C_RZ_1[3] #0         # 옆면 가공 로봇 자세 설정값
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 곡직부(각도턴)
            cal_robx = -Wval_c + PlasmaCutLoss
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = 0.0
            cal_rx = -Calc_DegreeL / 2
            cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            if (Wval_c == Wval_d) :
                cal_robx = -Wval_c + PlasmaCutLoss
            else:
                #(Wval_d - Wval_c) <~ (Wval_c - Wval_d) : 오타 수정 [14.03.28]
                cal_robx = -Wval_c - (Work_T * 1.5) / (Work_B / abs(Wval_d - Wval_c)) + PlasmaCutLoss  # /math.tan 각도=(Work_B / Wval_c)
            
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = -(Work_T * 1.5)
            cal_rx = -Calc_DegreeL
            cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            cal_robx = -Wval_d + PlasmaCutLoss
            cal_roby = Work_H + PlasmaGAP - TCPGAP
            cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
            cal_rx = -Calc_DegreeL
            cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 복귀 이동 중간점1
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            cal_rz = C_MoveRZ_1             # 이동 중간 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 복귀 이동 중간점2
            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
        
        else:       #상(좌 가공 ... 중간가공 .... 우 가공 ...) / 하(좌 가공 ... 중간가공 .... 우 가공 ...)

            # ===========================================================================
            # 상부 가공
            # ===========================================================================

            # 좌 가공 : 상 --------------------------------------------------------------
            if c_code == "001":         #좌 스닙 상
                JOB_NO = "4201 "
                Pos_Num = 6

                # 시작 이동 중간점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 중간점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                cal_roby = 0.0
                cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "002":       # 좌 각모 상
                JOB_NO = "4202 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 : 
                    Wval_c = Wval_b 
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss) #/ math.sqrt(2)
                    cal_roby = 0.0
                    cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)
                    cal_roby = 0.0
                    cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_d) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_roby = 0.0
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_roby = 0.0
                    cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)
                    cal_roby = 0.0
                    cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "003":       #좌 사각귀 상 ~ S개선 내용 추가 [13.10.24]
                JOB_NO = "4203 "
                Pos_Num = 12        # 2면 분할 사각귀 절단 [11.11.17]

                if ((Wval_b - Wval_a) == 0) :
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Work_B + Work_T2) / (Wval_b - Wval_a)    # tan 각도

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2 + 1
                    Wval_d = Work_T2 - 3
                
                # 시작 이동 중간점
                cal_robx = 0     ##SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = (Work_T2 + Wval_c) - PlasmaCutLoss         ####- Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 1차 상면
                cal_robx = 0.0
                cal_roby = (Work_T2 + Wval_c + GEdgeAdd) - PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Work_T2 + PlasmaCutLoss              # 좀 더 작게....
                cal_roby = (Wval_c + GEdgeAdd) - PlasmaCutLoss - 0.4     #0.4<~0.9=10도에 대한 보정값
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a) + PlasmaCutLoss           #T 만큼
                cal_roby = (Wval_d + GEdgeAdd) - PlasmaCutLoss - 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 옆으로 빠지는 위치
                cal_robx = -(Wval_a) + PlasmaCutLoss           #T 만큼
                if Wval_d > Work_T2 :    #상수d 큰 값일 때의 오류 수정 [13.10.25]
                    cal_roby = (Work_T2 + GEdgeAdd) - PlasmaCutLoss - 2.4       # 2mm 옆으로
                else:
                    cal_roby = (Wval_d + GEdgeAdd) - PlasmaCutLoss - 2.4       # 2mm 옆으로
                
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0.0      # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                #-------------------------------------------------
                # 곡직부(각도턴1)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴2)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-------------------------------------------------

                # 2차 옆면 ~ 사각귀 S개선 내용 추가 : GES_Angle(RY),GES_Shift(Rob_X) 적용하여 공통(일반,S개선) 사용 [13.10.24]
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                else:        #수정 : Wval_b~>Wval_a [15.05.10]
                    cal_robx = -((Wval_a + ((Work_T2 + Work_B - 1) / Calc_Cen))) + PlasmaCutLoss - GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = -(Work_B - 1)     # 각도 때문에 위로 1mm 보정
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # -(Work_T2) 까지
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                else:
                    cal_robx = -((Wval_a) + ((Work_T2 * 2) / Calc_Cen)) + PlasmaCutLoss - GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = -(Work_T2)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 위로 빠지는 위치 : 각도 30도에 대한 보정값
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                else:
                    cal_robx = -((Wval_a) + ((Work_T2 - 2) / Calc_Cen)) + PlasmaCutLoss - GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = 2     # 2mm 위로
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2      # 이동 중간 각도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_ry = GES_Angle / 2    #+15/0도~ 좌 사각귀 S개선은 각도/2 해야 원할한 복귀 행정
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_MoveRZ_2             # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

            elif c_code == "004":       # 좌 속 사각귀
                JOB_NO = "4204 "
                Pos_Num = 18

                # 시작 이동 중간점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 중간점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = 0.0
                cal_robz = -(Wval_b + (Wval_b * 0.6 + GEdgeAdd)) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_b      #Work_T
                cal_roby = 0.0
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = 0.0             
                cal_rx = Calc_DegreeH / 2
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴) ~ 추가 [21.12.02]
                cal_robx = -(Wval_a) + PlasmaCutLoss - 4        ##추가-4
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH / 2
                cal_rz = 0.0        ##cal_rz = C_RZ_2[3]   #0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴)
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH / 2
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중앙 기준값으로 ...
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = (Work_T2 * 1.5)
                cal_robz = 0.0
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중앙 직선부...
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = Work_H - (Work_T2 * 1.5)
                cal_robz = 0
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0.0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴) ~ 추가 [21.12.02]
                cal_robx = -(Wval_a) + PlasmaCutLoss - 4        ##추가-4
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴)
                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_b
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b + (Wval_b * 0.6 + GEdgeAdd)) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 중간 가공 : 상 ------------------------------------------------------------
            elif c_code == "011" or c_code == "012" :       # 원 상 / # 멀티원 상
                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4211 "
                Pos_Num = 15          #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 멀티원의 두 번째 원 작업
                if c_code == "012" and GDblJobExecCode == 1 :
                    Wval_b = Wval_b + Wval_c

                Cir_R = 0.0     #반지름
                Calc_Deg_A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]
                Calc_Deg_B = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]

                Cir_R = (Wval_a / 2 - PlasmaCutLoss)
                Calc_Deg_A[2] = Cir_R * math.sin(20 * round(math.pi / 180, 9))
                Calc_Deg_A[7] = Cir_R * math.sin(70 * round(math.pi / 180, 9))
                Calc_Deg_A[8] = Cir_R * math.sin(80 * round(math.pi / 180, 9))

                Calc_Deg_B[2] = Cir_R * math.cos(20 * round(math.pi / 180, 9))
                Calc_Deg_B[7] = Cir_R * math.cos(70 * round(math.pi / 180, 9))
                Calc_Deg_B[8] = Cir_R * math.cos(80 * round(math.pi / 180, 9))


                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 시작점
                cal_robx = -Wval_a / 2
                cal_roby = -PlasmaP_H + TCPGAP   # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH        #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T2 >= 9 :
                ##                        # 반복 (5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_roby = 0.0
                ##                        cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                        cal_rx = Calc_DegreeH
                ##                        cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        pose_Arr.append(cal_pose)
                ##                    else:

                ##중복 Point 제거 [2021.04.01]
                ## 반복 (3,)
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a / 4
                cal_roby = 0.0
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                
                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                ##                    cal_robx = -PlasmaCutLoss
                ##                    cal_roby = 0.0
                ##                    cal_robz = -(Work_B - Wval_b)
                ##                    cal_rx = Calc_DegreeH
                ##                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_roby = 0.0
                ##                    cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                    cal_rx = Calc_DegreeH
                ##                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 + Calc_Deg_A[8]
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + Calc_Deg_B[8])
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 + Calc_Deg_B[7]
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - Calc_Deg_A[7])
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 0.5)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 - Calc_Deg_A[2]
                cal_roby = 0.0 - 0.5
                cal_robz = -(Work_B - Wval_b - Calc_Deg_B[2] + 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                #============================
                cal_robx = -(Wval_a * 0.75)
                cal_roby = 0.0
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                #============================
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "013":       # 평 타원 상
                JOB_NO = "4213 "
                Pos_Num = 15

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = -PlasmaP_H + TCPGAP      # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH        #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a / 2
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -(Wval_a + Wval_c) / 2 - 1
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "014":       # 직 타원 상
                JOB_NO = "4214 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = -PlasmaP_H + TCPGAP       # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH                    #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01] [02.24]
                ## 반복(5,)
                #cal_robx = -PlasmaCutLoss
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = 0.0
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_rx = Calc_DegreeH
                #cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                # 반복(10,)
                # cal_robx = -PlasmaCutLoss
                # cal_roby = 0.0
                # cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                # cal_rx = Calc_DegreeH
                # cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                # cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                # pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -PlasmaCutLoss - 2
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - 1)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            ##elif c_code == "015":       # V 컷팅 상

            elif c_code == "016":       # ㄷ 컷팅 상
                JOB_NO = "4216 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Work_B)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                cal_roby = 0.0
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                cal_roby = 0.0
                cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 우 가공 : 상 --------------------------------------------------------------
            elif c_code == "021":       # 우 스닙 상
                JOB_NO = "4201 "
                Pos_Num = 6

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = -(Work_B)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                cal_roby = 0.0
                cal_robz = -(Work_B - (Wval_b + 1) + PlasmaCutLoss)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "022":       # 우 각모 상
                JOB_NO = "4202 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 :
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -(Work_B)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -(Work_B)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_d)     # 수정 [11.11.29]        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = 0.0
                    cal_robz = -(Work_B - (Wval_c) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = 0.0
                    cal_robz = -(Work_B - (Wval_b) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -(Work_B)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = 0.0
                    cal_robz = -(Work_B - (Wval_c) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a - Wval_d)        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = 0.0
                    cal_robz = -(Work_B - (Wval_b) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = 0.0
                    cal_robz = -(Work_B - (Wval_b + Wval_d) + PlasmaCutLoss)
                    cal_rx = Calc_DegreeH
                    cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "023":       # 우 사각귀 상 ~ S개선 내용 추가 [13.10.24]

                #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
                # 2면 분할 사각귀 절단 [11.11.17]
                JOB_NO = "4203 "
                Pos_Num = 13

                if Wval_b - Wval_a == 0 :
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Work_B + Work_T2) / (Wval_b - Wval_a)    # tan 각도
                
                if Wval_b <= Wval_a :
                    Work_Lenth = Wval_a
                else:
                    Work_Lenth = Wval_b

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2 + 1
                    Wval_d = Work_T2 - 3


                # 시작 이동 중간점
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)     ##SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = (Work_T2 + Wval_c) - PlasmaCutLoss         ####- Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 1차 상면 피어싱
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)         #- PlasmaCutLoss                  #T 만큼
                cal_roby = (Work_T2 + Wval_c + GEdgeAdd) - PlasmaCutLoss
                cal_robz = (PlasmaP_H - TCPGAP)
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #적용X#     cal_P_time = IIf(GTime_Set = 1, 0.1, 10)   # 시작 시간을 0.1로 최소화 한다.[11.11.15] 추가
                pose_Arr.append(cal_pose)

                # 1차 상면
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)         #- PlasmaCutLoss                  #T 만큼
                cal_roby = (Work_T2 + Wval_c + GEdgeAdd) - PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a) + Work_T2           #- PlasmaCutLoss              #T 만큼
                cal_roby = (Wval_c + GEdgeAdd) - PlasmaCutLoss - 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Work_Lenth - Wval_a)
                cal_roby = (Wval_d + GEdgeAdd) - PlasmaCutLoss - 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 옆으로 빠지는 위치
                cal_robx = -(Work_Lenth - Wval_a)
                if Wval_d > Work_T2 :    #상수d 큰 값일 때의 오류 수정 [13.10.25]
                    cal_roby = (Work_T2 + GEdgeAdd) - PlasmaCutLoss - 2.4       # 2mm 옆으로
                else:
                    cal_roby = (Wval_d + GEdgeAdd) - PlasmaCutLoss - 2.4       # 2mm 옆으로
                
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 10       # 상부 10도
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #-------------------------------------------------
                # 곡직부(각도턴1)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴2)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-------------------------------------------------

                # 2차 옆면 ~ 사각귀 S개선 내용 추가 : GES_Angle(RY),GES_Shift(Rob_X) 적용하여 공통(일반,S개선) 사용 [13.10.24]
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:        #수정 : Wval_b~>Wval_a [15.05.10]
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 + Work_B - 1) / Calc_Cen) + GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = -(Work_B - 1)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # -(Work_T2) 까지
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 * 2) / Calc_Cen) + GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = -(Work_T2)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 위로 빠지는 위치 : 각도 30도에 대한 보정값
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 - 2) / Calc_Cen) + GES_Shift
                
                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = 2     # 2mm 위로
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = Calc_DegreeH
                else:
                    cal_rx = Calc_DegreeH / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_ry = 0.0
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

            elif c_code == "024":       # 우 속 사각귀
                JOB_NO = "4204 "
                Pos_Num = 18

                # 시작 이동 중간점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 중간점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)        #+ PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Wval_b + (Wval_b * 0.6 + GEdgeAdd)) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a - Wval_b)
                cal_roby = 0.0
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0      #cal_robx = + PlasmaCutLoss
                cal_roby = 0.0
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = Calc_DegreeH - 15
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부
                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH / 2
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴) ~ 추가 [21.12.02]
                cal_robx = -4         ##추가-4
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH / 2
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴)
                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = 0.0
                cal_rx = Calc_DegreeH / 2
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중앙 기준값으로 ...
                cal_robx = 0.0
                cal_roby = (Work_T2 * 1.5)
                cal_robz = 0.0
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 중앙 직선부...
                cal_robx = 0.0
                cal_roby = Work_H - (Work_T2 * 1.5)
                cal_robz = 0.0
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부
                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0.0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴) ~ 추가 [21.12.02]
                cal_robx = -4        ##추가-4
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0.0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴)
                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = 0.0
                cal_rx = -Calc_DegreeL / 2
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a - Wval_b)       #+ PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b * 0.6 + GEdgeAdd) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a      #+ PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Wval_b + (Wval_b * 0.6 + GEdgeAdd)) + PlasmaCutLoss
                cal_rx = -Calc_DegreeL + 15
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            # 선1,2,3,4 : 상 ------------------------------------------------------------
            # 선은 플라즈마 절단 손실을 계산하지는 않는다 - 어는 방향일지 모르므로....(입력시 고려하여 입력)

            elif c_code == "031":       # 선1 상
                JOB_NO = "4231 "
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -PlasmaP_H + TCPGAP       # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "032":       # 선2 상 S개선
                JOB_NO = "4232 "
                Pos_Num = 7

                #------------------------------------------------------------------
                if Wval_d > 100 :            # S개선 각도 [12.03.13]~>[13.10.24]
                    # 변수활용 : 옆면(상,하)의 개선shift값 (쟌넬 옆면 두께 특성 고려 T2-2mm)
                    ##Calc_Cen = (Work_T2 - 2 + (PlasmaGAP - TCPGAP)) * math.tan((Wval_d) * round(math.pi / 180, 9))
                    #개선 각도와 이동량 계산 ~ 높이 보정값(1.5mm) 추가 [13.10.24]
                    if Wval_d > 200 :     #우 S개선
                        Wval_d = -(Wval_d - 200)      #-30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = -PlasmaCutLoss + (float(Work_T2) - 2 + GES_Adjust) * math.tan(float(-Wval_d) * round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    else:        #좌 S개선
                        Wval_d = Wval_d - 100         #30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = PlasmaCutLoss - (float(Work_T2) - 2 + GES_Adjust) * math.tan(float(Wval_d) * round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    
                else:
                    Calc_Cen = 0        #일반
                
                #------------------------------------------------------------------

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d / 2          # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -PlasmaP_H + TCPGAP       # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP
                if (Work_B - Wval_b - Wval_a) <= 0 :
                    cal_robz = -(Work_B - Wval_b - Wval_a - 2)   #2mm 더 위로 절단 추가 [13.10.24]
                else:
                    cal_robz = -(Work_B - Wval_b - Wval_a)
                
                cal_rx = Calc_DegreeH
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d / 2          # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "033":       # 선3 상
                JOB_NO = "4233 "            
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -PlasmaP_H + TCPGAP       # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "034":       # 선4 상
                JOB_NO = "4234 "
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = -PlasmaP_H + TCPGAP       # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = 0.0
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = Calc_DegreeH
                cal_rz = C_RZ_2[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        
            # ===========================================================================
            # 중부 가공
            # ===========================================================================

            # 중간 가공 : 중 --------------------------------------------------------------
            elif c_code == "111" or c_code == "112":       # 원 중앙 / # 멀티원 중앙
                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4271 "
                Pos_Num = 13      #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 멀티원의 두 번째 원 작업
                if c_code == "112" and GDblJobExecCode == 1 :
                    Wval_b = Wval_b + Wval_c
                
                Cir_R = 0.0     #반지름
                Calc_Deg_A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]
                Calc_Deg_B = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]

                Cir_R = (Wval_a / 2 - PlasmaCutLoss)
                Calc_Deg_A[2] = Cir_R * math.sin(20 * round(math.pi / 180, 9))
                Calc_Deg_A[7] = Cir_R * math.sin(70 * round(math.pi / 180, 9))
                Calc_Deg_A[8] = Cir_R * math.sin(80 * round(math.pi / 180, 9))

                Calc_Deg_B[2] = Cir_R * math.cos(20 * round(math.pi / 180, 9))
                Calc_Deg_B[7] = Cir_R * math.cos(70 * round(math.pi / 180, 9))
                Calc_Deg_B[8] = Cir_R * math.cos(80 * round(math.pi / 180, 9))


                # 시작 이동 중간점
                cal_robx = -Wval_a / 2
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #시작점
                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)             # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                     #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T >= 9 :
                ##                        # 반복(5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                        cal_robz = (PlasmaGAP - TCPGAP)
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        
                ##                        
                ##                        pose_Arr.append(cal_pose)
                ##                    else:

                ##중복 Point 제거 [2021.04.01]
                ## 반복(3,)
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a / 4
                cal_roby = ((Wval_b) - (Wval_a / 4))
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                ##                    cal_robx = -PlasmaCutLoss
                ##                    cal_roby = (Wval_b)
                ##                    cal_robz = (PlasmaGAP - TCPGAP)
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                    cal_robz = (PlasmaGAP - TCPGAP)
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 + Calc_Deg_A[8]
                cal_roby = (Wval_b + Calc_Deg_B[8])
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 + Calc_Deg_B[7]
                cal_roby = (Wval_b - Calc_Deg_A[7])
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss + 0.5)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 - Calc_Deg_A[2]
                cal_roby = (Wval_b - Calc_Deg_B[2] + 2)
                cal_robz = (PlasmaGAP - TCPGAP) - 0.5
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 종료점 추가
                #============================
                cal_robx = -(Wval_a * 0.75)
                cal_roby = ((Wval_b) - (Wval_a / 4))
                cal_robz = (PlasmaGAP - TCPGAP)
                #============================
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "113":       # 평 타원 중앙
                JOB_NO = "4273 "
                Pos_Num = 13       #17<-12    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a / 2
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -(Wval_a + Wval_c) / 2 - 1
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "114":       # 직 타원 중앙
                JOB_NO = "4274 "
                Pos_Num = 13       #17<-12    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 시작 이동 중간점
                cal_robx = -Wval_a / 2
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b - Wval_c / 2)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -PlasmaCutLoss
                #cal_roby = (Wval_b - Wval_c / 2)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = (Wval_b - Wval_c / 2)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = (Wval_b - Wval_c / 2)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = (Wval_b + Wval_c / 2)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = (Wval_b + Wval_c / 2)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = (Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b + Wval_c / 2)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -PlasmaCutLoss
                #cal_roby = (Wval_b + Wval_c / 2)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -PlasmaCutLoss - 2
                cal_roby = (Wval_b - 1)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -PlasmaCutLoss
                cal_roby = (Wval_b)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            # 선1,2,3,4 : 중 ------------------------------------------------------------
            
            elif c_code == "131":       # 선1 중앙
                JOB_NO = "4276 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                
                cal_robx = 0.0
                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -(Wval_a)
                cal_roby = (Wval_b)
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "132":       # 선2 중앙 ~ 선2 S개선 적용 [13.10.25]
                JOB_NO = "4277 "
                Pos_Num = 5

                #------------------------------------------------------------------
                if Wval_d > 100 :            # S개선 각도 [12.03.13]~>[13.10.24]
                    # 변수활용 : 개선shift값
                    ##Calc_Cen = (Work_T + (PlasmaGAP - TCPGAP)) * math.tan((Wval_d) * round(math.pi / 180, 9))
                    #개선 각도와 이동량 계산 ~ 높이 보정값(1.5mm) 추가 [13.10.24]
                    if Wval_d > 200 :     #우 S개선
                        Wval_d = -(Wval_d - 200)      #-30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = -PlasmaCutLoss + (float(Work_T) + GES_Adjust) * math.tan(float(-Wval_d) * round(math.pi / 180, 9))  #T2에 따른 개선의 Shift값 계산
                    else:        #좌 S개선
                        Wval_d = Wval_d - 100         #30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = PlasmaCutLoss - (float(Work_T) + GES_Adjust) * math.tan(float(Wval_d) * round(math.pi / 180, 9))  #T2에 따른 개선의 Shift값 계산
                    
                else:
                    Calc_Cen = 0        #일반
                #------------------------------------------------------------------

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Wval_b)
                cal_robz = (GES_Adjust + PlasmaGAP - TCPGAP)
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = (Wval_b + Wval_a)           # - ==> +로 수정[09.01.16]
                cal_robz = (GES_Adjust + PlasmaGAP - TCPGAP)
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_roby = (Wval_b + Wval_a)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "133":       # 선3 중앙
                JOB_NO = "4278 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Wval_b + Wval_c)           # - ==> +로 수정[09.01.16]
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Wval_b + Wval_c)           # - ==> +로 수정[09.01.16]
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


                # 복귀 이동 중간점
                cal_robx = -(Wval_a)
                cal_roby = (Wval_b)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "134":       # 선4 중앙
                JOB_NO = "4279 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Wval_b)
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = (Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = (Wval_b + Wval_c)           # - ==> +로 수정[09.01.16]
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -(Wval_a)
                cal_roby = (Wval_b + Wval_c)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            # 중간 특수 가공 RS
            elif c_code == "181":       #RS 중상 [12.03.13]
                JOB_NO = "4281 "
                Pos_Num = 10      #중복 Point 제거 [2021.04.01]

                # 시작 이동 중간점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + CUT_OUT / 2  # 4mm/2 : 노찌 방지용
                cal_roby = (Wval_a + Wval_b) - CUT_OUT       # 4mm : 노찌 방지용
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + CUT_OUT / 2  # 4mm/2 : 노찌 방지용
                cal_roby = (Wval_a + Wval_b) - CUT_OUT       # 4mm : 노찌 방지용
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c)
                cal_roby = (Wval_a + Wval_b) - PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a
                cal_roby = (Wval_a + Wval_b) - PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## R 시작부분
                #cal_robx = -Wval_a
                #cal_roby = (Wval_a + Wval_b) - PlasmaCutLoss
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # R 중간
                cal_robx = -(Wval_a - Wval_a / math.sqrt(2))
                cal_roby = (Wval_a / 2 + Wval_b)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # R 끝 부분
                cal_robx = 0
                cal_roby = (Wval_b) + PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ###중복 Point 제거 [2021.04.01]
                #cal_robx = 0
                #cal_roby = (Wval_b) + PlasmaCutLoss
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c)
                cal_roby = (Wval_b) + PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 피양점
                cal_robx = -(Wval_a + Wval_c) + CUT_OUT
                cal_roby = (Wval_b) + CUT_OUT
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = 0
                cal_roby = (Wval_b) + CUT_OUT
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "182":       #RS 중하 [12.03.13]
                JOB_NO = "4282 "
                Pos_Num = 10      #중복 Point 제거 [2021.04.01]

                # 시작 이동 중간점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + CUT_OUT / 2          # 4mm/2 : 노찌 방지용
                cal_roby = Work_H - ((Wval_a + Wval_b) - CUT_OUT)    # 4mm : 노찌 방지용
                cal_robz = (PlasmaP_H - TCPGAP)         # 피어싱 띄우기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + CUT_OUT / 2          # 4mm/2 : 노찌 방지용
                cal_roby = Work_H - ((Wval_a + Wval_b) - CUT_OUT)    # 4mm : 노찌 방지용
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c)
                cal_roby = Work_H - ((Wval_a + Wval_b) - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a
                cal_roby = Work_H - ((Wval_a + Wval_b) - PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## R 시작부분
                #cal_robx = -Wval_a
                #cal_roby = Work_H - ((Wval_a + Wval_b) - PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # R 중간
                cal_robx = -(Wval_a - Wval_a / math.sqrt(2))
                cal_roby = Work_H - ((Wval_a / 2 + Wval_b))
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # R 끝 부분
                cal_robx = 0
                cal_roby = Work_H - ((Wval_b) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                #cal_robx = 0
                #cal_roby = Work_H - ((Wval_b) + PlasmaCutLoss)
                #cal_robz = (PlasmaGAP - TCPGAP)
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c)
                cal_roby = Work_H - ((Wval_b) + PlasmaCutLoss)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 피양점
                cal_robx = -(Wval_a + Wval_c) + CUT_OUT
                cal_roby = Work_H - ((Wval_b) + CUT_OUT)
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -(Wval_a + Wval_c) + CUT_OUT
                cal_roby = Work_H - ((Wval_b) + CUT_OUT)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



            # ===========================================================================
            # 하부 가공
            # ===========================================================================

            # 좌 가공 : 하 --------------------------------------------------------------    
            elif c_code == "201":       #좌 스닙 하
                JOB_NO = "4201 "
                Pos_Num = 6

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "202":       # 좌 각모 하
                JOB_NO = "4202 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 :
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_d) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "203":       #좌 사각귀 하 ~ S개선 내용 추가 [13.10.24]
                # 2면 분할 사각귀 절단 [11.11.17]
                JOB_NO = "4203 "
                Pos_Num = 12

                if Wval_b - Wval_a == 0 :
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Work_B + Work_T2) / (Wval_b - Wval_a)    # tan 각도
                
                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2 + 1
                    Wval_d = Work_T2 - 3

                # 시작 이동 중간점
                cal_robx = 0.0     ##SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H - (Work_T2 + Wval_c) + PlasmaCutLoss       ####+ Margin_Y      #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0       # 상부 정상각
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 1차 상면
                cal_robx = 0.0
                cal_roby = Work_H - (Work_T2 + Wval_c + GEdgeAdd) + PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 0       # 상부 정상각
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Work_T2 + PlasmaCutLoss
                cal_roby = Work_H - (Wval_c + GEdgeAdd) + PlasmaCutLoss + 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a) + PlasmaCutLoss
                cal_roby = Work_H - (Wval_d + GEdgeAdd) + PlasmaCutLoss + 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 옆으로 빠지는 위치
                cal_robx = -(Wval_a) + PlasmaCutLoss
                if Wval_d > Work_T2 :    #상수d 큰 값일 때의 오류 수정 [13.10.25]
                    cal_roby = Work_H - (Work_T2 + GEdgeAdd) + PlasmaCutLoss + 2.4       # 2mm 옆으로
                else:
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) + PlasmaCutLoss + 2.4       # 2mm 옆으로
                
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #-------------------------------------------------
                # 곡직부(각도턴1)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴2)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-------------------------------------------------

                # 2차 옆면 ~ 사각귀 S개선 내용 추가 : GES_Angle(RY),GES_Shift(Rob_X) 적용하여 공통(일반,S개선) 사용 [13.10.24]
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift           #T 만큼
                else:        #수정 : Wval_b~>Wval_a [15.05.10]
                    cal_robx = -((Wval_a) + ((Work_T2 + Work_B - 1) / Calc_Cen)) + PlasmaCutLoss - GES_Shift #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - 1)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # -(Work_T2) 까지
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift           #T 만큼
                else:
                    cal_robx = -((Wval_a) + ((Work_T2 * 2) / Calc_Cen)) + PlasmaCutLoss - GES_Shift #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = -(Work_T2)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 위로 빠지는 위치 : 각도 30도에 대한 보정값
                if (Wval_a == Wval_b) :
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift           #T 만큼
                else:
                    cal_robx = -((Wval_a) + ((Work_T2 - 2) / Calc_Cen)) + PlasmaCutLoss - GES_Shift #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = 2     # 2mm 위로
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = GES_Angle      #+30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_ry = GES_Angle / 2    #+15/0도~ 좌 사각귀 S개선은 각도/2 해야 원할한 복귀 행정
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 중간 가공 : 하 ------------------------------------------------------------
            elif c_code == "211" or c_code == "212" :       # 원 하 / # 멀티원 하
                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4211 "
                Pos_Num = 15      #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 멀티원의 두 번째 원 작업
                if c_code == "212" and GDblJobExecCode == 1 :
                    Wval_b = Wval_b + Wval_c

                Cir_R = 0.0     #반지름
                Calc_Deg_A = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]
                Calc_Deg_B = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]   #As Double [9]

                Cir_R = (Wval_a / 2 - PlasmaCutLoss)
                Calc_Deg_A[2] = Cir_R * math.sin(20 * round(math.pi / 180, 9))
                Calc_Deg_A[7] = Cir_R * math.sin(70 * round(math.pi / 180, 9))
                Calc_Deg_A[8] = Cir_R * math.sin(80 * round(math.pi / 180, 9))

                Calc_Deg_B[2] = Cir_R * math.cos(20 * round(math.pi / 180, 9))
                Calc_Deg_B[7] = Cir_R * math.cos(70 * round(math.pi / 180, 9))
                Calc_Deg_B[8] = Cir_R * math.cos(80 * round(math.pi / 180, 9))


                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaP_H - TCPGAP        # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL      #+ 8     #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T2 >= 9 :
                ##                        # 반복(5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_roby = Work_H + PlasmaGAP - TCPGAP
                ##                        cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                ##                        cal_rx = -Calc_DegreeL
                ##                        cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        pose_Arr.append(cal_pose)
                ##                    else:

                ##중복 Point 제거 [2021.04.01]
                ## 반복(3,)
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a * 0.75
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)


                ##                    cal_robx = -Wval_a + PlasmaCutLoss
                ##                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                ##                    cal_robz = -(Work_B - Wval_b)
                ##                    cal_rx = -Calc_DegreeL
                ##                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                ##                    cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                ##                    cal_rx = -Calc_DegreeL
                ##                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 - Calc_Deg_A[8]
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) + Calc_Deg_B[8])
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 - Calc_Deg_B[7]
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_A[7])
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss + 0.5)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 + Calc_Deg_A[2]
                cal_roby = Work_H + PlasmaGAP - TCPGAP + 0.5
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_B[2] + 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                #============================
                cal_robx = -(Wval_a / 4)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                #============================
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "213":       # 평 타원 하
                JOB_NO = "4213 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H + PlasmaP_H - TCPGAP        # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL       #+ 8    #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a / 2
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -Wval_a / 2 + 1
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "214":       # 직 타원 하
                JOB_NO = "4214 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaP_H - TCPGAP      # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL                     #+ 8    #원점에서(기울기 각도)       # 면에 수직
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -PlasmaCutLoss
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -PlasmaCutLoss
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_roby = Work_H + PlasmaGAP - TCPGAP
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_rx = -Calc_DegreeL
                #cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -Wval_a + PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -Wval_a + PlasmaCutLoss + 2
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - 1)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            ##elif c_code == "215":     # V 컷팅 하

            elif c_code == "216":       # ㄷ 컷팅 하
                JOB_NO = "4216 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)


            # 우 가공 : 하 --------------------------------------------------------------
            elif c_code == "221":       # 우 스닙 하
                JOB_NO = "4201 "
                Pos_Num = 6

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -((Work_B - (Wval_b + 1)) + PlasmaCutLoss)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "222":       # 우 각모 하
                JOB_NO = "4202 "
                Pos_Num = 8

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 :
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -(Work_B)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -(Work_B)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_d)     # 수정 [11.11.29]       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_c)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_b)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -(Work_B)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_c)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a - Wval_d)       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_b)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                    cal_rx = -Calc_DegreeL
                    cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "223":       # 우 사각귀 하 ~ S개선 내용 추가 [13.10.24]
                # 2면 분할 사각귀 절단 [11.11.17]
                JOB_NO = "4203 "
                Pos_Num = 13

                if Wval_b - Wval_a == 0 :
                    Calc_Cen = 0
                else:
                    Calc_Cen = (Work_B + Work_T2) / (Wval_b - Wval_a)    # tan 각도

                if Wval_b <= Wval_a :
                    Work_Lenth = Wval_a
                else:
                    Work_Lenth = Wval_b

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2 + 1
                    Wval_d = Work_T2 - 3

                # 시작 이동 중간점
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)     ##SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H - (Work_T2 + Wval_c) + PlasmaCutLoss         ####- Margin_Y
                cal_robz = Margin_Z
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 1차 상면 피어싱
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)                         #- PlasmaCutLoss       #T 만큼     #T 만큼
                cal_roby = Work_H - (Work_T2 + Wval_c + GEdgeAdd) + PlasmaCutLoss
                cal_robz = (PlasmaP_H - TCPGAP)
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 1차 상면
                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a)                         #- PlasmaCutLoss       #T 만큼     #T 만큼
                cal_roby = Work_H - (Work_T2 + Wval_c + GEdgeAdd) + PlasmaCutLoss
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = 0.0       # 상부 정상각
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Work_Lenth - Wval_a) - (Wval_a) + Work_T2         #- PlasmaCutLoss       #T 만큼      #T 만큼
                cal_roby = Work_H - (Wval_c + GEdgeAdd) + PlasmaCutLoss + 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Work_Lenth - Wval_a)
                cal_roby = Work_H - (Wval_d + GEdgeAdd) + PlasmaCutLoss + 0.4
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 옆으로 빠지는 위치
                cal_robx = -(Work_Lenth - Wval_a)
                if Wval_d > Work_T2 :    #상수d 큰 값일 때의 오류 수정 [13.10.25]
                    cal_roby = Work_H - (Work_T2 + GEdgeAdd) + PlasmaCutLoss + 2.4       # 2mm 옆으로
                else:
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) + PlasmaCutLoss + 2.4       # 2mm 옆으로
                
                cal_robz = (PlasmaGAP - TCPGAP)
                cal_rx = -10       # 상부 10도
                cal_rz = 0.0       # 상부 정상각
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #-------------------------------------------------
                # 곡직부(각도턴1)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 곡직부(각도턴2)
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-------------------------------------------------

                # 2차 옆면 ~ 사각귀 S개선 내용 추가 : GES_Angle(RY),GES_Shift(Rob_X) 적용하여 공통(일반,S개선) 사용 [13.10.24]
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:        #수정 : Wval_b~>Wval_a [15.05.10]
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 + Work_B - 1) / Calc_Cen) + GES_Shift #- PlasmaCutLoss #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - 1)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # -(Work_T2) 까지
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 * 2) / Calc_Cen) + GES_Shift #- PlasmaCutLoss #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = -(Work_T2)
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 2mm 위로 빠지는 위치 : 각도 30도에 대한 보정값
                if (Wval_a == Wval_b) :
                    cal_robx = -(Work_Lenth - Wval_a) + GES_Shift
                else:
                    cal_robx = -(Work_Lenth - Wval_a) + ((Work_T2 - 2) / Calc_Cen) + GES_Shift #- PlasmaCutLoss #T 만큼
                
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = 2     # 2mm 위로
                #++++++++++++++++++++++++++++++++++++++++++++++
                if GES_Use :
                    cal_rx = -Calc_DegreeL
                else:
                    cal_rx = -Calc_DegreeL / 2
                
                cal_ry = -GES_Angle     #-30/0도
                #++++++++++++++++++++++++++++++++++++++++++++++
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점1
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_ry = 0.0
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 복귀점2
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            # 선1,2,3,4 : 하 ------------------------------------------------------------

            elif c_code == "231":       # 선1 하
                JOB_NO = "4231 "
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)                

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaP_H - TCPGAP      # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "232":       # 선2 하 S개선
                JOB_NO = "4232 "
                Pos_Num = 7

                #------------------------------------------------------------------
                if Wval_d > 100 :            # S개선 각도 [12.03.13]~>[13.10.24]
                    # 변수활용 : 옆면(상,하)의 개선shift값 (쟌넬 옆면 두께 특성 고려 T2-2mm)
                    ##Calc_Cen = (Work_T2 - 2 + (PlasmaGAP - TCPGAP)) * math.tan((Wval_d) * round(math.pi / 180, 9))
                    #개선 각도와 이동량 계산 ~ 높이 보정값(1.5mm) 추가 [13.10.24]
                    if Wval_d > 200 :     #우 S개선
                        Wval_d = -(Wval_d - 200)      #-30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = -PlasmaCutLoss + (float(Work_T2) - 2 + GES_Adjust) * math.tan(float(-Wval_d) * round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    else:        #좌 S개선
                        Wval_d = Wval_d - 100         #30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) * round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Calc_Cen = PlasmaCutLoss - (float(Work_T2) - 2 + GES_Adjust) * math.tan(float(Wval_d) * round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    
                else:
                    Calc_Cen = 0        #일반
                
                #------------------------------------------------------------------

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d / 2          # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaP_H - TCPGAP        # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP
                if (Work_B - Wval_b - Wval_a) <= 0 :
                    cal_robz = -(Work_B - Wval_b - Wval_a - 2)   #2mm 더 위로 절단 추가 [13.10.24]
                else:
                    cal_robz = -(Work_B - Wval_b - Wval_a)
                
                cal_rx = -Calc_DegreeL
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d              # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                #------------------------------------------------------------------
                cal_robx = Calc_Cen
                cal_ry = Wval_d / 2          # S개선 각도 [12.03.13]
                #------------------------------------------------------------------
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_ry = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "233":       # 선3 하
                JOB_NO = "4233 "
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaP_H - TCPGAP        # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "234":       # 선4 하
                JOB_NO = "4234 "
                Pos_Num = 7

                # 시작 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작 이동 각도 변경점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaP_H - TCPGAP        # 피어싱 띄우기
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b - Wval_c)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_roby = Work_H + PlasmaGAP - TCPGAP
                cal_robz = -(Work_B - Wval_b)
                cal_rx = -Calc_DegreeL
                cal_rz = C_RZ_1[0]          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = C_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
        
        pose_Arr.insert(0, "JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7))        #첫번째에 구분자,번호,P수를 전달  
    except:
        pose_Arr = ["Error Return"]

    return pose_Arr
