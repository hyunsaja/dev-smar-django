from django.db import models

# Create your models here.

# -------------------------------------------------------------------------------
# 부재 가공정보
from django.contrib.auth.models import User
from core.models import Code
from machine.models import Machine
from core.models import Company

# ===========================================================================================
# 자동 프레스 라인

class AutoPressMachine(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  #

    standard = models.CharField(max_length=10)  # 자재 규격
    texture = models.CharField(max_length=10, blank=True, null=True)  # 자재 규격
    ship_no = models.CharField(max_length=10, blank=True, null=True)  # 호선
    por_no = models.CharField(max_length=10, blank=True, null=True)  # 주문번호
    seq_no = models.CharField(max_length=10, blank=True, null=True)  # 주문세부번호
    pcs_no = models.CharField(max_length=10, blank=True, null=True)  # 피스번호
    part_no = models.CharField(max_length=30)  # 부재번호

    length_dwg = models.IntegerField()  # 입력 자재길이
    length_cut = models.IntegerField()  # 실제 가공자재길이(cut loss 감안하여 계산된 길이)

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL)  # 데이터 입력자

    work_quantity = models.IntegerField()  # 가공할 부재수량
    worked_quantity = models.IntegerField(default=0)  # 가공 작업한 수량(실적)
    work_select = models.BooleanField(default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    status = models.BooleanField(default=False)  # 작업 완료 정보

    part_point = models.IntegerField()  # 가공포인트수

    cutlist = models.JSONField()  # 가공리스트 #SHS 나중에 null false로 수정
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨

    description = models.CharField(max_length=128, null=True)


    def __str__(self):
        return self.ship_no

    class Meta:
        # managed = False
        db_table = "tb_auto_press_machine"
        verbose_name_plural = "3. 자동프레스라인"
        ordering = ["ship_no", "por_no", "seq_no", "pcs_no", "part_no"]
