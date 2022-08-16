from django.db import models
from django.contrib.auth.models import User
import jsonfield



# ---------------------------------------------------------
# 회사 정보
    # 회사명, 대표자, 대표메일, 사업자등록번호, 계산서 메일, 주소, 전화번호, 팩스번호


# ---------------------------------------------------------
# 사용자 정보
    # 이름, 회사명, 이메일, 모바일 ...

# ---------------------------------------------------------
# 장비 정보
    # 장비명, 회사명 ...


# ---------------------------------------------------------
# 자재 정보
class MaterialSpec(models.Model):
    m_kinds = models.CharField(max_length=20)
    standard = models.CharField(max_length=20)
    texture = models.CharField(max_length=20)
    m_param = jsonfield.JSONField()

# -------------------------------------------------------------------------------
# 부재 가공정보
class FieldMaster(models.Model):
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE) # 장비ID
    ship_no = models.CharField(max_length=10) # 호선
    por_no = models.CharField(max_length=10) # POR
    seq_no = models.CharField(max_length=10) # SQ
    pcs_no = models.CharField(max_length=10) # 피스번호
    part_no = models.CharField(max_length=10) # 부재번호
    material = models.CharField(max_length=10, null=True) # 호선-Por-Seq-Pcs-PartNo
    quantity = models.IntegerField() # 부재수량
    m_kind = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재종류 예)EA, UA, HB등
    standard = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재규격 예)50*50*6T
    texture = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재재질 예)SS400
    length_dwg = models.IntegerField() # 도면상의 자재길이
    length_cut = models.IntegerField() # 실제 가공길이
    mark_info = models.CharField(max_length=30) # 마킹정보

    created_at = models.DateTimeField(auto_now_add=True) # 생성일자
    updated_at = models.DateTimeField(auto_now=True) # 수정일자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # 데이터 입력자
    created_at = models.CharField(max_length=20) # 자재재질 예)SS400
    worked_at = models.DateTimeField(blank=True, null=True) # 작업일자
    worked_cnt = models.IntegerField(default=0) # 작업한수량
    work_select = models.BooleanField(default=False) # 작업지시 : 선텍한 놈만 장비에 내려줌
    # 작업 지시 선택시 ship, por, sq, pcs, part 항목별로 선택할 수 있게끔 함(좌로부터 1대N 관계)

    part_point = models.IntegerField() # 가공포인트수(자동계산)

    cutlist = jsonfield.JSONField() # 가공리스트
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨
    # 매크로명은 매크로 DB에서 불러옴