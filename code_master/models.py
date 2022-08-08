from django.db import models


# Create your models here.


# ---------------------------------------------------------
# 자재 정보
class MaterialSpec(models.Model):
    id = models.AutoField(primary_key=True)

    spec = models.CharField(max_length=32)
    m_param = models.JSONField()

    # texture = models.CharField(max_length=20)
    # m_kinds = models.CharField(max_length=20)
    # standard = models.CharField(max_length=20)
    # m_param = jsonfield.JSONField()

    description = models.CharField(max_length=128, null=True)
    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.spec

    class Meta:
        # managed = False
        db_table = "tb_material_spec"
        verbose_name_plural = "1. MaterialSpec"
        ordering = ["spec", ]


# -------------------------------------------------------------------------------
# 부재 가공정보
from django.contrib.auth.models import Group, User
from core.models import Code
from machine.models import Machine


class CodeMaster(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  # 장비ID
    ship_no = models.CharField(max_length=10)  # 호선
    por_no = models.CharField(max_length=10)  # POR
    seq_no = models.CharField(max_length=10)  # SQ
    pcs_no = models.CharField(max_length=10)  # 피스번호
    part_no = models.CharField(max_length=10)  # 부재번호
    quantity = models.IntegerField()  # 부재수량

    texture = models.IntegerField(
        choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=5).filter(aint__gt=-1))
    material_spec_id = models.ForeignKey(MaterialSpec, null=True,
                                         on_delete=models.CASCADE)
    # texture = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재재질 예)SS400
    # m_kind = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재종류 예)EA, UA, HB등
    # standard = models.ForeignKey(MaterialSpec, null=True, on_delete=models.CASCADE) # 자재규격 예)50*50*6T

    length_dwg = models.IntegerField()  # 도면상의 자재길이
    length_cut = models.IntegerField()  # 실제 가공길이
    mark_info = models.CharField(max_length=30)  # 마킹정보

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL)  # 데이터 입력자
    created_at = models.CharField(max_length=20)  # 자재재질 예)SS400
    worked_at = models.DateTimeField(blank=True, null=True)  # 작업일자
    worked_cnt = models.IntegerField(default=0)  # 작업한수량
    work_select = models.BooleanField(default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    # 작업 지시 선택시 ship, por, sq, pcs, part 항목별로 선택할 수 있게끔 함(좌로부터 1대N 관계)

    part_point = models.IntegerField()  # 가공포인트수(자동계산)

    cutlist = models.JSONField(blank=True,
                               null=True)  # 가공리스트 #SHS 나중에 null false로 수정
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨
    # 매크로명은 매크로 DB에서 불러옴
    description = models.CharField(max_length=128, null=True)
    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.ship_no

    class Meta:
        # managed = False
        db_table = "tb_field_master"
        verbose_name_plural = "2. FieldMaster"
        ordering = ["machine_id", "ship_no", "por_no", "seq_no", "pcs_no",
                    "part_no", ]