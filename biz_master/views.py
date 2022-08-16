import json
import math
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import BizMaster
from .serializers import BizMasterSerializer
from .serializers import BizCodeSerializer
from .xlparse import xlparse
from datetime import datetime, date, timedelta
from django.utils.dateformat import DateFormat


# Create your views here.
@api_view(['GET'])
def hello(request):
    return Response({
            '[GET] url/biz_master/...' : '가공코드 도면(블록) 데이터 관련 MES',
    })

# 코드시스 I/F 파트------------------------------------------------------------------------
# blkcp list 파트 : 가공 데이터 등록시 자동 생성된 데이터
@api_view(['POST'])
def cutting_list(request, format=None):

    # 1. 입력 데이터 업로드 ------------------------------------------------------------------
    # {"cmd": "jsonupload", "MachineID": "1", "MachineKey":"pass", "jsondata": [json]}
    if request.data['cmd'] == 'jsonupload':
        MachineID = request.data['MachineID']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        uploaddata = request.data['jsondata']

        # 필드마스터 등록
        try:
            fieldlist = []
            for fielddatas in uploaddata:   # 각 피스 단위로 추출됨: [{피스정보},{피스정보}]
                for key in fielddatas['part'].keys():   # 부재 단위로 추출됨: part : [{ea01:{},ea02:{},...}]
                    fielddata = fielddatas['part'][key]   # 부재 정보 담김
                    fielddata['UserID'] = fielddatas['UserID']
                    # fielddata['MachineID'] = fielddatas['MachineID']
                    fielddata['Material'] = fielddatas['Material'] + '~' + key
                    if FieldMaster.objects.filter(Material=fielddata["Material"]).exists():
                        continue
                    # Ubolt 변환...
                    cutlist = fielddata['cutlist']
                    cutlist2 = []
                    macro = fielddata['standard'].split(' ')[0]
                    for cut in cutlist:  # 가공 매크로 순회
                        # cuts는 {"CUT": [거리, 매크로(홀), 상수A(홀크기), 상수B(높이), 상수C, 상수D]}의 리스트
                        # U볼트 정보 ~ 홀(파이), 높이, 규격(A), Pitch, 홀체크(0,1),슈여부(0,1), 슈홀(파이), 슈높이
                        # {"CUT": ["100", "UBOLT0", "12", "22", "50A", "74", "1", "0", "0", "25"]}
                        if 'UBOLT' in cut['CUT'][1]:
                            start = {"CUT": [str(int(cut['CUT'][0])-int(cut['CUT'][5])/2), macro+cut['CUT'][1][-1]+'11',
                                             cut['CUT'][2], cut['CUT'][3], "0", "0"]}
                            cutlist2.append(start)
                            end = {"CUT": [str(int(cut['CUT'][0])+int(cut['CUT'][5])/2), macro+cut['CUT'][1][-1]+'11',
                                             cut['CUT'][2], cut['CUT'][3], "0", "0"]}
                            cutlist2.append(end)
                            if cut['CUT'][7] == '1':
                                mid = {"CUT": [cut['CUT'][0], macro+cut['CUT'][1][-1]+'11',
                                                 cut['CUT'][8], cut['CUT'][9], "0", "0"]}
                                cutlist2.append(mid)
                        else:
                            cutlist2.append(cut)
                    # 가공 위치순으로 정렬
                    list = []
                    cutting = []
                    for f in cutlist2:
                        list.append(f['CUT'])
                    s = sorted(list, key=lambda x: float(x[0]))
                    for l in s:
                        cutt = {'CUT': l}
                        cutting.append(cutt)
                    fielddata['cutlist']= cutting
                    fieldlist.append(fielddata)   # 부재 하나씩 추가하여 부재별 리스트 만들어짐(AutoMarkMachine)
            fieldserializer = FieldMasterSerializer(data=fieldlist, many=True)
            if fieldserializer.is_valid():
                fieldserializer.save()
            else:
                return Response(fieldserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'massage':'fieldcreate_Error'})
        # 코드 마스터 등록
        try:
            codedata = []
            for data in uploaddata:
                code = {}
                code['UserID'] = data['UserID']
                # code['MachineID'] = data['MachineID']
                code['Material'] = data['Material']

                if CodeMaster.objects.filter(Material=code["Material"]).exists():
                    continue

                if code not in codedata:
                    codedata.append(data)
            codeserializer = CodeMasterSerializer(data=codedata, many=True)
            if codeserializer.is_valid():
                codeserializer.save()
            else:
                return Response(codeserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'massage':'codecreate_Error'})
        # 비즈마스터 등록
        try:
            bizdata = []
            for data in uploaddata:
                bizcode = {}
                bizcode['UserID'] = data['UserID']
                # bizcode['MachineID'] = data['MachineID']
                material = data['Material'].split('~')   #호선~블럭~피스
                bizcode['Material'] = material[0] + '~' + material[1]

                if BizMaster.objects.filter(Material=bizcode["Material"]).exists():
                    continue

                if bizcode not in bizdata:
                    bizdata.append(bizcode)

            bizcodes = BizCodeSerializer(data=bizdata, many=True)
            if bizcodes.is_valid():
                bizcodes.save()
                return Response(bizcodes.data, status=status.HTTP_201_CREATED)
            return Response(bizcodes.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'massage':'bizcreate_Error'})

    # 2. 블록 리스트 전체 보기 -----------------------------------------------------------

    if request.data['cmd'] == 'blocklist':
        try:
            UserID = request.data['UserID']
            # MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage':'blocklist_Error'})

    # 3. 가공 작업 완료한 블록 리스트 보기 ---------------------------------------------------------------

    if request.data['cmd'] == 'workedblocklist':
        try:
            UserID = request.data['UserID']
            # MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID, worked_date__range=[date.today() - timedelta(days=60), datetime.now()])
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage':'workedblocklist_Error'})


    # 4. 미가공 블록 중 작업 선택된 블록 리스트 보기 -----------------------------------------------------------

    if request.data['cmd'] == 'selblocklist':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID, worked_date=None, work_select=True)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage':'selblocklist_Error'})

    # 5. 미가공 블록 중 작업 선택되지 않은 블록 리스트 보기 -----------------------------------------------------------

    if request.data['cmd'] == 'notselblocklist':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID, worked_date=None, work_select=False)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage':'notselblocklist_Error'})

    # 6. 작업할 블록 선택 하기 ----------------------------------------------------------------------
    if request.data['cmd'] == 'selectblock':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            selblk = request.data['blockname']
            _selblk = selblk + '~'  # 피스, 부재 쿼리시 블록이름 중복으로 오류방지를 위해 ~까지 넣어서 쿼리함
            try:
                select_fields = FieldMaster.objects.filter(UserID=UserID, Material__contains=_selblk)
                select_fields.update(work_select=True)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                select_blk = BizMaster.objects.get(UserID=UserID, Material=selblk)
                select_blk.work_select = True
                select_blk.save()
            except BizMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage': 'selectblock_Error'})

    # 7. 작업 선택한 블록 취소하기 ---------------------------------------------------------------------
    if request.data['cmd'] == 'cancleblock':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            selblk = request.data['blockname']
            _selblk = selblk + '~'
            try:
                select_blk = BizMaster.objects.get(UserID=UserID, Material=selblk)
                select_blk.work_select = False
                select_blk.save()
            except BizMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                select_fields = FieldMaster.objects.filter(UserID=UserID, Material__contains=_selblk)
                select_fields.update(work_select=False)
                # 아래의 내용과 동일하지만 효율적인 방식(반복하지 않고 여러필드를 한번에 수정)
                # for select_field in select_fields:
                #     select_field.work_select = False
                #     select_field.save()
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID)
            except BizMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = BizCodeSerializer(bizdata, many=True)
            return Response(serializer.data)
        except:
            return Response({'massage': 'cancleblock_Error'})

    # 8. 블록 삭제하기(코드, 필드 데이터 다 지워짐)-----------------------------------------------------
    if request.data['cmd'] == 'deleteblock':
        try:
            UserID = request.data['UserID']
            # MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            delblk = request.data['blockname']
            _delblk = delblk + '~'
            try:
                bizdata = BizMaster.objects.filter(UserID=UserID, Material=delblk)
                bizdata.delete()
                codedata = CodeMaster.objects.filter(UserID=UserID, Material__contains=_delblk)
                codedata.delete()
                fielddata = FieldMaster.objects.filter(UserID=UserID, Material__contains=_delblk)
                fielddata.delete()
                return Response({'massage': 'deleteblock_OK'})
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'massage': 'deleteblock_Error'})

    # 9. 소요자재 리스트 보기 -----------------------------------------------------------------
    if request.data['cmd'] == 'requiredmaterials':
        try:
            UserID = request.data['UserID']
            # MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fieldlist = []
            try:
                fielddata = FieldMaster.objects.filter(UserID=UserID, work_select=True)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = FieldMasterSerializer(fielddata, many=True)
            for field in serializer.data:
                fieldlist.append({field['standard']: field['length']})
            result = {}
            for d in fieldlist:
                for k in d.keys():
                    result[k] = result.get(k, 0) + d[k]
            return Response(result)
        except:
            return Response({'massage': 'requiredmaterials_Error'})

    # 10. 부재 가공 실적 등록 -----------------------------------------------------------------------
    if request.data['cmd'] == 'workedmaterial':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            material = request.data['Material']
            try:
                work = FieldMaster.objects.get(UserID=UserID, Material=material)
                # 전체 수량이 작업 수량 보다 클때
                if work.quantity > work.work_count:
                    work.work_count = work.work_count + 1
                # 작업 수량 increment 후 가공 완료 확인
                if work.quantity == work.work_count:
                    work.worked_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                work.save()
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            blocklist = material.split('~')[:2]
            blockname = blocklist[0] + '~' + blocklist[1]
            _blockname = blockname + '~'
            try:
                result = FieldMaster.objects.filter(UserID=request.data['UserID'],
                                                    Material__contains=_blockname, worked_date=None).exists()
                if result == False:
                    try:
                        block = BizMaster.objects.get(UserID=request.data['UserID'], Material=blockname)
                        block.worked_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        block.save()
                        return Response({blockname: 'wb_Ok'})
                    except:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                return Response({'workcount': work.work_count})
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'massage': 'workedmaterial_Error'})

    # 11. 투입 자재의 길이에 따른 가공 순서 정렬 하기(Nesting)------------------------------------------
    if request.data['cmd'] == 'nesting':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            if MachineID != 'miju_rpcm_agcut':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            standard = request.data['standard']
            inputlength = int(request.data['length'])  # 투입 자재 길이
            texture =request.data['texture']
            if inputlength < 2000:
                return Response({'massage': 'shortLength'})

            # ---------------------------------------------------------------
            try:
                fielddata = FieldMaster.objects.filter(UserID=UserID, work_select=True, standard=standard, texture=texture)
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = FieldMasterSerializer(fielddata, many=True)
            nestlist = []
            nonnestlist = []
            minlen = 15
            maxlen = 900
            oklen = 100
            endlen = 400  # 900이상이 없을때 끝자재의 최소 길이
            count = 0
            worklength = inputlength
            nestlength = 0
            for nest in serializer.data:
                worklength = worklength - int(nest['length_real'])
                if int(nest['length_real']) >= maxlen:
                    count = count + 1
                # -------------------------------------------------------
                if count == 0:
                    if worklength >= (maxlen + minlen):
                        nestlist.append(nest)
                        nestlength = nestlength + int(nest['length_real'])  # 정렬에 포함된 자재 길이의 합
                    elif worklength < (maxlen + minlen):   # 정렬 길이 범위 초과
                        nonnestlist.append(nest)
                        worklength = worklength + int(nest['length_real'])
                # -------------------------------------------------------
                elif count == 1:
                    if worklength >= minlen:
                        nestlist.append(nest)
                        nestlength = nestlength + int(nest['length_real'])  # 정렬에 포함된 자재 길이의 합
                    elif worklength < minlen:   # 정렬 길이 범위 초과
                        if int(nest['length_real']) >= maxlen:
                            while True:
                                poppcs = nestlist.pop()
                                nestlength = nestlength - int(poppcs['length_real'])
                                worklength = worklength + int(poppcs['length_real'])
                                if worklength >= minlen:
                                    break
                            nestlist.append(nest)
                            nestlength = nestlength + int(nest['length_real'])
                        else:
                            nonnestlist.append(nest)
                            worklength = worklength + int(nest['length_real'])
                    if worklength <= oklen:   # 잔재(x) 길이가 15 < x < 100 이면 nest_ok
                        break
                # ------------------------------------------------------------
                else:  # count가 2 이상일때
                    if int(nest['length_real']) >= maxlen:
                        nonnestlist.append(nest)
                        worklength = worklength + int(nest['length_real'])
                    else:
                        if worklength >= minlen:
                            nestlist.append(nest)
                            nestlength = nestlength + int(nest['length_real'])  # 정렬에 포함된 자재 길이의 합
                        elif worklength < minlen:   # 정렬 길이 범위 초과
                            nonnestlist.append(nest)
                            worklength = worklength + int(nest['length_real'])
                        if worklength <= oklen:   # 잔재(x) 길이가 15 < x < 100 이면 nest_ok
                            break
            print(count)
            # 정렬된 자재속에 900mm 이상이 있을시
            if int(nestlist[-1]['length_real']) > 900 and count >= 1:  # 정렬 부재의 마지막 길이가 900 이상인 경우
                # return Response(nestlist)
                pass
            elif count >= 1:
                # 정렬된 부재속에 900 이상이 포함되어 있고 마지막 피스가 maxlen 이하일 경우
                for idx, nest in enumerate(nestlist):
                    if int(nest['length_real']) > maxlen:
                        del nestlist[idx]
                        nestlist.append(nest)
                        break
                # return Response(nestlist)
                # return Response({'nestlength': nestlength})
            elif count == 0:   # 정렬된 부재속에 900 이상이 포함되지 않았을 경우
                for nest in nonnestlist:
                    re_len = inputlength - nestlength
                    if (re_len - nest['length_real']) > endlen:
                        nestlist.append(nest)
                        nestlength = nestlength + int(nest['length_real'])
                    else:
                        break
            for part in nestlist:
                del part['id']
                del part['UserID']
                del part['standard']
                del part['texture']
                del part['part_point']
                del part['creation_date']
                del part['weight']
                del part['worked_date']
                del part['work_select']
                del part['cutlist']
                del part['worked_time']
                del part['length']
            return Response(nestlist)

        except:
            return Response({'massage': 'nesting_Error'})

    # 12. Cutting data ------------------------------------------
    if request.data['cmd'] == 'cutting_data':
        try:
            UserID = request.data['UserID']
            MachineID = request.data['MachineID']
            if MachineID != 'miju_rpcm_agcut':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            MachineKey = request.data['MachineKey']
            if MachineKey != 'pass':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Material = request.data['Material']
            # ---------------------------------------------------------------
            try:
                fielddata = FieldMaster.objects.filter(UserID=UserID, Material=Material).last()
            except FieldMaster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            cutting_data = fielddata.cutlist

            return Response(cutting_data)
        except:
            return Response({'massage': 'cuttingData_Error'})





# init_data 파트-------------------------------------------------------------------
@api_view(['POST'])
def init_list(request, format=None):
    try:
        UserID = request.data['UserID']
        MachineID = request.data['MachineID']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        inidata = InitData.objects.filter(UserID=UserID, MachineID=MachineID)
        serializer = InitDataSerializer(inidata, many=True)
        return Response(serializer.data)
    except:
        return Response({'massage': 'InitList_Error'})

# material_spec 파트
# MaterialSpec Model 사용안함
@api_view(['POST'])
def material_list(request, format=None):
    try:
        UserID = request.data['UserID']
        MachineID = request.data['MachineID']  # 로봇 형강가공기 공통
        MachineKey = request.data['MachineKey']
        m_kinds = request.data['worksize']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            initdata = InitData.objects.filter(MachineID=MachineID).last()
        except InitData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kind = m_kinds.split(' ')  # 자재종류
        size = kind[1].split('*')   # 자재규격
        pos = initdata.ORIGIN_POS.split(',')  # 장비 원점 좌표

        res = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
           # 단위중량, x,   y,   z,   rx,  ry,  rz,상부각,하부각,높이,중심점
        if MachineID == 'miju_rpcm_agcut':
            res[0] = '10'
            res[1] = pos[0]  # 절대원점 x 그대로 대입
            res[2] = pos[1]  # 절대원점 y 그대로 대입
            a = float(size[0]) * round(math.radians(45), 1)  # 앵글 삼각형 중심선 높이
            b = size[2].replace('T', '')
            c = float(b[0]) * round(math.radians(45), 1)  # 두께에 대한 꼭지점 높이
            res[3] = str(round(float(pos[2]) + a + (c * 0.8), 1))
            res[4] = pos[3]  # 절대원점 rx 그대로 대입
            res[5] = pos[4]  # 절대원점 ry 그대로 대입
            res[6] = pos[5]  # 절대원점 rz 그대로 대입
            res[7] = '45'
            res[8] = '45'
            res[9] = res[3]  # 자재원점 z 대입
            res[9] = pos[1]  # 절대원점 y 그대로 대입

            return Response(res)
        elif MachineID == 'miju_rpcm_S300':
            pass
    except:
        return Response({'massage': 'MaterialList_Error'})

# speed_spec 파트

@api_view(['POST'])
def speed_list(request, format=None):
    try:
        Userid = request.data['UserID']
        MachineID = request.data['MachineID']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 속도 데이터 요청

        if request.data['cmd'] == 'RD_velocity':
            s_kinds = request.data['worksize']
            texture = request.data['texture']
            print('aaa')
            try:
                speeddata = SpeedSpec.objects.filter(MachineID=MachineID,
                                                     s_kinds=s_kinds, texture=texture).last()
            except SpeedSpec.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            print(speeddata.s_param)
            res = speeddata.s_param
            return Response(res)
    except:
        return Response({'massage': 'SpeedList_Error'})

# macro_spec 파트------------------------------------------------------

@api_view(['POST'])
def macro_list(request, format=None):
    try:
        Userid = request.data['UserID']
        MachineID = request.data['MachineID']
        MachineKey = request.data['MachineKey']
        if MachineKey != 'pass':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        r_value = request.data['r_value']
        edgeadd = request.data['edgeadd']

        # 매크로 함수 호출
        if request.data['sizekind'] == 'EA' or 'UA':
            res = mdlPosAngle.func_ang_pose(r_value, edgeadd)
            return Response(res)
        if request.data['sizekind'] == 'CH':
            res = mdlPosChannel.func_channel_pose(r_value, edgeadd)
            return Response(res)
        if request.data['sizekind'] == 'IB' or 'HB':
            res = mdlPosHFlange.func_hflange_pose(r_value, edgeadd)
            return Response(res)
        if request.data['sizekind'] == 'PI':
            res = mdlPosPipe36.func_pipe36_pose(r_value, edgeadd)
            return Response(res)
    except:
        return Response({'massage': 'MacorList_Error'})


# ubolt_spec 파트

@api_view(['GET', 'POST'])
def ubolt_list(request, format=None):
    if request.method == 'GET':
        uboltdata = UboltSpec.objects.all()
        serializer = UboltSpecSerializer(uboltdata, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UboltSpecSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ubolt_detail(request, pk, format=None):
    try:
        uboltdata = UboltSpec.objects.get(pk=pk)
    except UboltSpec.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UboltSpecSerializer(uboltdata)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UboltSpecSerializer(uboltdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        uboltdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# all()	테이블 모든 데이터 셋 가져오기
# filter()	특정 조건에 부합하는 데이터셋 가져오기
# exclude()	특정 조건을 제외한 데이터셋 가져오기
# get()	특정 조건에 부합하는 1개의 데이터 가져오기
# count()	가져올 데이터의 개수 가져오기
# first()	첫번째 데이터 가져오기
# last()	가장 마지막 데이터 가져오기
# exists()	데이터 유무에 대한 결과(True, False)를 가져오기
# order_by()	특정 필드 순서대로 정렬


# class RegistrationAPI(generics.GenericAPIView):
#     serializer_class = CreateUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
#             body = {"message": "short field"}
#             return Response(body, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {
#                 "user": UserSerializer(
#                     user, context=self.get_serializer_context()
#                 ).data,
#                 "token": AuthToken.objects.create(user),
#             }
#         )
#
#
# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response(
#             {
#                 "user": UserSerializer(
#                     user, context=self.get_serializer_context()
#                 ).data,
#                 "token": AuthToken.objects.create(user)[1],
#             }
#         )
#
#
# class UserAPI(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
#
#     def get_object(self):
#         return self.request.user

# @api_view(['GET', 'POST'])
# def markdata_list(request, format=None):
#     if request.method == 'GET':
#         markdata = AutoMarkMachine.objects.filter(mark_ok=False).order_by('id')[:2]
#         serializer = MarkMachineSerializer(markdata, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = MarkMachineSerializer(data=request.data, nany=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

