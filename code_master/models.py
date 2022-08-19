from django.db import models


# Create your models here.

# -------------------------------------------------------------------------------
# 부재 가공정보
from django.contrib.auth.models import Group, User
from core.models import Code
from machine.models import Machine
from core.models import Company


class RobotCuttingMachine(models.Model):
    id = models.AutoField(primary_key=True)
    # company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  # 장비ID

    ship_no = models.CharField(max_length=10)  # 호선
    por_no = models.CharField(max_length=10)  # POR
    seq_no = models.CharField(max_length=10)  # SQ
    block_no = models.CharField(max_length=10)  # 블럭넘버
    pcs_no = models.CharField(max_length=10)  # 피스번호
    part_no = models.CharField(max_length=10)  # 부재번호
    quantity = models.IntegerField()  # 부재수량

    texture = models.IntegerField(choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=2).filter(aint__gt=0))  # 자재 재질
    m_kind = models.IntegerField(choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=3).filter(aint__gt=0))  # 자재 종류
    standard = models.IntegerField(choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=4).filter(aint__gt=0))  # 자재 규격

    length_dwg = models.IntegerField()  # 도면상의 자재길이
    length_cut = models.IntegerField()  # 실제 가공길이
    mark_info = models.CharField(max_length=30)  # 마킹정보

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 데이터 입력자

    worked_cnt = models.IntegerField(default=0)  # 작업한수량
    work_select = models.BooleanField(default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    # 작업 지시 선택시 ship, por, sq, pcs, part 항목별로 선택할 수 있게끔 함(좌로부터 1대N 관계)

    part_point = models.IntegerField()  # 가공포인트수(자동계산)

    cutlist = models.JSONField(blank=True, null=True)  # 가공리스트 #SHS 나중에 null false로 수정
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨
    # 매크로명은 매크로 DB에서 불러옴
    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.ship_no

    # 단일 필드 작업시만 가능하므로 해당 내용 미적용함(save, delete 메서드)
    # def save(self, *args, **kwargs):
    #     self.material = self.ship_no + '-' + self.por_no + '-' + self.seq_no
    #     super(BizMaster, self).save(*args, **kwargs)

    class Meta:
        # managed = False
        db_table = "tb_robot_cutting_machine"
        verbose_name_plural = "1. 로봇형강가공기"
        ordering = ["machine_id", "ship_no", "por_no", "seq_no", "pcs_no", "part_no", ]


# -------------------------------------------------------------------------------
# 자동 마킹기
from django.contrib.auth.models import Group, User
from core.models import Code
from machine.models import Machine

class AutoMarkMachine(models.Model):
    id = models.AutoField(primary_key=True)
    # company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  # 장비ID

    # 엑셀 업로드 항목 start
    ship_no = models.CharField(max_length=10)  # 호선
    por_no = models.CharField(max_length=10)  # POR
    seq_no = models.CharField(max_length=10)  # SQ
    block_no = models.CharField(max_length=10)  # 블럭넘버
    pcs_no = models.CharField(max_length=10)  # 피스번호
    paint_code = models.CharField(max_length=10)  # 페인트코드
    lot_no = models.CharField(max_length=10, null=True)  # 로트번호
    work_quantity = models.IntegerField(default=1)  # 작업수량
    # 엑셀 업로드 항목 end

    # delevery = models.DateTimeField(blank=True, null=True)  # 납기일
    # description = models.CharField(max_length=128, null=True)  # 추가 마킹 정보

    worked_quantity = models.IntegerField(default=0)  # 작업한수량
    work_select = models.BooleanField(default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    status = models.BooleanField(default=False)  # 작업 완료 정보

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 데이터 입력자

    mark_data = models.CharField(null=True, max_length=50)  # 실제 마킹데이터

    def __str__(self):
        return self.ship_no

    class Meta:
        # managed = False
        db_table = "tb_dot_marking_machine"
        verbose_name_plural = "2. 자동도트마킹기"
        ordering = ["machine_id", "ship_no", "por_no", "seq_no", "block_no", "pcs_no"]


# ===========================================================================================
# 자동 프레스 라인

class AutoPressMachine(models.Model):
    id = models.AutoField(primary_key=True)
    # company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  # 장비ID

    # ship_no = models.CharField(max_length=10)  # 호선
    # por_no = models.CharField(max_length=10)  # POR
    # seq_no = models.CharField(max_length=10)  # SQ
    # block_no = models.CharField(max_length=10)  # 블럭넘버
    # pcs_no = models.CharField(max_length=10)  # 피스번호

    part_no = models.CharField(max_length=30)  # 부재번호
    quantity = models.IntegerField()  # 부재수량

    # texture = models.IntegerField(
    #     choices=Code.objects.values_list('aint', 'avarchar').filter(
    #         gNumber=2).filter(aint__gt=0))  # 자재 재질
    m_kind = models.IntegerField(
        choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=3).filter(aint__gt=0))  # 자재 종류
    standard = models.IntegerField(
        choices=Code.objects.values_list('aint', 'avarchar').filter(
            gNumber=4).filter(aint__gt=0))  # 자재 규격

    length_dwg = models.IntegerField()  # 도면상의 자재길이
    length_cut = models.IntegerField()  # 실제 가공길이
    # mark_info = models.CharField(max_length=30)  # 마킹정보

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL)  # 데이터 입력자

    worked_cnt = models.IntegerField(default=0)  # 작업한수량
    work_select = models.BooleanField(default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌

    part_point = models.IntegerField()  # 가공포인트수(자동계산)

    cutlist = models.JSONField()  # 가공리스트 #SHS 나중에 null false로 수정
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨
    # 매크로명은 매크로 DB에서 불러옴
    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.ship_no

    # 단일 필드 작업시만 가능하므로 해당 내용 미적용함(save, delete 메서드)
    # def save(self, *args, **kwargs):
    #     self.material = self.ship_no + '-' + self.por_no + '-' + self.seq_no
    #     super(BizMaster, self).save(*args, **kwargs)

    class Meta:
        # managed = False
        db_table = "tb_auto_press_machine"
        verbose_name_plural = "3. 자동 프레스 라인"
        ordering = ["machine_id", "part_no", ]
