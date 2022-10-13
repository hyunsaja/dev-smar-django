import math
import json


# 함수 구분 호출
def rpcm_Func(f_cmd, f_val):
    if f_cmd == "CALCREALLENTH":
        return CalcRealLenth(f_val)     # 리턴 : OK,로봇가공거리,콘베어이동거리,배출핸드Blank영역
    else:
        return 'NG,error cmd none'


# =================================================================================
# =================================================================================

# GworkPoint = 0
# RBeforeCode = f_WorkProcess.dgvWorkNow.Rows[GworkRow].Cells[GworkPoint + 14 - 1].Value.ToString().Substring(1, 2)
# RAfterCode = f_WorkProcess.dgvWorkNow.Rows[GworkRow].Cells[GworkPoint + 14 + 1].Value.ToString().Substring(1, 2)
# RLenCode, RBeforeCode, RAfterCode,GA_LenthCalc  //

# EA 50*50*6T$294,EA015,90,43,0,0,12
# GRobotLen 계산 : 실제 로봇 가공 거리(Z축 값) <~~ 가공 원점에서 시작 되도록...
def CalcRealLenth(F_Val):        # GVCutTAdj, GVCutGapAdj, PIPESTART, GTubeMargin

    try:

        # 전달 변수
        # ===========================================================================
        
        val_buf = F_Val.split('$')
        sizekind = val_buf[0][0:2]     # 자재 구분 : EA UA CH IB HB PI SP

        if sizekind == 'EA' or sizekind == 'SP':
            Size_buf = val_buf[0][3:]               # 'EA ', 'UA ' 제거
            Size_buf = Size_buf.split('*')
            Work_S = float(Size_buf[0])
            Work_L = float(Size_buf[1])
            Work_T1 = float(Size_buf[2].replace('T',''))
            Work_T2 = Work_T1
        elif sizekind == 'PI':
            Size_buf = val_buf[0].split(' ')
            Size_buf2 = Size_buf[1].split('-')    
            Work_S = float(Size_buf2[1])            # <~ WORK_R
            Size_buf2 = Size_buf[2].split('-')
            Work_T1 = float(Size_buf2[1].replace('T',''))
        else:       # UA CH IB HB
            Size_buf = val_buf[0][3:]
            Size_buf2 = Size_buf.split('/')
            Size_buf = Size_buf2[0].split('*')
            Work_S = float(Size_buf[0])
            Work_L = float(Size_buf[1])
            Work_T1 = float(Size_buf[2])
            Work_T2 = float(Size_buf2[1].replace('T',''))

        Work_Code = str(val_buf[1]).split(',')         # ~> ["294","EA015","90","43","0","0","12"]    
        c_code = int(Work_Code[1][2:])                 # 자재 구분 제거 한 두자리 코드 <~ 가공코드(Work_Code[1] = RLenCode)

        Cons_a = float(Work_Code[2])
        Cons_b = float(Work_Code[3])
        Cons_c = float(Work_Code[4])
        Cons_d = float(Work_Code[5])
        Cons_Lenth = float(Work_Code[0])

        # 길이차감값
        if len(Work_Code) > 6:
            LenAdd = float(Work_Code[6])
        else:
            LenAdd = 0

        GVCutTAdj = float(val_buf[2])     #1
        GVCutGapAdj = float(val_buf[3])     #0

        PIPESTART = int(val_buf[4])     #100
        GTubeMargin = int(val_buf[5])     #10

        # GDblJobExecCode = int(val_buf[6])     #0      # 비사용

        # ===========================================================================
        GCutLoss = 3
        # ===========================================================================

        Calc_Buf1 = 0
        Calc_Buf2 = 0

        GA_LenthCalc = 0.0          # 비사용 : 3D 가공 위치값이므로 계산만 하고, 사용X
        # GA_L_C_Before = 0.0     

        GRobotLen = 0.0
        GBlankArea = 0.0
        # GConvDist = 0.0
        

        #실제 거리 값 계산(자동에서의 콘베어에 의한 이동값과 비교)
        #이전의 값과 현재의 이동 요구값을 비교 -> 더 많이 나가 있으면, 그 만큼을 계산에 포함하고, 콘베어는 이동하지 않는다.
        # GA_L_C_Before = GA_LenthCalc      # 비사용
        CalcConvLen = Cons_Lenth            # - GA_LenthCalc    # 비사용    
        

        #프라즈마 절단 Loss
        PlasmaCutLoss = GCutLoss / 2        # 1.5

        #사각관의 우 절단 가공에 적용 [14.02.21]
        if (sizekind == 'SP'):
            Tube_Margin = GTubeMargin - PlasmaCutLoss
        else:
            Tube_Margin = 0


        # #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # #사각귀 S개선용 ~ 비사용 제거
        # ES_Use = 0
        ES_Start = 0        # 비사용(=0) 으로 대응
        # #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        

        #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        #가공 구분에 따라 ~ 로봇가공거리,콘베어이동거리,BlankArea를 계산
        if c_code == 0:
            GRobotLen = 0
            CalcConvLen = CalcConvLen + PlasmaCutLoss

        elif c_code == 1 or c_code == 2:
            GRobotLen = Cons_a
            GBlankArea = Cons_a
            CalcConvLen = CalcConvLen + Cons_a

        elif c_code == 3:
            if (Cons_a >= Cons_b):
                Calc_Buf1 = Cons_a + ES_Start
            else:
                Calc_Buf1 = Cons_b + ES_Start
            GRobotLen = Calc_Buf1
            GBlankArea = Calc_Buf1

            if (sizekind == 'EA' or sizekind == 'UA'):		#앵글
                if (LenAdd > 0):     #추가코드:길이차감값
                    Calc_Buf2 = LenAdd
                else: Calc_Buf2 = (Cons_c + 1)
                GA_LenthCalc = GA_LenthCalc + Calc_Buf2
                CalcConvLen = CalcConvLen + Calc_Buf1

            elif (sizekind == 'CH'):		#쟌넬
                if (LenAdd > 0):     #추가코드:길이차감값
                    #쟌넬의 사각귀 가공길이 계산은 T1을 빼야한다.[11.07.04] 정정
                    GA_LenthCalc = GA_LenthCalc + (Work_T1 + 1)
                    CalcConvLen = CalcConvLen + Calc_Buf1
                else:
                    CalcConvLen = CalcConvLen + Calc_Buf1

            else:    # 빔 / H 빔(플렌지)
                if (LenAdd > 0):
                    #I빔과 H빔의 사각귀 가공길이 계산은 T1/2을 빼야한다.[11.07.04] 정정
                    GA_LenthCalc = GA_LenthCalc + (Work_T1 / 2 + 1)
                    CalcConvLen = CalcConvLen + Calc_Buf1
                else:
                    CalcConvLen = CalcConvLen + Calc_Buf1

        elif c_code == 4:
            #작업 선택에 따라 : 앵글/부등변 - C절단, 쟌넬 - 속사각귀
            if (sizekind == 'EA' or sizekind == 'UA'):
                if (Cons_a >= Cons_c):
                    Calc_Buf1 = Cons_a                    
                else:
                    Calc_Buf1 = Cons_c
                GRobotLen = Calc_Buf1                
                GBlankArea = Calc_Buf1
            else: 
                GRobotLen = Cons_a
                GBlankArea = Cons_a
            CalcConvLen = CalcConvLen + GBlankArea

        elif c_code == 5:
            if (Cons_a <= Cons_b): Calc_Buf1 = Cons_b
            else: Calc_Buf1 = Cons_a

            if (Cons_c <= Cons_d): Calc_Buf2 = Cons_d
            else: Calc_Buf2 = Cons_c

            if (Calc_Buf1 <= Calc_Buf2): 
                GRobotLen = Calc_Buf2
                GBlankArea = Calc_Buf2
            else: 
                GRobotLen = Calc_Buf1
                GBlankArea = Calc_Buf1
            CalcConvLen = CalcConvLen + GBlankArea

        elif c_code == 11 or c_code == 12 or c_code == 14:
            GRobotLen = Cons_a
            if (sizekind == 'PI' or sizekind == 'SP'):
                CalcConvLen = CalcConvLen + Cons_a / 2 + PIPESTART
            else:
                CalcConvLen = CalcConvLen + Cons_a / 2            

        elif c_code == 13:
            GRobotLen = Cons_a + Cons_c       #평타원
            if (sizekind == 'PI' or sizekind == 'SP'):
                CalcConvLen = CalcConvLen + (Cons_a + Cons_c) / 2 + PIPESTART
            else:
                CalcConvLen = CalcConvLen + (Cons_a + Cons_c) / 2

        elif c_code == 15:
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            #상/하에 따라 - 거리 상수b값 재 계산 및 V Cut 내부 간격(GAP) : T에대한 비율값(상수b에 포함한) + 보정값
            if (Work_Code[1][0:1] == "0"):
                # V 컷팅 상부(두께) 비율(GVCutTAdj:1)
                if (Work_T2 >= 9): Calc_Buf1 = GVCutTAdj + 0.15
                else: Calc_Buf1 = GVCutTAdj + 0.21
                Cons_b = int((Work_S - (Work_T2 * Calc_Buf1)) * math.tan(Cons_a / 2 * math.pi / 180.0))
                GRobotLen = (Cons_b + (Work_T1 * 0.12)) * 2 + (GVCutGapAdj)

                if (LenAdd > 0):     #추가코드:길이차감값 [2019.05.09]
                    Calc_Buf2 = LenAdd
                else:
                    Calc_Buf2 = (Work_T2 * 2)   #GA_LenthCalc = GA_LenthCalc + (Work_T2 * 2)

                GA_LenthCalc += Calc_Buf2
                CalcConvLen = CalcConvLen + Cons_b + (Work_T1 * 0.12) + (GVCutGapAdj / 2) - (Calc_Buf2 / 2)
            else:
                if (Work_T1 >= 9): Calc_Buf1 = GVCutTAdj + 0.15 
                else: Calc_Buf1 = GVCutTAdj + 0.21
                Cons_b = int((Work_L - (Work_T1 * Calc_Buf1)) * math.tan(Cons_a / 2 * math.pi / 180.0))
                GRobotLen = (Cons_b + (Work_T2 * 0.12)) * 2 + (GVCutGapAdj)

                if (LenAdd > 0):     #추가코드:길이차감값 [2019.05.09]
                    Calc_Buf2 = LenAdd
                else:
                    Calc_Buf2 = (Work_T1 * 2)   #GA_LenthCalc = GA_LenthCalc + (Work_T1 * 2)

                GA_LenthCalc += Calc_Buf2
                CalcConvLen = CalcConvLen + Cons_b + (Work_T2 * 0.12) + (GVCutGapAdj / 2) - (Calc_Buf2 / 2)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        elif c_code == 16:
            GRobotLen = Cons_a
            CalcConvLen = CalcConvLen + Cons_a

        elif c_code == 21 or c_code == 22:
            GRobotLen = Cons_a
            GBlankArea = Cons_a
            CalcConvLen = CalcConvLen + Cons_a + PlasmaCutLoss

        elif c_code == 23:
            if (Cons_a >= Cons_b):
                Calc_Buf1 = Cons_a
            else:
                Calc_Buf1 = Cons_b
            GRobotLen = Calc_Buf1

            if (sizekind == 'EA' or sizekind == 'UA'):		#앵글
                if (LenAdd > 0):     #추가코드:길이차감값 [2019.05.09]
                    Calc_Buf2 = LenAdd
                else: Calc_Buf2 = (Cons_c + 1)
                GA_LenthCalc = GA_LenthCalc + Calc_Buf2
                CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss       # - (Calc_Buf2)

            elif (sizekind == 'CH'):		#쟌넬
                if (LenAdd > 0):
                    #쟌넬의 사각귀 가공길이 계산은 T1을 빼야한다.[11.07.04] 정정
                    GA_LenthCalc = GA_LenthCalc + (Work_T1 + 1)
                    CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss   # - (Work_T1 + 1)
                else:
                    CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss

            else:    # 빔 / H 빔(플렌지)
                if (LenAdd > 0):
                    #I빔과 H빔의 사각귀 가공길이 계산은 T1/2을 빼야한다.[11.07.04] 정정
                    GA_LenthCalc = GA_LenthCalc + (Work_T1 / 2 + 1)
                    CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss   # - (Work_T1 / 2 + 1)
                else:
                    CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss 

        elif c_code == 24:
            #작업 선택에 따라 : 앵글/부등변 - C절단, 쟌넬 - 속사각귀
            if (sizekind == 'EA' or sizekind == 'UA'):
                if (Cons_a >= Cons_c):
                    Calc_Buf1 = Cons_a                    
                else:
                    Calc_Buf1 = Cons_c
                GRobotLen = Calc_Buf1
                CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss
            else: 
                GRobotLen = Cons_a
                CalcConvLen = CalcConvLen + Cons_a + PlasmaCutLoss

        elif c_code == 25:
            if (Cons_a <= Cons_b): Calc_Buf1 = Cons_b
            else: Calc_Buf1 = Cons_a

            if (Cons_c <= Cons_d): Calc_Buf2 = Cons_d
            else: Calc_Buf2 = Cons_c

            if (Calc_Buf1 <= Calc_Buf2): 
                GRobotLen = Calc_Buf2
                CalcConvLen = CalcConvLen + Calc_Buf2 + PlasmaCutLoss
            else: 
                GRobotLen = Calc_Buf1
                CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss


        elif c_code == 31:
            GRobotLen = Cons_a
            if (sizekind == 'PI' or sizekind == 'SP'): CalcConvLen = CalcConvLen + Cons_a + PIPESTART
            else: CalcConvLen = CalcConvLen + Cons_a
            #선1도 블랭크 영역으로 계산하여 배출 핸드로 잡지 않는다.(특히 앵글->부등변 만들기 가공) [08.05.22]
            GBlankArea = GBlankArea + Cons_a

        elif c_code == 32:    #선2 S개선
            if (Cons_d > 100 and Cons_d <= 145): GRobotLen = ES_Start
            else: GRobotLen = 0

        elif c_code == 33 or c_code == 34:
            GRobotLen = Cons_a
            if (sizekind == 'PI' or sizekind == 'SP'): CalcConvLen = CalcConvLen + Cons_a + PIPESTART
            else: CalcConvLen = CalcConvLen + Cons_a


        elif c_code == 40:    #파이프/사각관 수직 절단(+ PIPESTART는 기준점에서...)
            GRobotLen = 0 + Tube_Margin
            CalcConvLen = CalcConvLen + PlasmaCutLoss + PIPESTART + Tube_Margin

        elif c_code == 50:
            GRobotLen = 0
            CalcConvLen = CalcConvLen + PIPESTART

        elif c_code == 41 or c_code == 42:
            GRobotLen = (Cons_b + Work_T2) /  math.tan(Cons_a * math.pi / 180.0)
            CalcConvLen = CalcConvLen + Cons_b / math.tan(Cons_a * math.pi / 180.0) + PIPESTART
            GBlankArea = Cons_b / math.tan(Cons_a * math.pi / 180.0)

        elif c_code == 43:
            GRobotLen = (Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2)))
            CalcConvLen = CalcConvLen + (Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2))) + PIPESTART
            if (LenAdd > 0):     #두개가 쌍이므로 두번째에서...(그리고 2행정이므로 두번째 행정에서만) ~> 길이 차감값
                GBlankArea = CalcConvLen + (Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2)))
                #가공길이 차감항목 [08.06.14]
                Calc_Buf1 = (Cons_b / 2) - ((Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2))))
                GA_LenthCalc = GA_LenthCalc + Calc_Buf1

        elif c_code == 44 or c_code == 45:        #파이프 가공 길이 Over 계산 포함 : Cons_d [21.10.28] ~ 롤백[22.01.06]
            #GRobotLen = 0 + (Cons_b + Work_T2) / math.tan(Cons_a * math.pi / 180.0)         #수정 전 내용 : NG
            GRobotLen = 0 + (Cons_b + 0) / math.tan(Cons_a * math.pi / 180.0)               #재고찰 수정 [2022.03.22]
            CalcConvLen = CalcConvLen + Cons_d + (Cons_b + 0) / math.tan(Cons_a * math.pi / 180.0) + PIPESTART
            if (LenAdd > 0):
                GA_LenthCalc = GA_LenthCalc - (Cons_d)
                GBlankArea = Cons_d + Cons_b / math.tan(Cons_a * math.pi / 180.0)

        elif c_code == 51 or c_code == 52:
            GRobotLen = (Cons_b - Work_T2) / math.tan(Cons_a * math.pi / 180.0)
            CalcConvLen = CalcConvLen + Cons_b / math.tan(Cons_a * math.pi / 180.0) + PlasmaCutLoss + PIPESTART

        elif c_code == 53:
            GRobotLen = (Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2)))
            CalcConvLen = CalcConvLen + (Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2))) + PlasmaCutLoss + PIPESTART
            if (LenAdd > 0):     #두개가 쌍이므로 첫번째에서...(그리고 2행정이므로 첫 행정에서만) ~> 길이 차감값
                #가공길이 차감항목 [08.06.14]
                Calc_Buf1 = (Cons_b / 2) - ((Cons_c / 2) - (math.sqrt(math.pow((Cons_c / 2), 2) - math.pow((Cons_b / 2 - Work_T2), 2))))
                GA_LenthCalc = GA_LenthCalc + Calc_Buf1
                # CalcConvLen = CalcConvLen - Calc_Buf1

        elif c_code == 54 or c_code == 55:        #파이프 가공 길이 Over 계산 포함 : Cons_d [21.10.28] ~ 롤백X(같음)
            #GRobotLen = Cons_d + (Cons_b - Work_T2) / math.tan(Cons_a * math.pi / 180.0)      #NG
            GRobotLen = Cons_d + (Cons_b - 0) / math.tan(Cons_a * math.pi / 180.0)          #재고찰 수정 [2022.03.22]
            #CalcConvLen = CalcConvLen + Cons_d + (Cons_b - Work_T2) / math.tan(Cons_a * math.pi / 180.0F) + PlasmaCutLoss + PIPESTART    # : NG
            CalcConvLen = CalcConvLen + Cons_d + (Cons_b - 0) / math.tan(Cons_a * math.pi / 180.0) + PlasmaCutLoss + PIPESTART

        elif c_code == 46:    #사각관 좌 대각절단
            if (Cons_a <= Cons_b): Calc_Buf1 = Cons_b
            else: Calc_Buf1 = Cons_a

            if (Cons_c <= Cons_d): Calc_Buf2 = Cons_d
            else: Calc_Buf2 = Cons_c

            if (Calc_Buf1 <= Calc_Buf2):
                GRobotLen = Calc_Buf2
                GBlankArea = Calc_Buf2
            else: 
                GRobotLen = Calc_Buf1
                GBlankArea = Calc_Buf1            
            CalcConvLen = CalcConvLen + GBlankArea + PIPESTART

        elif c_code == 56:    #사각관 우 대각절단
            if (Cons_a <= Cons_b): Calc_Buf1 = Cons_b
            else: Calc_Buf1 = Cons_a

            if (Cons_c <= Cons_d): Calc_Buf2 = Cons_d
            else: Calc_Buf2 = Cons_c

            if (Calc_Buf1 <= Calc_Buf2): 
                GRobotLen = Calc_Buf2 + Tube_Margin
                CalcConvLen = CalcConvLen + Calc_Buf2 + PlasmaCutLoss + PIPESTART + Tube_Margin
            else: 
                GRobotLen = Calc_Buf1 + Tube_Margin
                CalcConvLen = CalcConvLen + Calc_Buf1 + PlasmaCutLoss + PIPESTART + Tube_Margin


        #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        # 결과값 ~ 소수점 3자리로 정리
        # 로봇 이동 거리 
        GRobotLen = str(round(float(GRobotLen), 3))
        # 콘베어 이동 거리(값) 및 그리퍼 blank 값 계산
        GConvDist = str(round(float(CalcConvLen), 3))
        # 배출 핸드 ~ 가공으로 인해 잡히는 부분이 없는 구간(좌측 가공 및 V,ㄷ 컷팅)
        GBlankArea = str(round(float(GBlankArea), 3))
        
        return 'OK,' + GRobotLen + ',' + GConvDist + ',' + GBlankArea      # 'OK,로봇가공거리,콘베어이동거리, 배출핸드Blank영역'

        #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    except:
        # print("error occured")       # 에러 메시지
        return 'NG,error occured,0,0,0'



# # 가공 포인트 정렬 및 V 컷팅 및 사각귀에 의한 전체 길이 계산 (앵글, 파이프) ~ 사용X
# def PointArrary1(VAngle_S, VAngle_L, VAngle_T, VLenth, ArrayBuffer, WorkPointCode):

# # 가공 포인트 정렬 및 V 컷팅 및 사각귀에 의한 전체 길이 계산 (부등변, 쟌넬, I/H빔) ~ 사용X
# def PointArrary2(VAngle_S, VAngle_L, VAngle_T1, VAngle_T2, VLenth, ArrayBuffer, WorkPointCode):

# # 좌표 계산 하기 함수 : 앵글 전용기 ~> Web 함수 (이동)
# def CalcNewStan_EA(T_Origin, size_code):

# # 좌표 계산 하기 함수 ~> Web 함수 (이동)
# def CalcNewStan(Sel_Calc, T_Origin, GWorkPosition, size_code):


# data='C_FUNC#CALCREALLENTH#EA 50*50*6T$294,EA015,90,43,0,0,12$1$0$100$10'
# recvstr = data.split('#')
# print(rpcm_Func(recvstr[1], recvstr[2]))


