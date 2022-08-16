import math
import json
from .models import MaterialSpec

# 좌표 계산 하기 함수 : 앵글 전용기 (U1 좌표계)
def CalcNewStan_Agcut(MachineID, origin_pos):     # 앵글 전용기
    try:
        return ('ok')
        materialdata = MaterialSpec.objects.filter(MachineID=MachineID)
    except MaterialSpec.DoesNotExist:
        return ('Not Data')
    # 자재 기준점 계산
    for code in materialdata:
        k = code.m_kinds
        Sel_Calc = k.split()
        c1 = json.loads(code.m_param)
        if Sel_Calc[0] == 'EA':     #앵글
            c1[1] = str(round(T_Origin[0], 1))     # X
            c1[2] = str(round(T_Origin[1], 1))     # Y
            c1[3] = str(round(T_Origin[2] + float(c1[9]), 1))     # Z
            c1[4] = str(round(T_Origin[3], 1))     # RX
            c1[5] = str(round(T_Origin[4], 1))     # RY
            c1[6] = str(round(T_Origin[5], 1))     # RZ
        code.m_param = c1
        code.save()
    return "OK"

# 좌표 계산 하기 함수 : 자재별 (U1 좌표계)
def CalcNewStan(MachineID, GWorkPosition, T_Origin):
    try:
        try:
            materialdata = MaterialSpec.objects.filter(MachineID=MachineID)
        except MaterialSpec.DoesNotExist:
            return('Not Data')
        for code in materialdata:
            k = code.m_kinds
            Sel_Calc = k.split()
            c1 = json.loads(code.m_param)

            if Sel_Calc[0] == 'EA':     #앵글
                c1[1] = str(round(T_Origin[0], 1))      # X
                #작업 위치 방향 (A형/B형(우행))
                if GWorkPosition == '1':
                    c1[2] = str(round(T_Origin[1] - float(c1[10]) + 0.5, 1))     # Y
                else:
                    c1[2] = str(round(T_Origin[1] + float(c1[10]) - 0.5, 1))     # Y
                c1[3] = str(round(T_Origin[2] + float(c1[9]), 1))      # Z
                c1[4] = str(round(T_Origin[3], 1))      # RX
                c1[5] = str(round(T_Origin[4], 1))      # RY
                c1[6] = str(round(T_Origin[5], 1))      # RZ
                code.m_param = c1
                code.save()

            elif Sel_Calc[0] == 'UA':     #부등변
                c1[1] = str(round(T_Origin[0], 1))     # X

                #작업 위치 방향 (A형/B형)
                if  GWorkPosition == '1':
                    Size_buf2 = c1[3:]
                    Size_buf = Size_buf2.split('*')
                    work_S1 = float(Size_buf[0])
                    work_S2 = float(Size_buf[1])
                    #--------------------------------------------------------------------------------------------------------------
                    #중심점(Y) 값 계산 : 전체밑변 길이에서 DB의 center값을 뺀 나머지 값 ~ 부등변 앵글은 중심점이 정센터가 아니므로 ~ 수정 괄호<")"> [2019.08.29]
                    Calc_Center = math.sqrt(math.pow(work_S1, 2) + math.pow(work_S2, 2)) - float(c1[10])
                    #--------------------------------------------------------------------------------------------------------------
                    c1[2] = str(round(T_Origin[1] - Calc_Center + 0.5, 1))   #Y
                else:
                    #--------------------------------------------------------------------------------------------------------------
                    #중심점(Y) 값 계산 : 전체밑변 길이에서 DB의 center값을 뺀 나머지 값 ~ 부등변 앵글은 중심점이 정센터가 아니므로
                    # Calc_Center = size_code[c1][10]
                    #--------------------------------------------------------------------------------------------------------------
                    c1[2] = str(round(T_Origin[1] + float(c1[10]) - 0.5, 1))   #Y

                c1[3] = str(round(T_Origin[2] + float(c1[9]), 1))      # Z
                c1[4] = str(round(T_Origin[3], 1))      # RX
                c1[5] = str(round(T_Origin[4], 1))      # RY
                c1[6] = str(round(T_Origin[5], 1))      # RZ
                code.m_param = c1
                code.save()

            elif Sel_Calc[0] == 'CH' or Sel_Calc[0] == 'IB' or Sel_Calc[0] == 'HB':     #쟌넬 / #I빔 / #H빔
                Size_buf2 = k[3:]
                Size_buf = Size_buf2.split('*')
                work_S1 = float(Size_buf[0])
                work_S2 = float(Size_buf[1])
                c1[1] = str(round(T_Origin[0], 1))     # X
                #작업 위치 방향 (A형/B형(우행)
                if  GWorkPosition == '1': # 우행
                    c1[2] = str(round(T_Origin[1], 1))     # Y
                else:
                    c1[2] = str(round(T_Origin[1] + work_S1, 1))    # Y

                c1[3] = str(round(T_Origin[2] + work_S2, 1))      # Z
                c1[4] = str(round(T_Origin[3], 1))      # RX
                c1[5] = str(round(T_Origin[4], 1))      # RY
                c1[6] = str(round(T_Origin[5], 1))      # RZ
                code.m_param = c1
                code.save()

            elif Sel_Calc[0] == 'PI':     #파이프
                Size_buf2 = k[3:]
                Size_buf = Size_buf2.split('-')
                work_S2 = float(Size_buf[1])

                c1[1] = str(round(T_Origin[0], 1))     # X
                #작업 위치 방향 (A형/B형)
                Calc_Center = work_S2 / 2
                if  GWorkPosition == '1':
                    c1[2] = str(round(T_Origin[1] - Calc_Center, 1))     # Y
                else:
                    c1[2] = str(round(T_Origin[1] + Calc_Center, 1))     # Y

                c1[3] = str(round(T_Origin[2] + work_S2, 1))      # Z
                c1[4] = str(round(T_Origin[3], 1))      # RX
                c1[5] = str(round(T_Origin[4], 1))      # RY
                c1[6] = str(round(T_Origin[5], 1))      # RZ
                code.m_param = c1
                code.save()

            elif Sel_Calc[0] == 'SP':     #사각관
                Size_buf2 = k[3:]
                Size_buf = Size_buf2.split('*')
                work_S1 = float(Size_buf[0])
                work_S2 = float(Size_buf[1])

                c1[1] = str(round(T_Origin[0], 1))     # X
                #작업 위치 방향 (A형/B형)
                if  GWorkPosition == '1':
                    c1[2] = str(round(T_Origin[1], 1))    # Y
                else:
                    c1[2] = str(round(T_Origin[1] + work_S1, 1))     # Y

                c1[3] = str(round(T_Origin[2] + work_S2, 1))      # Z
                c1[4] = str(round(T_Origin[3], 1))      # RX
                c1[5] = str(round(T_Origin[4], 1))      # RY
                c1[6] = str(round(T_Origin[5], 1))      # RZ
                code.m_param = c1
                code.save()
            else:
                return('Not Match')
        return "OK"
    except:
        return "NG error occured"
