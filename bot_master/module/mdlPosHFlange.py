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


def func_hflange_pose(DLL_VAL, GEdgeAdd):

    global JOB_NO
    global Pos_Num

    #===================================================================
    # "SEND", "0.0,0.0,500.0,180.0,0.0,-180.0$HB 100*50*6/8.5T,294,HB002,30,30,0,0,0$ 등

    VAL_buf = str(DLL_VAL).split('$')
    
    Size_buf = VAL_buf[1][3:]                   # 'HB ', 'IB ' 제거
    Size_buf2 = Size_buf.split('/')
    Size_buf = Size_buf2[0].split('*')
    Work_H = float(Size_buf[0])
    Work_B = float(Size_buf[1])
    Work_T = float(Size_buf[2])
    Work_T2 = float(Size_buf2[1].replace('T',''))

    WorkCode = str(VAL_buf[2]).split(',')       # ~> ["294","HB002","30","30","0","0","0"]
    c_code = WorkCode[1][2:]                    # HB, IB 제거
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
    GSizeAdjustC = 0
    GSizeAdjustD = 0
    GBeamAdjustMH = 0
    #===================================================================
        
    GES_Use = False
    GES_Shift = Work_T
    GES_Adjust = 0.0
    GES_Angle = 30
    GES_TIP_R = 6

    GCutLoss = 3            # 절단손실:고정값
    GCircleLoss2 = 1.3
    GCircleLoss = 2

    # 옆면 가공 로봇 자세 설정값
    H_RZ_1 = 45            # 로봇 옆면 가공 RZ_1 각도
    H_RZ_2 = -45           # 로봇 옆면 가공 RZ_2 각도

    H_MoveRZ_1 = 20       # 옆면 이동 중간 각도
    H_MoveRZ_2 = -20      # 옆면 이동 중간 각도

    SideRZADJ = 100     # 로봇 옆면 가공 중간 이동 보정 X값(100)

    # GRobotLen에 따라서 계산
    if SideRZADJ > GRobotLen :
        SideRZADJ = SideRZADJ - GRobotLen       #100
    else:
        SideRZADJ = 0       #GRobotLen

    GPlasmaGap = 6      # 플라즈마 GAP
    PlasmaGAP = GPlasmaGap
    TCPGAP = 6

    GPlasmaP_H = 9      #피어싱 띄우기 높이
    PlasmaP_H = 9       #피어싱 띄우기 높이

            
    #프라즈마 절단 Loss
    PlasmaCutLoss = GCutLoss / 2

    # 시작/복귀점에 대한 Y,Z 여유값(기본:50mm)
    Margin_Y = 50
    ##Margin_Z = 50
    if(Work_B >= 75): 
        Margin_Z= 50
    else:
        Margin_Z = 125 - Work_B      # 토치의 대기 높이를 그리퍼 핸드(h:115)+10 =125 으로 한다.(충돌방지)
        
    
    # 자재 실제 크기 보정 (A & B)
    Work_H = Work_H + GSizeAdjustA
    Work_B = Work_B + GSizeAdjustB


    # 작업 위치 방향 (A형/B형)
    if GWorkPosition :
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # 자재 실제 크기 보정값 C & D에 따른 계산(B형방향)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Adj_C_L = abs(GSizeAdjustC)         # 자재 보정값 C의 절대값
        if(GSizeAdjustC >= 0):
            Adj_C_Sign = 0          # 자재 보정값 C의 부호값
        else:
            Adj_C_Sign = -1  

        Adj_D_H = -abs(GSizeAdjustD)        # 자재 보정값 D의 절대값
        if(GSizeAdjustD >= 0):
            Adj_D_Sign = 0          # 자재 보정값 D의 부호값
        else:
            Adj_D_Sign = -1
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    else:
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # 자재 실제 크기 보정값 C & D에 따른 계산(A형방향)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        
        Adj_C_L = -abs(GSizeAdjustC)        # 자재 보정값 C의 절대값
        if(GSizeAdjustC >= 0):
            Adj_C_Sign = 0          # 자재 보정값 C의 부호값
        else:
            Adj_C_Sign = -1  

        Adj_D_H = abs(GSizeAdjustD)        # 자재 보정값 D의 절대값
        if(GSizeAdjustD >= 0):
            Adj_D_Sign = 0          # 자재 보정값 D의 부호값
        else:
            Adj_D_Sign = -1
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    

    # HB_S_Cfg = "&H0080"       #[16.12.15]
    # HB_E_Cfg = "&H0080"       #[16.12.15]

    pose_Arr=[]     #빈 리스트 생성

    cal_robx = 0.0
    cal_roby = 0.0
    cal_robz = 0.0
    cal_rx = 0.0
    cal_ry = 0.0
    cal_rz = 0.0
    
    try:

        if c_code == "000":         # 수직절단
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # 우 사각귀 수직 절단 보상용 : 중앙 종료부 ~ 추가 보정 1P [11.10.25]
            if GE_CutLast == 1 :        # 우 사각귀 상
                JOB_NO = "4351 "
                Pos_Num = 14       #14<-13
            elif GE_CutLast == 2 :      # 우 사각귀 하
                JOB_NO = "4352 "
                Pos_Num = 14       #14<-13
            elif GE_CutLast == 3 :      # 우 사각귀 상 & 하
                JOB_NO = "4353 "
                Pos_Num = 6        #6<-5
            else:
                JOB_NO = "4300 "
                Pos_Num = 22       #22<-21<-16
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++

            #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
            ##if (Wval_a + Wval_b + Wval_c) = 0 :       # 수직절단

            # 시작 이동 중간점 ~ P이동
            cal_robx = 0.0
            cal_roby = Work_H / 2
            cal_robz = Margin_Z
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            #----------------------------------------------------------------------------------
            # 중앙 시작부(1mm씩 Y,Z로 더 높이기)
            cal_robx = 0.0   #강제 보정 함수에서...  1.5  1mm  0  # 강제 보정
            ##cal_roby = (Work_T2 + 7 + 3) + 1   # +7 : 내부 벽면에서 띄우는 값    +3 : 피어싱
            cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
            cal_roby = (Work_T2 + 7 + 2) + 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign)) # +7 : 내부 벽면에서 띄우는 값    +3 : 피어싱
            cal_rx = -30     # -20 [11.07.16] & 7+2 <- &+3 (위 Y값)
            cal_rz = -10      # RZ : -10
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 중앙 중심부...
            cal_robx = 0.0   #강제 보정 함수에서...  2.2   #강제보정[2007.12.11] 1.7mm   #0       ##1.5         # 강제 보정
            cal_roby = Work_H / 2
            cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 중앙 종료부
            cal_robx = 0.0   #강제 보정 함수에서...  #3.5  2.4mm  0   1.5         # 강제 보정
            ##cal_roby = Work_H - (Work_T2 + 7) - 1  ##- 4     # +7 : 내부 벽면에서 띄우는 값   # 강제보정 -4 더
            cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
            cal_roby = Work_H - (Work_T2 + 7) - 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign)) ##- 4     # +7 : 내부 벽면에서 띄우는 값   # 강제보정 -4 더
            cal_rx = 30
            cal_rz = 10       # RZ : +10
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 중앙 종료부 ~ 추가 보정 1P [11.10.25]
            cal_robx = 0.0   #강제 보정 함수에서...  #3.5   #강제보정[2007.12.11] 2.4mm   #0       ##1.5         # 강제 보정
            ##cal_roby = Work_H - (Work_T2 + 7) - 1  ##- 4     # +7 : 내부 벽면에서 띄우는 값   # 강제보정 -4 더
            cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + 2 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]    # +2 1P 추가하여 Z방향으로 높임
            cal_roby = Work_H - (Work_T2 + 7) - 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign)) ##- 4     # +7 : 내부 벽면에서 띄우는 값   # 강제보정 -4 더
            cal_rx = 30
            cal_rz = 10       # RZ : +10
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)
            #----------------------------------------------------------------------------------

            # 전체 좌우 강제 보정 이전
            ##                    #----------------------------------------------------------------------------------
            ##                    # 중앙 시작부(1mm씩 Y,Z로 더 높이기)
            ##                    cal_robx = 1.5   #강제보정[2007.12.11] 1mm   #0       ##1.5         # 강제 보정
            ##                    cal_roby = (Work_T2 + 7 + 3) + 1   # +7 : 내부 벽면에서 띄우는 값
            ##                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + 1
            ##                    cal_rx = -20
            ##                    cal_rz = -10      # RZ : -10
            ##
            ##                    # 중앙 중심부...
            ##                    cal_robx = 2.2   #강제보정[2007.12.11] 1.7mm   #0       ##1.5         # 강제 보정
            ##                    cal_roby = Work_H / 2
            ##                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
            ##
            ##                    # 중앙 종료부
            ##                    cal_robx = 3.5   #강제보정[2007.12.11] 2.4mm   #0       ##1.5         # 강제 보정
            ##                    cal_roby = Work_H - (Work_T2 + 7) - 4     # +7 : 내부 벽면에서 띄우는 값   # 강제보정 -4 더
            ##                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
            ##                    cal_rx = 30
            ##                    cal_rz = 10       # RZ : +10
            ##                    #----------------------------------------------------------------------------------

            # 반복 ~ 동작 중간 대기점:P051
            cal_robx = SideRZADJ     # [11.03.16] 추가
            cal_roby = Work_H / 2
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            ####                    #33333333333333333333333333~X
            # ###                    if GE_CutLast != 3 :
            # ###
            # ###                        pose_Arr.append(cal_pose)
            # ###
            # ###
            # ###                        #11111111111111111111111111~X
            # ###                        if GE_CutLast != 1 :
            # ###
            # ###
            # ###                            # 동작 중간 대기점
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = -PlasmaGAP - 50 
            # ###                            cal_robz = 50
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            # 동작 중간 각도 변경점 ~ P이동
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = -PlasmaGAP - 50 
            # ###                            cal_robz = 50
            # ###                            cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            # ###                            cal_rz = H_MoveRZ_2              # 이동 중간 각도  #H_RZ_2
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            #----------------------------------------------------------------------------------
            # ###                            # H빔 수직 절단 위에서 아래로 (상부가 기준점이므로 자재의 크기와 관계없이 잘린다.)
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = 0.0
            # ###                            #cal_robz = 0     ##- 2              # -2 : 절단 부분 좀 더 보정(잘 안 잘림)
            # ###                            cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
            # ###                            cal_rx = Calc_DegreeH
            # ###                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = 0.0
            # ###                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1          # -1mm 수평 절단 위로
            # ###                            cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
            # ###                            cal_rx = Calc_DegreeH
            # ###                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = 0.0
            # ###                            cal_robz = -(Work_B + Work_T * 1.3) / 2 + PlasmaCutLoss
            # ###                            cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
            # ###                            cal_rx = Calc_DegreeH
            # ###                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # ###
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = 0.0
            # ###                            cal_robz = -Work_B - 1           # 최종 절단은 좀더 아래로
            # ###                            cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
            # ###                            cal_rx = Calc_DegreeH
            # ###                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #----------------------------------------------------------------------------------
            # ###
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                            # 반복 P056 ~ 동작 중간 대기점:P056, P055, P066, P065
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                            # 반복 P056 ~ # 동작 중간 각도 변경점
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = -PlasmaGAP - 50 
            # ###                            cal_robz = 50
            # ###                            cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
            # ###                            cal_rz = H_MoveRZ_2              # 이동 중간 각도  #H_RZ_2
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                            # 반복 P055 ~ # 동작 중간 대기점 ~ P이동
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = -PlasmaGAP - 50 
            # ###                            cal_robz = 50
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                        
            # ###                        #11111111111111111111111111~X
            # ###
            # ###                        #22222222222222222222222222~X
            # ###                        if GE_CutLast != 2 :
            # ###
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                            # 반복 P066 ~ # 복귀 이동 중간점
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            # ###                            cal_robz = Margin_Z
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###                            # 반복 P065 ~ # 복귀 이동 각도점 ~ P이동
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            # ###                            cal_robz = Margin_Z
            # ###                            cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            # ###                            cal_rz = H_MoveRZ_1             # 이동 중간 각도  #H_RZ_1
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # ###
            # ###                            #----------------------------------------------------------------------------------
            # ###                            #MovePos(10,0) = 0
            # ###                            ##cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###                            #cal_robz = 0
            # ###                            cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
            # ###                            cal_rx = -Calc_DegreeL
            # ###                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1          # -1mm 수평 절단 위로
            # ###                            cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
            # ###                            cal_rx = -Calc_DegreeL
            # ###                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###                            cal_robz = -(Work_B + Work_T * 1.3) / 2 + PlasmaCutLoss
            # ###                            cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
            # ###                            cal_rx = -Calc_DegreeL
            # ###                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # ###
            # ###                            #cal_robx = 0
            # ###                            ##cal_roby = Work_H + PlasmaGAP - TCPGAP
            # ###                            cal_robz = -Work_B - 1            # 최종 절단은 좀더 아래로
            # ###                            cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
            # ###                            cal_rx = -Calc_DegreeL
            # ###                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###                            #----------------------------------------------------------------------------------
            # ###
            # ###                            # 복귀 이동 각도점
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            # ###                            cal_robz = Margin_Z
            # ###                            cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
            # ###                            cal_rz = H_MoveRZ_1             # 이동 중간 각도  #H_RZ_1
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                            # 복귀 이동 중간점 ~ P이동
            # ###                            cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
            # ###                            cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
            # ###                            cal_robz = Margin_Z
            # ###                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            # ###                            pose_Arr.append(cal_pose)
            # ###
            # ###                        #22222222222222222222222222~X
            # ###
            # ###                    #33333333333333333333333333~X

            #선2 S개선의 마무리 동작(토치 충돌 방지)을 위해 아래에서 위로 행정 변경 [15.07.09]
            #33333333333333333333333333~X
            if GE_CutLast != 3 :

                pose_Arr.append(cal_pose)

                #11111111111111111111111111~X
                if GE_CutLast != 1 :

                    # 동작 중간 대기점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - 50 
                    cal_robz = Margin_Z
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 각도 변경점 ~ P이동
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - 50 
                    cal_robz = Margin_Z
                    cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도  #H_RZ_2
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #----------------------------------------------------------------------------------
                    # H빔 수직 절단 아래에서 위로 수정 [15.07.09]
                    cal_robx = 0.0
                    ##cal_roby = 0.0
                    cal_robz = -Work_B - 0           #최초 절단은 0에서 [15.07.09]
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    cal_robx = 0.0
                    ##cal_roby = 0.0
                    cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    ##cal_roby = 0.0
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                    cal_robx = 0.0
                    ##cal_roby = 0.0
                    cal_robz = 2                     #최종 절단은 위로 [15.07.09]
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #----------------------------------------------------------------------------------

                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # 반복 P056 ~ 동작 중간 대기점:P056, P055, P066, P065
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # 반복 P056 ~ # 동작 중간 각도 변경점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - 50 
                    cal_robz = Margin_Z
                    cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도  #H_RZ_2
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # 반복 P055 ~ # 동작 중간 대기점 ~ P이동
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - 50 
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                #11111111111111111111111111~X

                #22222222222222222222222222~X
                if GE_CutLast != 2 :

                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # 반복 P066 ~ # 복귀 이동 중간점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    # 반복 P065 ~ # 복귀 이동 각도점 ~ P이동
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
                    cal_rz = H_MoveRZ_1             # 이동 중간 각도  #H_RZ_1
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                    #----------------------------------------------------------------------------------
                    # H빔 수직 절단 아래에서 위로 수정 [15.07.09]
                    cal_robx = 0.0
                    ##cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -Work_B - 0            #최종 절단은 0에서 [15.07.09]
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    cal_robx = 0.0
                    ##cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    ##cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                    #MovePos(10,0) = 0
                    ##cal_roby = Work_H + PlasmaGAP - TCPGAP
                    cal_robz = 2                     #최종 절단은 위로 [15.07.09]
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #----------------------------------------------------------------------------------

                    # 복귀 이동 각도점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = -Calc_DegreeL / 2      # 이동 중간 각도
                    cal_rz = H_MoveRZ_1             # 이동 중간 각도  #H_RZ_1
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점 ~ P이동
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                
                #22222222222222222222222222~X
            
            #33333333333333333333333333~X

            GE_CutLast = 0         # 앵글 마지막 피스 수직 절단 보상용 초기화(우 사각귀 수직 절단 보상용으로 활용)
            GH_REdge_Up = 0 
            GH_REdge_Down = 0

            #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

            ##Case 5, 25    # 특수 대각귀(좌/우)

            #WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

        else:
            # ===========================================================================
            # 상부 가공
            # ===========================================================================

            # 좌 가공 : 상 --------------------------------------------------------------
            if c_code == "001" or c_code == "101" :         # 좌 스닙 상
                JOB_NO = "4301 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)                
                pose_Arr.append(cal_pose)

                if c_code == "001" :        # 상 0 / 1 구분
                    cal_robx = 0.0
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)      ##- TCPGAP : 오류
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                    cal_robz = -(Work_B + 1)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -((Wval_b) - PlasmaCutLoss)           ##- TCPGAP : 오류
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                    cal_robz = 1
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "002" or c_code == "102" :       # 좌 각모 상
                JOB_NO = "4302 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 : 
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    if c_code == "002" :        # 상 0 / 1 구분
                        cal_robx = 0.0
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss) #/ math.sqrt(2)
                        cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -(Work_B + 1)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss) #/ math.sqrt(2)
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = 1
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:
                    if c_code == "002" :        # 상 0 / 1 구분
                        cal_robx = 0.0
                        cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_d) - PlasmaCutLoss)   #/ math.sqrt(2)
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                        cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -(Work_B + 1)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -((Wval_b + Wval_d) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_d) - PlasmaCutLoss)   #/ math.sqrt(2)
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = 1
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "003" :                          # 좌 사각귀 상

                ##                    if Wval_b - Wval_a = 0 :
                ##                        Calc_Cen = 0
                ##                    else:
                ##                        Calc_Cen = (Work_B + Wval_c) / (Wval_b - Wval_a)    # tan 각도

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2
                    Wval_d = Work_T2

                #-------------------------------------------------------------------
                # 사각귀의 2행정 구분 작업 (첫번째) : P값도 시작/종료부를 포함하여 순차적으로 JOB을 구성
                if GDblJobExecCode == 0 :                    
                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30]
                        JOB_NO = "4364 "
                        Pos_Num = 10
                    else:
                        JOB_NO = "4303 "
                        Pos_Num = 10

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
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용
                        #=======================================================================================================
                        #=======================================================================================================

                        # 시작점
                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -Work_B - 2           # 최종 절단은 좀 더 아래로 : 2mm<-1 [13.10.24]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        #                            #종료 중간점 [추가] ~ NO
                        #                            cal_robx = -(Wval_a) + PlasmaCutLoss
                        #                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1
                        #                            cal_roby = -PlasmaGAP - Margin_Y
                        #                            cal_rx = Calc_DegreeH
                        #                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        #                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        #                            pose_Arr.append(cal_pose)

                        #=======================================================================================================
                        #=======================================================================================================

                    else:
                        # 시작점
                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -Work_B - 1           # 최종 절단은 좀 더 아래로
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    # 2차 시작점
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift + 1.5         #1.5 절단면을 벗어나도록
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_ry = GES_Angle       #S개선:적용=40도/비적용=0도
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 1 + 2        #추가로 2 더
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 각도점 (& 이전은 시작 이동 중간점과 동일)
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - Margin_Y 
                    cal_robz = Margin_Z
                    cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    
                    pose_Arr.append(cal_pose)

                    # 동작 중간 대기점 (& 이전은 시작 이동 중간점과 동일)
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - Margin_Y 
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #-------------------------------------------------------------------

                else:    # 사각귀의 2행정 구분 작업 (두번째)
                    JOB_NO = "4362 "
                    Pos_Num = 7
                    
                    # 3차 시작 대기 점 (추가)
                    cal_robx = -(Wval_a / 2)
                    cal_roby = (Work_T2 * 3)
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = -10              # RZ : -10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점
                    # [11.11.16] 피어싱 높이로 밖(-2mm)에서 들어오는 1P 추가
                    cal_robx = -(Wval_a) + PlasmaCutLoss + 7    # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    ##cal_roby = + (Work_T2 * 1.2 + GEdgeAdd) + PlasmaCutLoss ####+ 2     #+3:RZ 기울기에 따른 보정
                    cal_roby = (Wval_d + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign)) - 2       # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = -10              # RZ : -10 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점 실제
                    cal_robx = -(Wval_a) + PlasmaCutLoss + 7    # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    ##cal_roby = + (Work_T2 * 1.2 + GEdgeAdd) + PlasmaCutLoss ####+ 2     #+3:RZ 기울기에 따른 보정
                    cal_roby = (Wval_d + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = -10              # RZ : -10 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a / 2)                # 행정의 중간 점까지
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = ((Wval_d + Wval_c) / 2 + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))      # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20
                    cal_rz = -10              # RZ : -10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -Wval_c
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Wval_c + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = 0.0   # 좌 사각귀는 각도를 푼다 [11.11.17]    #-20              # RY : -20
                    cal_rz = -10              # RZ : -10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 2        # 시작부 더(좌 사각귀 만)
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Work_T2 + Wval_c) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))          # 안쪽으로 더 붙이기
                    cal_ry = 0.0   # 좌 사각귀는 각도를 푼다 [11.11.17]    #-20              # RY : -20
                    cal_rz = -10              # RZ : -10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = (Work_T2 + Wval_c) + PlasmaCutLoss    ####+ 2     #+3:RZ 기울기에 따른 보정
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                #-------------------------------------------------------------------

                ####                Case 4

            # 중간 가공 : 상 ------------------------------------------------------------
            elif c_code == "011" or c_code == "111" :       # 원 상 / #Case 12  # 멀티원 상
                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4311 "
                Pos_Num = 15          #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 상 0 / 1 구분
                if c_code == "111" :        # 상 0 / 1 구분
                    Wval_b = (Work_B - Wval_b)

                # # 멀티원의 두 번째 원 작업
                # if c_code == "012" and GDblJobExecCode == 1 :
                #     Wval_b = Wval_b + Wval_c
                #     # 상 0 / 1 구분
                #     if c_code == "111" :       # 상 0 / 1 구분
                #         Wval_b = (Work_B - Wval_b - Wval_c)
                    
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))   # 피어싱 띄우기
                cal_rx = Calc_DegreeH        #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T2 >= 9 :
                ##                        # 반복 (5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                        cal_rx = Calc_DegreeH
                ##                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        pose_Arr.append(cal_pose)
                ##                    else:

                ##중복 Point 제거 [2021.04.01]
                ## 반복 (3,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a / 4
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                ##                    cal_robx = -PlasmaCutLoss
                ##                    cal_robz = -(Work_B - Wval_b)
                ##                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                    cal_rx = Calc_DegreeH
                ##                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                ##                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                    cal_rx = Calc_DegreeH
                ##                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 + Calc_Deg_A[8]
                cal_robz = -((Work_B - Wval_b) + Calc_Deg_B[8])
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 + Calc_Deg_B[7]
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_A[7])
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 0.5)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 - Calc_Deg_A[2]
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_B[2] + 2)
                cal_roby = 0.0 - 0.5 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                #cal_robx = -Wval_a / 2 - 1
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + 2 + PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #============================
                #안쪽으로 깊게 빠지기
                #============================
                cal_robx = -(Wval_a * 0.75)
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #============================
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "013" or c_code == "113" :       # 평 타원 상
                JOB_NO = "4313 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 상 0 / 1 구분
                if c_code == "113" :       # 상 0 / 1 구분
                    Wval_b = (Work_B - Wval_b)
                
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))      # 피어싱 띄우기
                cal_rx = Calc_DegreeH        #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -(Wval_a + Wval_c) / 2 - 1
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "014" or c_code == "114" :       # 직 타원 상
                JOB_NO = "4314 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 상 0 / 1 구분
                if c_code == "114" :       # 상 0 / 1 구분
                    Wval_b = (Work_B - Wval_b)

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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                cal_rx = Calc_DegreeH                    #- 8   #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_rx = Calc_DegreeH
                #cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -PlasmaCutLoss - 2
                cal_robz = -(Work_B - Wval_b - 1)
                cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_rx = Calc_DegreeH
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y 
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            ##Case 15       # V 컷팅 상

            elif c_code == "016" or c_code == "116" :       # ㄷ 컷팅 상
                JOB_NO = "4316 "
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
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 상 0 / 1 구분
                if c_code == "016" :        # 상 0 / 1 구분
                    cal_robx = -PlasmaCutLoss
                    cal_robz = -(Work_B)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -PlasmaCutLoss
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -(Work_B + 1)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = -PlasmaCutLoss
                    #cal_robz = 0
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -PlasmaCutLoss
                    cal_robz = -((Wval_b) - PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -((Wval_b) - PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = 1
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
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
            elif c_code == "021" or c_code == "121" :       # 우 스닙 상
                JOB_NO = "4301 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 상 0 / 1 구분
                if c_code == "001" :        # 상 0 / 1 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_robz = -(Work_B - (Wval_b + 1) + PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = 0.0
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_robz = -((Wval_b + 1) - PlasmaCutLoss)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "022" or c_code == "122" :       # 우 각모 상
                JOB_NO = "4302 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 : 
                    Wval_c = Wval_b 
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    # 상 0 / 1 구분
                    if c_code == "022" :        # 상 0 / 1 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_d)     # 수정 [11.11.29]        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(Work_B - (Wval_c) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(Work_B - (Wval_b) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = 0.0
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = 0.0
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:
                    # 상 0 / 1 구분
                    if c_code == "022" :        # 상 0 / 1 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - (Wval_c) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(Work_B - (Wval_b) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(Work_B - (Wval_b + Wval_d) + PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = 0.0
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)        #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)          #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Wval_b + Wval_d) - PlasmaCutLoss)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "023" :                          # 우 사각귀 상

                ##                    if Wval_b - Wval_a = 0 :
                ##                        Calc_Cen = 0
                ##                    else:
                ##                        Calc_Cen = (Work_B + Wval_c) / (Wval_b - Wval_a)    # tan 각도
                ##                    
                ##
                ##                    if Wval_b <= Wval_a :
                ##                        Work_Lenth = Wval_a
                ##                    else:
                ##                        Work_Lenth = Wval_b
                ##                    

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2
                    Wval_d = Work_T2
                
                # 사각귀의 2행정 구분 작업 (첫번째)
                if GDblJobExecCode == 0 :                    
                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30]
                        JOB_NO = "4365 "
                        Pos_Num = 13
                    else:
                        JOB_NO = "4361 "
                        Pos_Num = 12

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
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 0차 시작점
                    cal_robx = -(Wval_a)
                    #cal_robz = 0     ##- 3              # -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -Work_B - 1           # 최종 절단은 좀 더 아래로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용

                        #=======================================================================================================
                        #=======================================================================================================

                        #시작 중간점 [추가]
                        cal_robx = 0 + GES_Shift
                        cal_roby = -PlasmaGAP - Margin_Y 
                        #cal_robz = 0
                        cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                        cal_rz = H_MoveRZ_2              # 이동 중간 각도
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        # 1차 시작점
                        cal_robx = 0 + GES_Shift
                        #cal_robz = 0     ##- 3              # -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -Work_B - 2           # 최종 절단은 좀 더 아래로 : 2mm<-1 [13.10.24]
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        #                            #종료 중간점 [추가] ~ NO
                        #                            #cal_robx = 0
                        #                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1          # -1mm 수평 절단 위로
                        #                            cal_roby = -PlasmaGAP - Margin_Y
                        #                            cal_rx = Calc_DegreeH
                        #                            cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        #                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        #                            pose_Arr.append(cal_pose)

                        #=======================================================================================================
                        #=======================================================================================================

                    else:
                        # 1차 시작점
                        cal_robx = 0.0
                        cal_robz = 0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -Work_B - 1           # 최종 절단은 좀 더 아래로
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    # 2차 시작점
                    cal_robx = GES_Shift - 1.5          #1.5 절단면을 벗어나도록
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_ry = -GES_Angle      #S개선:적용=40도/비적용=0도(-)
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 각도점 (& 이전은 시작 이동 중간점과 동일)
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_2              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 대기점 (& 이전은 시작 이동 중간점과 동일)
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = -PlasmaGAP - Margin_Y
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)
                    #-------------------------------------------------------------------

                else:    # 사각귀의 2행정 구분 작업 (두번째)
                    JOB_NO = "4362 "
                    Pos_Num = 7

                    # 3차 시작 대기 점 (추가)
                    cal_robx = -(Wval_a / 2)
                    cal_roby = (Work_T2 * 3)
                    cal_robz = Margin_Z
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점
                    # [11.11.16] 피어싱 높이로 밖(-2mm)에서 들어오는 1P 추가
                    cal_robx = -6     # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Wval_d + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign)) - 2       # 안쪽으로 더 붙이기
                    cal_ry = 15               # RY : +15
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점 실제
                    cal_robx = -6     # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Wval_d + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = 15               # RY : +15
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a / 2)                # 행정의 중간 점까지
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = ((Wval_d + Wval_c) / 2 + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))     # 안쪽으로 더 붙이기
                    cal_ry = 0.0
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a - Wval_c) #* 1.2)        # T2로 바뀌었으므로 .2배 하지 않는다. [11.06.10]
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Wval_c + GEdgeAdd) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = -20   # 우 사각귀는 각도를 더 준다 [11.11.17]    #-15              # RY : -15
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = (Work_T2 + Wval_c) + PlasmaCutLoss - 1 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = -20   # 우 사각귀는 각도를 더 준다 [11.11.17]    #-20, -18, -15              # RY : -15
                    cal_rz = -45              # RZ : -45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = 50          # 안쪽으로....
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 우 사각귀 상(1) 수직 절단 보상용
                    ##GE_CutLast = GE_CutLast + 1
                    GH_REdge_Up = 1
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

            # 선1,2,3,4 : 상 ------------------------------------------------------------

            elif c_code == "031" or c_code == "131" :       # 선1 상
                JOB_NO = "4331 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 상 0 / 1 구분
                if c_code == "031" :        # 상 0 / 1 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b)
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "032" or c_code == "132" :       # 선2 상
                JOB_NO = "4332 "
                if Wval_d < 100 :   #일반
                    Pos_Num = 7
                else:
                    if Wval_b < (Work_B / 2 - Work_T2) and (Wval_a - Wval_b) > (Work_B / 2 + Work_T2) :    #T포함의 경우
                        JOB_NO = "4366 "
                        Pos_Num = 8
                    else:
                        JOB_NO = "4367 "
                        Pos_Num = 6
                    
                    #개선 각도와 이동량 계산 ~ 높이 보정값(1.5mm) 추가 [13.09.07]
                    if Wval_d > 200 :     #우 S개선
                        Wval_d = -(Wval_d - 200)      #-30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) *  round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Wval_c = -PlasmaCutLoss + (float(Work_T2) + GES_Adjust) * math.tan(float(-Wval_d) *  round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    else:        #좌 S개선
                        Wval_d = Wval_d - 100         #30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) *  round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Wval_c = PlasmaCutLoss - (float(Work_T2) + GES_Adjust) * math.tan(float(Wval_d) *  round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산

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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if Wval_d == 0 :   #일반

                    # 상 0 / 1 구분
                    if c_code == "032" :        # 상 0 / 1 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b)
                        cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b - Wval_a)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -(Wval_b)
                        cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Wval_b)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Wval_b + Wval_a)
                        cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:    #선2 S개선 상
                    cal_robx = Wval_c
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))      # 피어싱 띄우기~>일반 띄우기
                    cal_rx = Calc_DegreeH
                    cal_ry = Wval_d       #30도/-30도
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # T의 중간 부분
                    if Wval_b < (Work_B / 2 - Work_T2) and (Wval_a - Wval_b) > (Work_B / 2 + Work_T2) :   #T포함의 경우
                        cal_robx = Wval_c
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = Wval_d       #30도/-30도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = Wval_c
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3
                        cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                        cal_rx = Calc_DegreeH
                        cal_ry = Wval_d       #30도/-30도
                        cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    cal_robx = Wval_c
                    if (Work_B - Wval_b - Wval_a) <= 0 :
                        cal_robz = -(Work_B - Wval_b - Wval_a - 2)   #2mm 더 위로 절단 추가 [13.10.24]
                    else:
                        cal_robz = -(Work_B - Wval_b - Wval_a)
                    
                    cal_roby = -GES_Adjust - PlasmaGAP + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_ry = Wval_d       #30도/-30도
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_ry = 0.0
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "033" or c_code == "133" :       # 선3 상
                JOB_NO = "4333 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 상 0 / 1 구분
                if c_code == "033" :        # 상 0 / 1 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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

            elif c_code == "034" or c_code == "134" :       # 선4 상
                JOB_NO = "4334 "
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
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 상 0 / 1 구분
                if c_code == "034" :        # 상 0 / 1 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = -PlasmaP_H + TCPGAP + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       # 피어싱 띄우기
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = 0.0 + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                    cal_rx = Calc_DegreeH
                    cal_rz = H_RZ_2          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = -PlasmaGAP - Margin_Y  
                cal_robz = Margin_Z
                cal_rx = Calc_DegreeH / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_2              # 이동 중간 각도
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
            elif c_code == "211" :                          # 원 중앙 / #Case 12  # 멀티원 중앙

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T >= 9 :
                ##                        Pos_Num = 11:     ReDim MovePos.job1(Pos_Num - 1)
                ##                        ##GJobName = "CCIRCLE9.JBI"       # 직각으로 올라가기
                ##                    else:
                ##                        Pos_Num = 12:     ReDim MovePos.job1(Pos_Num - 1)
                ##                        ##GJobName = "CCIRCLE.JBI"        # 원형으로 올라가기
                ##                    
                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4371 "
                Pos_Num = 13          #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # # 멀티원의 두 번째 원 작업
                # if c_code == "212" and GDblJobExecCode == 1 :
                #     Wval_b = Wval_b + Wval_c
                
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
                cal_roby = Work_H / 2      ##-PlasmaGAP - 50  
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]            # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T >= 9 :
                ##                        # 반복(5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
                ##                        cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        pose_Arr.append(cal_pose)
                ##                    else:

                ##중복 Point 제거 [2021.04.01]
                ## 반복(3,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a / 4
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = ((Wval_b) - (Wval_a / 4)) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #
                #
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                ##                    cal_robx = -PlasmaCutLoss
                ##                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
                ##                    cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
                ##                    cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 + Calc_Deg_A[8]
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Calc_Deg_B[8]) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 + Calc_Deg_B[7]
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - Calc_Deg_A[7]) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss + 0.5) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 - Calc_Deg_A[2]
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) - 0.5 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - Calc_Deg_B[2] + 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점
                #cal_robx = -Wval_a / 2 - 1
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP)
                #cal_roby = (Wval_b - (Wval_a / 2) + 2 + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #============================
                cal_robx = -(Wval_a * 0.75)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = ((Wval_b) - (Wval_a / 4)) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
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

            elif c_code == "213" :                          # 평 타원 중앙
                JOB_NO = "4373 "
                Pos_Num = 13       #17<-12    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_roby = Work_H / 2      ##
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + (Wval_a / 2) - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -(Wval_a + Wval_c) / 2 - 1
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
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

            elif c_code == "214" :                          # 직 타원 중앙
                JOB_NO = "4374 "
                Pos_Num = 13       #17<-12    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 시작 이동 중간점
                cal_robx = -Wval_a / 2
                cal_roby = Work_H / 2      ##
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b - Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                #cal_roby = (Wval_b + Wval_c / 2) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4, )
                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -PlasmaCutLoss - 2
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b - 1) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
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

            elif c_code == "231" :                          # 선1 중앙
                JOB_NO = "4376 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
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

            elif c_code == "232" :                          # 선2 중앙 ~ 선2 S개선 비적용 영역
                JOB_NO = "4377 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Wval_a) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))       #[11.12.19] 수정
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = 0.0
                cal_roby = (Wval_b + Wval_a)
                cal_robz = Margin_Z
                cal_rx = 0.0
                cal_rz = 0.0
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            elif c_code == "233" :                          # 선3 중앙
                JOB_NO = "4378 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b + Wval_c) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))   # +로 수정[11.03.18]
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Wval_c) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))   # +로 수정[11.03.18]
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
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

            elif c_code == "234" :                          # 선4 중앙
                JOB_NO = "4379 "
                Pos_Num = 5

                # 시작 이동 중간점
                cal_roby = Work_H / 2
                cal_robz = Margin_Z
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]        # 피어싱 띄우기
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = 0.0
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a)
                cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                cal_roby = (Wval_b + Wval_c) + (Adj_D_H * (cal_robz / Work_B + Adj_D_Sign))   # +로 수정[11.03.18]
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 중간점
                cal_robx = -(Wval_a)
                cal_roby = (Wval_b - Wval_c)
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
            elif c_code == "301" or c_code == "401" :       # 좌 스닙 하
                JOB_NO = "4301 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "401" :        # 하 3 / 4 구분
                    cal_robx = 0.0
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                    cal_robz = -(Work_B + 1)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -((Wval_b) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a + 1) - PlasmaCutLoss)
                    cal_robz = 1
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "302" or c_code == "402" :       # 좌 각모 하
                JOB_NO = "4302 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 : 
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    # 하 3 / 4 구분
                    if c_code == "402" :        # 하 3 / 4 구분
                        cal_robx = 0.0
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss)
                        cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -(Work_B + 1)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a - Wval_d) - PlasmaCutLoss)
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = 1
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:
                    # 하 3 / 4 구분
                    if c_code == "402" :        # 하 3 / 4 구분
                        cal_robx = 0.0
                        cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_d) - PlasmaCutLoss)
                        cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -((Work_B - Wval_c) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -(Work_B + 1)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -((Wval_b + Wval_d) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_d) - PlasmaCutLoss)
                        cal_robz = -((Wval_b) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = -((Wval_c) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -((Wval_a) - PlasmaCutLoss)
                        cal_robz = 1
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "303" :                          # 좌 사각귀 하

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2
                    Wval_d = Work_T2

                # 사각귀의 2행정 구분 작업 (첫번째)
                if GDblJobExecCode == 0 :                    
                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30]
                        JOB_NO = "4364 "
                        Pos_Num = 10
                    else:
                        JOB_NO = "4303 "
                        Pos_Num = 10

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
                    cal_rz = H_MoveRZ_1              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용

                        #=======================================================================================================
                        #=======================================================================================================

                        # 시작점
                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift
                        cal_robz = -(Work_B + 2)           # 최종 절단은 좀 더 아래로 : 2mm<-1 [13.10.24]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = GES_Angle       #40도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        #                            #종료 중간점 [추가] ~ NO
                        #                            cal_robx = -(Wval_a) + PlasmaCutLoss
                        #                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1          # -1mm 수평 절단 위로
                        #                            cal_roby = Work_H + PlasmaGAP + Margin_Y
                        #                            cal_rx = -Calc_DegreeL
                        #                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        #                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        #                            pose_Arr.append(cal_pose)

                        #=======================================================================================================
                        #=======================================================================================================

                    else:

                        # 시작점
                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a) + PlasmaCutLoss
                        cal_robz = -(Work_B + 1)           # 최종 절단은 좀 더 아래로
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    # 2차 시작점
                    cal_robx = -(Wval_a) + PlasmaCutLoss - GES_Shift + 1.5         #1.5 절단면을 벗어나도록
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_ry = GES_Angle       #S개선:적용=40도/비적용=0도
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 1 + 2        #추가로 2 더
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 각도점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_1              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 대기점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #-------------------------------------------------------------------

                else:    # 사각귀의 2행정 구분 작업 (두번째)
                    JOB_NO = "4362 "
                    Pos_Num = 7

                    # 3차 시작 대기 점 (추가)
                    cal_robx = -(Wval_a / 2)
                    cal_roby = Work_H - (Work_T2 * 3)
                    cal_robz = Margin_Z
                    cal_rz = 10               # RZ : +10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점
                    # [11.11.16] 피어싱 높이로 밖(-2mm)에서 들어오는 1P 추가
                    cal_robx = -(Wval_a) + PlasmaCutLoss + 7    # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign)) + 2      # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = 10               # RZ : +10 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점 실제
                    cal_robx = -(Wval_a) + PlasmaCutLoss + 7    # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))        # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = 10               # RZ : +10 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a / 2)                # 행정의 중간 점까지
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - ((Wval_d + Wval_c) / 2 + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))    # 안쪽으로 더 붙이기
                    cal_ry = -20              # RY : -20
                    cal_rz = 10               # RZ : +10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -Wval_c
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_c + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))        # 안쪽으로 더 붙이기
                    cal_ry = 0.0   # 좌 사각귀는 각도를 푼다 [11.11.17]    #-20              # RY : -20
                    cal_rz = 10               # RZ : +10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 2        # 시작부 더(좌 사각귀 만)
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Work_T2 + Wval_c) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))        # 안쪽으로 더 붙이기
                    cal_ry = 0.0   # 좌 사각귀는 각도를 푼다 [11.11.17]    #-20              # RY : -20
                    cal_rz = 10               # RZ : +10
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H - (Work_T2 + Wval_c) - PlasmaCutLoss           # (T2) * 1.2 삭제
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

            # 중간 가공 : 하 ------------------------------------------------------------
            elif c_code == "311" or c_code == "411" :       # 원 하 / #Case 12  # 멀티원 하

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T2 >= 9 :
                ##                        Pos_Num = 13:     ReDim MovePos.job1(Pos_Num - 1)
                ##                        ##GJobName = "SCIRCLE9.JBI"       # 직각으로 올라가기
                ##                    else:
                ##                        Pos_Num = 14:     ReDim MovePos.job1(Pos_Num - 1)
                ##                        ##GJobName = "SCIRCLE.JBI"        # 원형으로 올라가기
                ##                    
                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                # T와 관계없이 1/4R로 진입 / C-C-C L로 끊어서 간다.
                JOB_NO = "4311 "
                Pos_Num = 15          #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm

                # 하 3 / 4 구분
                if c_code == "311" :        # 하 3 / 4 구분
                    Wval_b = (Work_B - Wval_b)

                # # 멀티원의 두 번째 원 작업
                # if c_code == "312" and GDblJobExecCode == 1 :
                #     Wval_b = Wval_b + Wval_c
                #     # 상 0 / 1 구분
                #     if c_code == "312" :        # 하 3 / 4 구분
                #         Wval_b = (Work_B - Wval_b - Wval_c)
                    
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                cal_rx = -Calc_DegreeL      #+ 8     #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ##                    if Work_T2 >= 9 :
                ##                        # 반복(5,)
                ##                        cal_robx = -Wval_a / 2
                ##                        cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                ##                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                ##                        cal_rx = -Calc_DegreeL
                ##                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                ##                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                        pose_Arr.append(cal_pose)
                ##                    else:        ##if Ang_T2 < 9 :

                ##중복 Point 제거 [2021.04.01]
                ## 반복(3,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
                # 곡면으로 시작점으로 접근점 - MOVE C
                cal_robx = -Wval_a * 0.75
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

                cal_robx = -Wval_a / 2
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)
                #-----------------------------

                ##중복 Point 제거 [2021.04.01]
                ##L로 끊어서 간다.
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)
                ##-----------------------------
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                ##                    cal_robx = -Wval_a + PlasmaCutLoss
                ##                    cal_robz = -(Work_B - Wval_b)
                ##                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                ##                    cal_rx = -Calc_DegreeL
                ##                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)
                ##
                ##                    # 리턴 (5, )
                ##                    cal_robx = -Wval_a / 2
                ##                    cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss)
                ##                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                ##                    cal_rx = -Calc_DegreeL
                ##                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                ##                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                ##                    pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2 - Calc_Deg_A[8]
                cal_robz = -((Work_B - Wval_b) + Calc_Deg_B[8])
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 리턴 (5, ) : -20도
                cal_robx = -Wval_a / 2 - Calc_Deg_B[7]
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_A[7])
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #테스트 추가
                # 리턴 (5, ) : L
                cal_robx = -Wval_a / 2
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + PlasmaCutLoss + 0.5)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                #원래값에서 아래로 3mm->2mm
                cal_robx = -Wval_a / 2 + Calc_Deg_A[2]
                cal_robz = -((Work_B - Wval_b) - Calc_Deg_B[2] + 2) + 0.5
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                #cal_robx = -Wval_a / 2 + 1
                #cal_robz = -((Work_B - Wval_b) - (Wval_a / 2) + 2 + PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #============================
                cal_robx = -(Wval_a / 4)
                cal_robz = -((Work_B - Wval_b) - (Wval_a / 4))
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #============================
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "313" or c_code == "413" :       # 평 타원 하
                JOB_NO = "4313 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 하 3 / 4 구분
                if c_code == "313" :        # 하 3 / 4 구분
                    Wval_b = (Work_B - Wval_b)

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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                cal_rx = -Calc_DegreeL       #+ 8    #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -Wval_a / 2
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Wval_b + (Wval_a / 2) - PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -(Wval_a + Wval_c) + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -((Wval_a / 2) + Wval_c)
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -((Wval_a / 2) + Wval_c)
                #cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4,)
                cal_robx = -(Wval_a + Wval_c) / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -Wval_a / 2 + 1
                cal_robz = -(Work_B - Wval_b - (Wval_a / 2) + PlasmaCutLoss + 2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "314" or c_code == "414" :       # 직 타원 하
                JOB_NO = "4314 "
                Pos_Num = 15       #19<-14    #중복 Point 제거 [2021.04.01]

                # 원형 절단손실L (6T초과의 12파이 이하는 따로...)
                if Work_T2 > 6 and Wval_a <= 12 :       #
                    PlasmaCutLoss = GCircleLoss2 / 2    #1.3mm
                else:
                    PlasmaCutLoss = GCircleLoss / 2     #2mm
                
                # 하 3 / 4 구분
                if c_code == "314" :        # 하 3 / 4 구분
                    Wval_b = (Work_B - Wval_b)
                
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 시작점
                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))     # 피어싱 띄우기
                cal_rx = -Calc_DegreeL                     #+ 8    #원점에서(기울기 각도)       # 면에 수직
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(5,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b - (Wval_a + Wval_c) / 2 + PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(7,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b - Wval_c / 2)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(8,)
                #cal_robx = -PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                cal_robx = -Wval_a / 2
                cal_robz = -(Work_B - Wval_b + (Wval_a + Wval_c) / 2 - PlasmaCutLoss)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                ##중복 Point 제거 [2021.04.01]
                ## 반복(10,)
                #cal_robx = -Wval_a + PlasmaCutLoss
                #cal_robz = -(Work_B - Wval_b + Wval_c / 2)
                #cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                #cal_rx = -Calc_DegreeL
                #cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                #cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                #pose_Arr.append(cal_pose)

                # 리턴 (4,)
                cal_robx = -Wval_a + PlasmaCutLoss
                cal_robz = -(Work_B - Wval_b)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 종료점 추가
                cal_robx = -Wval_a + PlasmaCutLoss + 2
                cal_robz = -(Work_B - Wval_b - 1)
                cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                cal_rx = -Calc_DegreeL
                cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

                ##Case 15  # V 컷팅 하

            elif c_code == "316" or c_code == "416" :       # ㄷ 컷팅 하
                JOB_NO = "4316 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "416" :        # 하 3 / 4 구분
                    cal_robx = -PlasmaCutLoss
                    cal_robz = -(Work_B)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -PlasmaCutLoss
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -((Work_B - Wval_b) + PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -(Work_B + 1)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = -PlasmaCutLoss
                    #cal_robz =0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -PlasmaCutLoss
                    cal_robz = -((Wval_b) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = -((Wval_b) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -((Wval_a) - PlasmaCutLoss)   #/ math.sqrt(2)
                    cal_robz = 1
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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
            elif c_code == "321" or c_code == "421" :       # 우 스닙 하
                JOB_NO = "4301 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "421" :        # 하 3 / 4 구분
                    cal_robz = -(Work_B)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_robz = -((Work_B - (Wval_b + 1)) + PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robz = 0.0
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)         #- PlasmaCutLoss      #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                    cal_robz = -(((Wval_b + 1)) - PlasmaCutLoss)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "322" or c_code == "422" :       # 우 각모 하
                JOB_NO = "4302 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 오류 방지
                if Wval_c == 0 : 
                    Wval_c = Wval_b
                    Wval_d = 0

                if Wval_d >= 500 :     # 사선형 각모
                    Wval_d = Wval_d - 500

                    # 하 3 / 4 구분
                    if c_code == "422" :        # 하 3 / 4 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_d)     # 수정 [11.11.29]       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Work_B - (Wval_c)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Work_B - (Wval_b)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = 0
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(((Wval_c)) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(((Wval_b)) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:
                    # 하 3 / 4 구분
                    if c_code == "422" :        # 하 3 / 4 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -((Work_B - (Wval_c)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Work_B - (Wval_b)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -((Work_B - (Wval_b + Wval_d)) + PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(((Wval_c)) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a - Wval_d)       #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(((Wval_b)) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = -(Wval_a)         #- PlasmaCutLoss       #(Wval_a + 1)를 조금 작게 - 다음 모재에 흔적이 남는다.
                        cal_robz = -(((Wval_b + Wval_d)) - PlasmaCutLoss)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "323" :                          # 우 사각귀 하

                if Wval_d == 0 :      # 이전 버전의 값에 대한 보정 [11.06.10] <- 입력 상수값 조정 가능으로 변경
                    Wval_c = Work_T2
                    Wval_d = Work_T2

                # 사각귀의 2행정 구분 작업 (첫번째)
                if GDblJobExecCode == 0 :
                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30]
                        JOB_NO = "4365 "
                        Pos_Num = 13
                    else:
                        JOB_NO = "4361 "
                        Pos_Num = 12

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
                    cal_rz = H_MoveRZ_1              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 0차 시작점
                    cal_robx = -(Wval_a)
                    cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B + 1)           # 최종 절단은 좀 더 아래로
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    if GES_Use :     #사각귀 S개선 적용/비적용[13.05.30] ~ GES_Angle(RY),GES_Shift(Rob_X) 적용

                        #=======================================================================================================
                        #=======================================================================================================

                        #시작 중간점 [추가]
                        cal_robx = 0 + GES_Shift
                        cal_roby = Work_H + PlasmaGAP + Margin_Y           #Y+50위치
                        cal_robz = 0.0
                        cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                        cal_rz = H_MoveRZ_1              # 이동 중간 각도
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        # 1차 시작점
                        cal_robx = 0 + GES_Shift
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0 + GES_Shift
                        cal_robz = -(Work_B + 2)           # 최종 절단은 좀 더 아래로 : 2mm<-1 [13.10.24]
                        cal_roby = Work_H + (GES_Adjust + PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = -GES_Angle      #40도(-)
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        #                            #종료 중간점 [추가] ~ NO
                        #                            #cal_robx = 0
                        #                            cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1          # -1mm 수평 절단 위로
                        #                            cal_roby = Work_H + PlasmaGAP + Margin_Y
                        #                            cal_rx = -Calc_DegreeL
                        #                            cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        #                            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        #                            pose_Arr.append(cal_pose)

                        #=======================================================================================================
                        #=======================================================================================================

                    else:

                        # 1차 시작점
                        cal_robx = 0.0
                        cal_robz = 0.0     ## -3 : 절단 부분 좀 더 보정(잘 안 잘림)
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로 ~> 옆면은 -2mm 더=>-3mm[11.11.15]
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B + 1)           # 최종 절단은 좀 더 아래로
                        cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    # 2차 시작점
                    cal_robx = GES_Shift - 1.5           #1.5 절단면을 벗어나도록
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_ry = -GES_Angle      #S개선:적용=40도/비적용=0도(-)
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 1 + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]          # -1mm 수평 절단 위로
                    cal_roby = Work_H + (PlasmaGAP - TCPGAP) + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 각도점 (& 이전은 시작 이동 중간점과 동일)
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                    cal_rz = H_MoveRZ_1              # 이동 중간 각도
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 동작 중간 대기점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #-------------------------------------------------------------------

                else:    # 사각귀의 2행정 구분 작업 (두번째)
                    JOB_NO = "4362 "
                    Pos_Num = 7

                    # 3차 시작 대기 점 (추가)
                    cal_robx = -(Wval_a / 2)
                    cal_roby = Work_H - (Work_T2 * 3)
                    cal_robz = Margin_Z
                    cal_rz = 45               # RZ : +45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점
                    # [11.11.16] 피어싱 높이로 밖(-2mm)에서 들어오는 1P 추가
                    cal_robx = -6     # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaP_H - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign)) + 2       # 안쪽으로 더 붙이기
                    cal_ry = 15                       # RY : +15 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = 45                       # RX : +45 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 3차 시작점 실제
                    cal_robx = -6     # : 부딪치지 않는 부분까정
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_d + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))         # 안쪽으로 더 붙이기
                    cal_ry = 15                       # RY : +15 값을 앞쪽으로 기울여서 간섭을 피한다.
                    cal_rz = 45                       # RX : +45 값을 안쪽으로 돌려서 간섭을 피한다.
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a / 2)                # 행정의 중간 점까지
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - ((Wval_d + Wval_c) / 2 + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))    # 안쪽으로 더 붙이기
                    cal_ry = 0.0
                    cal_rz = 45               # RZ : +45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a - Wval_c * 1.2)
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Wval_c + GEdgeAdd) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))        # 안쪽으로 더 붙이기
                    cal_ry = -20   # 우 사각귀는 각도를 더 준다 [11.11.17]    #-15              # RY : -15
                    cal_rz = 45               # RZ : +45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Work_T) / 2 + (PlasmaGAP - TCPGAP) + GBeamAdjustMH     #중간 높이 보정값 [16.12.28]
                    cal_roby = Work_H - (Work_T2 + Wval_c) - PlasmaCutLoss + 1 + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))        # 안쪽으로 더 붙이기
                    cal_ry = -20   # 우 사각귀는 각도를 더 준다 [11.11.17]    #-15              # RY : -15
                    cal_rz = 45               # RZ : +45
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # 복귀 이동 중간점
                    cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                    cal_roby = 50          # 안쪽으로....
                    cal_robz = Margin_Z
                    cal_rx = 0.0
                    cal_ry = 0.0
                    cal_rz = 0.0
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    # 우 사각귀 하(2) 수직 절단 보상용
                    ##GE_CutLast = GE_CutLast + 2
                    GH_REdge_Down = 2
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++

            # 선1,2,3,4 : 하 ------------------------------------------------------------

            elif c_code == "331" or c_code == "431" :       # 선1 하
                JOB_NO = "4331 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "431" :        # 하 3 / 4 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b)
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "332" or c_code == "432" :       # 선2 하

                if Wval_d < 100 :   #일반
                    JOB_NO = "4332 "
                    Pos_Num = 7
                else:
                    if Wval_b < (Work_B / 2 - Work_T2) and (Wval_a - Wval_b) > (Work_B / 2 + Work_T2) :    #T포함의 경우
                        JOB_NO = "4366 "
                        Pos_Num = 8
                    else:
                        JOB_NO = "4367 "
                        Pos_Num = 6
                    
                    #개선 각도와 이동량 계산 ~ 높이 보정값(1.5mm) 추가 [13.09.07]
                    if Wval_d > 200 :     #우 S개선
                        Wval_d = -(Wval_d - 200)      #-30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) *  round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Wval_c = -PlasmaCutLoss + (float(Work_T2) + GES_Adjust) * math.tan(float(-Wval_d) *  round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산
                    else:        #좌 S개선
                        Wval_d = Wval_d - 100         #30도
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        #S개선의 높이에 대한 방식 변경 ~ 팁의 높이를 GPlasmaGap으로 맞추고~> 편차값을 Gap에 적용[14.01.23]
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GES_Adjust = GPlasmaGap - (math.sqrt(GPlasmaGap ^ 2 + GES_TIP_R ^ 2) * math.sin((90 - abs(Wval_d) - math.atan(GES_TIP_R / GPlasmaGap) / math.pi * 180) *  round(math.pi / 180, 9)))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        Wval_c = PlasmaCutLoss - (float(Work_T2) + GES_Adjust) * math.tan(float(Wval_d) *  round(math.pi / 180, 9)) #T2에 따른 개선의 Shift값 계산

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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                if Wval_d == 0 :   #일반

                    # 하 3 / 4 구분
                    if c_code == "432" :        # 하 3 / 4 구분
                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b)
                        cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Work_B - Wval_b - Wval_a)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                    else:
                        cal_robx = 0.0
                        cal_robz = -(Wval_b)
                        cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Wval_b)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = 0.0
                        cal_robz = -(Wval_b + Wval_a)
                        cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                else:    #선2 S개선 하
                    cal_robx = Wval_c
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기~>일반 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_ry = Wval_d       #30도/-30도
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    # T의 중간 부분
                    if Wval_b < (Work_B / 2 - Work_T2) and (Wval_a - Wval_b) > (Work_B / 2 + Work_T2) :   #T포함의 경우
                        cal_robx = Wval_c
                        cal_robz = -(Work_B + Work_T * 1.3) / 2 - PlasmaCutLoss
                        cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = Wval_d       #30도/-30도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)

                        cal_robx = Wval_c
                        cal_robz = -(Work_B - Work_T * 1.3) / 2 + PlasmaCutLoss + 3
                        cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                        cal_rx = -Calc_DegreeL
                        cal_ry = Wval_d       #30도/-30도
                        cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                        cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                        pose_Arr.append(cal_pose)
                    
                    cal_robx = Wval_c
                    if (Work_B - Wval_b - Wval_a) <= 0 :
                        cal_robz = -(Work_B - Wval_b - Wval_a - 2)   #2mm 더 위로 절단 추가 [13.10.24]
                    else:
                        cal_robz = -(Work_B - Wval_b - Wval_a)
                    
                    cal_roby = Work_H + GES_Adjust + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_ry = Wval_d       #30도/-30도
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_ry = 0.0
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "333" or c_code == "433" :       # 선3 하
                JOB_NO = "4333 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "433" :        # 하 3 / 4 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

            elif c_code == "334" or c_code == "434" :       # 선4 하
                JOB_NO = "4334 "
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
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

                # 하 3 / 4 구분
                if c_code == "434" :        # 하 3 / 4 구분
                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Work_B - Wval_b - Wval_c)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Work_B - Wval_b)
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                else:
                    cal_robx = 0.0
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaP_H - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))       # 피어싱 띄우기
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = 0.0
                    cal_robz = -(Wval_b)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                    cal_robx = -(Wval_a)
                    cal_robz = -(Wval_b + Wval_c)     # [11.03.18] 수정
                    cal_roby = Work_H + PlasmaGAP - TCPGAP + (Adj_C_L * (cal_robz / Work_B + Adj_C_Sign))
                    cal_rx = -Calc_DegreeL
                    cal_rz = H_RZ_1          # 옆면 가공 로봇 자세 설정값
                    cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                    pose_Arr.append(cal_pose)

                # 복귀 이동 각도점
                cal_robx = SideRZADJ       # 로봇 옆면 가공 중간 이동 보정 X값
                cal_roby = Work_H + PlasmaGAP + Margin_Y        #Y+50위치
                cal_robz = Margin_Z
                cal_rx = -Calc_DegreeL / 2        # 이동 중간 각도
                cal_rz = H_MoveRZ_1              # 이동 중간 각도
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

                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        pose_Arr.insert(0, "JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7))        #첫번째에 구분자,번호,P수를 전달  
    except:
        pose_Arr = ["Error Return"]

    return pose_Arr

