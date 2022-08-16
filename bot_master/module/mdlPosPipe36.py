import math
import json


    # # HP6
    # # 최종 리턴에서 str(roune(????, 3)).zfill(8) + ' '
    # return_arr.append("JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7) + ' ' + func_Set_Vel(Work_T))           #7자리
    # for pose_buf in return_buf:         # 기준값 적용 및 로봇 자세 변환
    #     a1 = str(round(pose_buf[0] + stan_pos[0], 3)).zfill(8) + ' '
    #     a2 = str(round(pose_buf[1] + stan_pos[1], 3)).zfill(8) + ' '
    #     a3 = str(round(pose_buf[2] + stan_pos[2], 3)).zfill(8) + ' '
    #     a4 = str(round(pose_buf[3] + stan_pos[3], 3)).zfill(8) + ' '
    #     a5 = str(round(pose_buf[4] + stan_pos[4], 3)).zfill(8) + ' '
    #     a6 = str(round(pose_buf[5] + stan_pos[5], 3)).zfill(8)     # 로봇 자세값은 기준값에서 얻는다!
    #     return_arr.append(a1 + a2 + a3 + a4 + a5 + a6)

    # return return_arr


def func_pipe36_pose(DLL_VAL, GEdgeAdd):          # GEdgeAdd : 전체 형식을 맞추기 위해 ...

    global JOB_NO
    global Pos_Num

    #===================================================================
    # "SEND", "0.0,0.0,500.0,180.0,0.0,-180.0$PI 100A-114.3 SCH40-6T$294,PI040,0,0,0,0,0$0 등

    VAL_buf = str(DLL_VAL).split('$')

    Size_buf = VAL_buf[1].split(' ')
    Size_buf2 = Size_buf[1].split('-')    
    WORK_R = float(Size_buf2[1])    
    Size_buf2 = Size_buf[2].split('-')
    Work_T = float(Size_buf2[1].replace('T',''))

    WorkCode = str(VAL_buf[2]).split(',')       # ~> ["294","PI040","0","0","0","0","0"]
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
    GPipeAdj_End = 1        # 파이프 절단에 따른 종단 접점 부분 보정 2mm 
    #===================================================================

    GCutLoss = 3            # 절단손실:고정값

    P_DegreeRX_1=[]                # RX_1 각도 변화량 : 36<-18
    P_DegreeRX_2=[]                # RX_2 각도 변화량 : 36<-18
    P_DegreeRX_1 = [0 for i in range(37)]   #0~36
    P_DegreeRX_2 = [0 for i in range(37)]

    P_DegreeRZ_1S = 0.0             # RZ_1 각도 시작 기본값(X:0 - 원점 위치)
    P_DegreeRZ_1E = 0.0             # RZ_1 각도 종료 기본값(X:250 - 가공최대 거리 to 원점)
    Calc_P_RZ1 = 0.0                # RZ_1의 X 변화에 따른 각도 변화량

    P_DegreeRZ_2 = 0.0              # RZ_2 각도 기본값

    DIV_DEGREE = 5         # 각도 분할 구분(5<-10) : 36등분*2
    DIV_NUM = 36           # 36 = 18*2

    Calc_Deg = 0.0              # 설정 각도값 계산
    Calc_Deg_Buf = 0.0          # 설정 각도값 계산용
    Calc_Cen = 0.0              # 계산용
    Calc_Buf = 0.0              # 계산용

    Cal_T_Buf = 0.0             # 계산용 ~ 반지름
    Cal_IN_Buf = 0.0            # 계산용 ~ 반지름
    Cal_OUT_Buf = 0.0           # 계산용 ~ 반지름

    Calc_INx=[]                 # 반지름 * math.cos d, d:0~180도 의 변화량 값(robx)
    Calc_OUTy=[]                # 반지름 * math.cos d, d:-90~90도 의 변화량 값(roby)
    Calc_OUTz=[]                # 반지름 * math.cos d, d:0~180도 의 변화량 값(robz)
    Calc_INx = [0 for i in range(37)]
    Calc_OUTy = [0 for i in range(37)]
    Calc_OUTz = [0 for i in range(37)]

    Round_T=[]                  # 지주쪽에 대한 반지름
    Round_Rou=[]                # 지주쪽에 대한 원 변화량
    Round_T = [0 for i in range(37)]
    Round_Rou = [0 for i in range(37)]

    P_RXDegree = 0.0            # 기울임 각도값 : Wval_d ~ 작업후에 적용 예정  
    P_RZ = 0                    # 옆면 가공 로봇 자세 설정값(<-상수D 값에 의함)

    CodeDeg = 0      # 상/하 = 0/180

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # RX_1 / RX_2 각도 변화량
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for p in range(28):     #0~27
        P_DegreeRX_1[p] = -(DIV_DEGREE * p)      # RX_1 각도 변화량
        P_DegreeRX_2[p] = (DIV_DEGREE * p)       # RX_2 각도 변화량
    
    for p in range(28, (DIV_NUM+1)):    #28 To DIV_NUM    #36
        P_DegreeRX_1[p] = -135      # RX_1 각도 변화량 (<- -139)
        P_DegreeRX_2[p] = 135       # RX_2 각도 변화량        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    if WORK_R > 260 :        #8호기 250A(267.4mm) [12.03.05] 추가
        #************************************************************************************
        P_DegreeRZ_1S = 50
        P_DegreeRZ_1E = 50
        Calc_P_RZ1 = 0
        P_DegreeRZ_2 = -56      #<~ -57 : [13.07.29] 수정
        #************************************************************************************
    # elif GR_Divide >= 8 :      # 작업 8호기 구분 안함
    #     #************************************************************************************
    #     # ((8호기 이상)) 일반대신 - 파이프는 65A 이하 // 그 이상으로 턴 각도 구분 [09.04.29]
    #     #************************************************************************************
    #     if WORK_R <= 76.3 :       # 50A(60.5), 65A(76.3)
    #         P_DegreeRZ_1S = 36
    #         P_DegreeRZ_1E = 36
    #         Calc_P_RZ1 = 0
    #         P_DegreeRZ_2 = -36
    #     else :
    #         P_DegreeRZ_1S = 40
    #         P_DegreeRZ_1E = 40
    #         Calc_P_RZ1 = 0
    #         P_DegreeRZ_2 = -40
    #     #************************************************************************************
    else :
        #***************************************************************
        # 일반
        #***************************************************************
        if WORK_R <= 76.3 :       # 50A(60.5), 65A(76.3)
            P_DegreeRZ_1S = 45
            P_DegreeRZ_1E = 70
            Calc_P_RZ1 = (P_DegreeRZ_1E - P_DegreeRZ_1S) / 250
            P_DegreeRZ_2 = -50
        else :
            # RZ_1 각도 기본값
            P_DegreeRZ_1S = 50           # -> 찾은값(-50.02)    <== X값에 대응하여 가변 : 0위치
            P_DegreeRZ_1E = 75.5           # -> 찾은값(-75.49)    <== X값에 대응하여 가변 : 250위치

            # RZ_1의 X 변화에 따른 각도 변화량
            Calc_P_RZ1 = (P_DegreeRZ_1E - P_DegreeRZ_1S) / 250
            # (MovePos(, 0) * Calc_P_RZ1)   # X 값에 비례하여 보정

            # RZ_2 각도 기본값
            P_DegreeRZ_2 = -60          # -> 찾은값(65.94) (2차 80A가 안된다:63)(3차 50A가 안된다:60)
        
        #***************************************************************
    

    # 자재 실제 크기 보정 ~ 인자값 전달에서 이미 계산 안됨
    WORK_R = WORK_R + GSizeAdjustA
    

    GPlasmaGap = 6      # 플라즈마 GAP
    PlasmaGAP = GPlasmaGap
    TCPGAP = 6

    GPlasmaP_H = 9      #피어싱 띄우기 높이
    PlasmaP_H = 9       #피어싱 띄우기 높이


    if GDblJobExecCode == 0 :
        P_RXDegree = Wval_d     # 기울임 각도값(엇각)
    else :
        P_RXDegree = -Wval_d     # 기울임 각도값(엇각)

    ## 임시 : 강제 설정 ==> 테스트 후에 적용할 것이므로....
    P_RXDegree = 0
    
    #+++++++++++++++++++++++++++++++++++++++++++++++
    # 옆면 가공 로봇 자세 설정값(<-상수D 값에 의함)
    #+++++++++++++++++++++++++++++++++++++++++++++++
    if Wval_d > 0 :
        P_RZ = 45
    elif Wval_d < 0 :
        P_RZ = -45
    else :
        P_RZ = 0
    #+++++++++++++++++++++++++++++++++++++++++++++++

    #프라즈마 절단 Loss
    PlasmaCutLoss = GCutLoss / 2

    # 시작/복귀점에 대한 Y,Z 여유값(기본:50mm)
    Margin_Z = 50       # 시작/복귀점에 대한 Z 여유값(기본:50mm) : 파이프는 Y는 비사용, Z만 적용


    pose_Arr=[]     #빈 리스트 생성

    cal_robx = 0.0
    cal_roby = 0.0
    cal_robz = 0.0
    cal_rx = 0.0
    cal_ry = 0.0
    cal_rz = 0.0

    Pos_Num = 4 + (DIV_NUM * 1)     # 4+36=4+(18*2) : 공통으로 P 수량 및 저장용 버퍼 설정

    try:

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # 원형 두께에 대한 보정값 계산 [11.05.16]
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        Cal_T_Buf = (WORK_R / 2) - Work_T           # 접합면에 대한 실제 닫는 부위는 두께를 뺀 내접원이다.(두께 보정)
        Cal_IN_Buf = (WORK_R / 2)                           # 원 자재 외경에 대한 (X축)
        Cal_OUT_Buf = (WORK_R / 2) + (PlasmaGAP - TCPGAP)       #  반지름 + (플라즈마GAP-TCPGAP:2mm만큼 더 큰 원으로 돈다.) = 실제는 플라즈마 GAP 만큼 큰 원으로 돈다

        Calc_Cen = (WORK_R / 2)        # 기준점에서 Z축 중심점까지의 거리

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # 가공 형태 코드 ~ robx 구하기
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if c_code == "040":         # 수직절단
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            Calc_P_RZ1 = 0      # 수직절단에서는 0

            for p in range(DIV_NUM+1):      #0~36 : For p = 0 To DIV_NUM    #36
                Calc_INx[p] = 0

        elif c_code == "041":       # 좌면각상
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 0
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                # Calc_INx[p] = (Calc_Cen + (IIf(Calc_Buf < 0, Cal_T_Buf, Cal_IN_Buf) * Calc_Buf)) / Calc_Deg
                if Calc_Buf < 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf)) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf)) / Calc_Deg

        elif c_code == "042":       # 좌면각하
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 180
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf < 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf)) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf)) / Calc_Deg

        elif c_code == "043":       # 좌원수직 ~ 수정됨 => [11.10.26] 재수정
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)

            # ###            CodeDeg = 0
            # ###            for p in range(DIV_NUM+1):      #0~36
            # ###                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
            # ###                Round_Rou[p] = -(Cal_T_Buf * Calc_Buf)     # 우원수직과는 이곳만 다르다
            # ###            #--------------------------------------------------
            # ###                if (Work_Lenth - Round_Rou[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
            # ###                    Calc_INx[p] = Work_Lenth
            # ###                else :
            # ###                    Calc_INx[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_Rou[p] ^ 2))
            # ###                
            # ###            

            CodeDeg = 180       # [11.10.26] 재수정
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_Rou[p] = -(Cal_T_Buf * Calc_Buf)    # 우원수직과는 이곳만 다르다
                #--------------------------------------------------
                if (Work_Lenth - Round_Rou[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Calc_INx[p] = Work_Lenth
                else :
                    Calc_INx[p] = (math.sqrt(Work_Lenth ^ 2 - Round_Rou[p] ^ 2)) - (math.sqrt(Work_Lenth ^ 2 - Cal_T_Buf ^ 2))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_INx[0]) * Calc_P_RZ1

        elif c_code == "044":       # 좌원각상
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)  # 임시 변수로 사용
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))
            Calc_Deg_Buf = math.cos(Wval_a *  round(math.pi / 180, 9))    # 먼저 변수로 사용(지주쪽 원형 보정)

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 0
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_T[p] = (Cal_T_Buf * Calc_Buf)

                if (Work_Lenth - Round_T[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Round_Rou[p] = Work_Lenth / Calc_Deg_Buf
                else :
                    Round_Rou[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_T[p] ^ 2)) / Calc_Deg_Buf
                

                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf < 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf) - Round_Rou[p]) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf) - Round_Rou[p]) / Calc_Deg

        elif c_code == "045":       # 좌원각하
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)  # 임시 변수로 사용
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))
            Calc_Deg_Buf = math.cos(Wval_a *  round(math.pi / 180, 9))    # 먼저 변수로 사용(지주쪽 원형 보정)

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 180
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_T[p] = (Cal_T_Buf * Calc_Buf)

                if (Work_Lenth - Round_T[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Round_Rou[p] = Work_Lenth / Calc_Deg_Buf
                else :
                    Round_Rou[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_T[p] ^ 2)) / Calc_Deg_Buf
                
                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf < 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf) - Round_Rou[p]) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf) - Round_Rou[p]) / Calc_Deg
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        elif c_code == "051":       # 우면각상
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 180
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf >= 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf)) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf)) / Calc_Deg

        elif c_code == "052":       # 우면각하
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 0
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf >= 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf)) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf)) / Calc_Deg

        elif c_code == "053":       # 우원수직
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)

            CodeDeg = 0
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_Rou[p] = (Cal_T_Buf * Calc_Buf)               # 좌원수직과는 이곳만 다르다
                #--------------------------------------------------
                if (Work_Lenth - Round_Rou[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Calc_INx[p] = Work_Lenth
                else :
                    Calc_INx[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_Rou[p] ^ 2))

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_INx[18]) * Calc_P_RZ1

        elif c_code == "054":       # 우원각상
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)  # 임시 변수로 사용
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))
            Calc_Deg_Buf = math.cos(Wval_a *  round(math.pi / 180, 9))    # 먼저 변수로 사용(지주쪽 원형 보정)

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 180
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_T[p] = -(Cal_T_Buf * Calc_Buf)

                if (Work_Lenth - Round_T[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Round_Rou[p] = Work_Lenth / Calc_Deg_Buf
                else :
                    Round_Rou[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_T[p] ^ 2)) / Calc_Deg_Buf
                

                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf >= 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf) + Round_Rou[p]) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf) + Round_Rou[p]) / Calc_Deg

        elif c_code == "055":       # 우원각하
            #__________________________________________________________________________________________________________________
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 지주쪽 반지름 R
            Work_Lenth = (Wval_c / 2)  # 임시 변수로 사용
            # X축에 대한 Tan각도값  : Z축 변화량에 따른....
            Calc_Deg = math.tan((Wval_a) *  round(math.pi / 180, 9))
            Calc_Deg_Buf = math.cos(Wval_a *  round(math.pi / 180, 9))    # 먼저 변수로 사용(지주쪽 원형 보정)

            # X 길이에 대한 각 크기
            P_DegreeRZ_1S = P_DegreeRZ_1S + (Calc_Cen + (WORK_R / 2)) / Calc_Deg * Calc_P_RZ1

            CodeDeg = 0
            for p in range(DIV_NUM+1):      #0~36
                Calc_Buf = math.cos((DIV_DEGREE * p - 90 + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                Round_T[p] = -(Cal_T_Buf * Calc_Buf)

                if (Work_Lenth - Round_T[p]) < 0 :   # 절단과 지주쪽이 같은 크기 일 때...?!
                    Round_Rou[p] = Work_Lenth / Calc_Deg_Buf
                else :
                    Round_Rou[p] = (Work_Lenth - math.sqrt(Work_Lenth ^ 2 - Round_T[p] ^ 2)) / Calc_Deg_Buf

                Calc_Buf = math.cos((DIV_DEGREE * p + CodeDeg + P_RXDegree) *  round(math.pi / 180, 9))
                if Calc_Buf >= 0 :
                    Calc_INx[p] = (Calc_Cen + (Cal_T_Buf * Calc_Buf) + Round_Rou[p]) / Calc_Deg
                else :
                    Calc_INx[p] = (Calc_Cen + (Cal_IN_Buf * Calc_Buf) + Round_Rou[p]) / Calc_Deg

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # 전체 공통 ~ roby, robz 구하기
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        for p in range(DIV_NUM+1):      #0~36
            Calc_OUTy[p] = Cal_OUT_Buf * math.cos((DIV_DEGREE * p - 90) *  round(math.pi / 180, 9))
            Calc_OUTz[p] = Calc_Cen + (Cal_OUT_Buf * math.cos((DIV_DEGREE * p) *  round(math.pi / 180, 9)))
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # 코드 2행정 실행
        if GDblJobExecCode == 0 :
            JOB_NO = "4501 "

            # 시작 이동 중간점1
            cal_robx = -Calc_INx[0]
            cal_roby = (WORK_R / 2 + 50)      #Y+(반지름+50)위치
            cal_robz = Margin_Z
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 시작 이동 중간점2
            cal_robx = -Calc_INx[0]
            cal_roby = (WORK_R / 2 + 50)      #Y+(반지름+50)위치
            cal_robz = -(WORK_R + (PlasmaP_H - (PlasmaGAP - TCPGAP)))          # 피어싱 띄우기
            cal_rx = -90
            cal_rz = 30      # 시작 접근 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            ################################################################

            #-----------------------------------
            cal_robx = -Calc_INx[0]
            # PlasmaGAP : 하부로 45도로 접근 했으므로 그 만큼 빼줘야 실제 원형의 하부 중앙점이 된다.
            cal_roby = Calc_OUTy[DIV_NUM] + 0    ## 보정 없이 피어싱과 같이 사용    #PlasmaGAP / math.sqrt(2)       # 하부 45도 접근 보상(PlasmaGAP/ math.sqrt(2))
            cal_robz = -Calc_OUTz[0]
            cal_rx = P_DegreeRX_1[DIV_NUM]
            cal_rz = P_DegreeRZ_1S + (cal_robx * Calc_P_RZ1)   # X값은 0이므로 각도 추가 보정 없다.                # 로봇 팔 간섭 피하기
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)
            #-----------------------------------

            for p in range(1, DIV_NUM):      #1~35 : For p = 1 To DIV_NUM - 1
                cal_robx = -Calc_INx[p]
                cal_roby = Calc_OUTy[DIV_NUM - p]
                cal_robz = -Calc_OUTz[p]
                cal_rx = P_DegreeRX_1[DIV_NUM - p]
                cal_rz = P_DegreeRZ_1S + (cal_robx * Calc_P_RZ1)                # 로봇 팔 간섭 피하기
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            #-----------------------------------
            cal_robx = -Calc_INx[DIV_NUM]   ##-0.7     # 수직 특수 보정 0.5
            cal_roby = Calc_OUTy[0] - GPipeAdj_End      # 종단 부분 겹치게 보정[2008.01.14]
            cal_robz = -Calc_OUTz[DIV_NUM]
            cal_rx = P_DegreeRX_1[0]      # 0도
            cal_rz = P_DegreeRZ_1S + (cal_robx * Calc_P_RZ1)
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            ################################################################

            # 추가 중심 복귀점(끝단 가공시의 핸드 전진 피하기-작은 자재) : 자재의 중심 기준점으로 이동
            cal_robx = -Calc_INx[0]
            cal_roby = 0
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)            
            pose_Arr.append(cal_pose)

        else :
            JOB_NO = "4502 "

            # 시작 이동 중간점1
            cal_robx = -Calc_INx[0]
            cal_roby = -(WORK_R / 2 + 50)      #Y-(반지름+50)위치
            cal_robz = Margin_Z
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            # 시작 이동 중간점2
            cal_robx = -Calc_INx[0]
            cal_roby = -(WORK_R / 2 + 50)      #Y-(반지름+50)위치
            cal_robz = -(WORK_R + (PlasmaP_H - (PlasmaGAP - TCPGAP)))        # 피어싱 띄우기만큼 띄운다.
            cal_rx = 90
            cal_rz = -30        # 시작 접근 각도
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            ################################################################

            #-----------------------------------
            cal_robx = -Calc_INx[0]      ##1.5     # 2 로봇 행정 강제 보정(1.5->0) 안함
            # (PlasmaGAP / 2) : 하부로 45도로 접근 했으므로 그 만큼 빼줘야 실제 원형의 하부 중앙점이 되지만 끝이므로 살짝 중복되게....
            cal_roby = -Calc_OUTy[DIV_NUM] - 3   #- 0    ## 보정 안함 : #(PlasmaGAP / 2)        # 하부 45도 접근 보상(/2)
            cal_robz = -Calc_OUTz[0]
            cal_rx = P_DegreeRX_2[DIV_NUM]
            cal_rz = P_DegreeRZ_2
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)
            #-----------------------------------

            for p in range(1, DIV_NUM):      #1~35 : For p = 1 To DIV_NUM - 1
                cal_robx = -Calc_INx[p]
                cal_roby = -Calc_OUTy[DIV_NUM - p]
                cal_robz = -Calc_OUTz[p]
                cal_rx = P_DegreeRX_2[DIV_NUM - p]
                cal_rz = P_DegreeRZ_2
                cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
                pose_Arr.append(cal_pose)

            #-----------------------------------
            cal_robx = -Calc_INx[DIV_NUM]   ##-0.7     # 수직 특수 보정 0.5
            cal_roby = -Calc_OUTy[0] + GPipeAdj_End      # 종단 부분 겹치게 보정[2008.01.14]
            cal_robz = -Calc_OUTz[DIV_NUM]
            cal_rx = P_DegreeRX_2[0]
            cal_rz = P_DegreeRZ_2
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)

            ################################################################

            # 추가 중심 복귀점(끝단 가공시의 핸드 전진 피하기-작은 자재) : 자재의 중심 기준점으로 이동
            cal_robx = -Calc_INx[0]
            cal_roby = 0
            cal_robz = Margin_Z
            cal_rx = 0.0
            cal_rz = 0.0
            cal_pose = (cal_robx, cal_roby, cal_robz, cal_rx, cal_ry, cal_rz)
            pose_Arr.append(cal_pose)
        
        pose_Arr.insert(0, "JOBMAKE_RES= 000" + JOB_NO + str(Pos_Num).zfill(7))        #첫번째에 구분자,번호,P수를 전달  
    except:
        pose_Arr = ["Error Return"]

    return pose_Arr


