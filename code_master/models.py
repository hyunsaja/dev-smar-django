from django.db import models


# Create your models here.

# from core.models import Company

# ==============================================================================
#1 자동 마킹기
# ==============================================================================


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

    mark_data = models.CharField(blank=True, null=True, max_length=50)  # 실제 마킹데이터

    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.ship_no

    class Meta:
        # managed = False
        db_table = "tb_dot_marking_machine"
        verbose_name_plural = "1. 자동도트마킹기"
        ordering = ["ship_no", "por_no", "seq_no", "block_no", "pcs_no"]


# ==============================================================================
# 2. 로봇 형강 가공기 ( 앵글 전용기 )
# ==============================================================================


class RpcagMachine(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)

    standard = models.CharField('자재규격', max_length=20)                       # 자재 규격
    texture = models.CharField('자재재질', max_length=10)                        # 자재 재질
    view_data = models.CharField('부재번호', unique=True, max_length=50)  # 화면에 뿌려줄 부재번호
    group_data = models.CharField('그룹번호', max_length=20)
    ship_no = models.CharField(max_length=10, blank=True, null=True) # 호선
    por_no = models.CharField(max_length=10, blank=True, null=True)  # 주문번호
    seq_no = models.CharField(max_length=10, blank=True, null=True)  # 주문세부번호
    block_no = models.CharField(max_length=10, blank=True, null=True)  # 블록번호
    pcs_no = models.CharField(max_length=10, blank=True, null=True)  # 피스번호
    part_no = models.CharField(max_length=10, blank=True, null=True)  # 부재번호
    weight = models.CharField(max_length=10, blank=True, null=True)  # 중량

    length_dwg = models.IntegerField()  # 입력 자재길이
    length_cut = models.IntegerField()  # 실제 가공자재길이(cut loss 감안하여 계산된 길이)

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField('작업일자', auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 데이터 입력자

    work_quantity = models.IntegerField('전체수량', default=1)  # 부재수량
    worked_quantity = models.IntegerField('작업수량', default=0)  # 작업한수량
    work_select = models.BooleanField('작업선택', default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    status = models.BooleanField('작업유무', default=False)  # 작업 완료 정보

    part_point = models.IntegerField(blank=True, null=True)  # 가공포인트수(자동계산)

    cutlist = models.JSONField()
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨


    description = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.view_data


    class Meta:
        # managed = False
        db_table = "tb_rpcag_machine"
        verbose_name_plural = "2. 로봇 앵글 가공기"
        ordering = ["view_data" ]


# ==============================================================================
# 3. 자동 프레스 라인
# ==============================================================================


class AutoPressMachine(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  #

    standard = models.CharField(max_length=10)                       # 자재 규격
    # texture = models.CharField(max_length=10)                       # 자재 재질
    ship_no = models.CharField(max_length=10, blank=True, null=True) # 호선
    por_no = models.CharField(max_length=10, blank=True, null=True)  # 주문번호
    seq_no = models.CharField(max_length=10, blank=True, null=True)  # 주문세부번호
    block_no = models.CharField(max_length=10, blank=True, null=True)  # 블록번호
    pcs_no = models.CharField(max_length=10, blank=True, null=True)  # 피스번호
    part_no = models.CharField(max_length=10)                        # 부재번호

    length_dwg = models.IntegerField()  # 입력 자재길이
    length_cut = models.IntegerField()  # 실제 가공자재길이(cut loss 감안하여 계산된 길이)

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField('작업일자', auto_now=True)  # 수정일자
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 데이터 입력자

    work_quantity = models.IntegerField('전체수량', default=1)  # 부재수량
    worked_quantity = models.IntegerField('작업수량', default=0)  # 작업한수량
    work_select = models.BooleanField('작업선택', default=False)  # 작업지시 : 선텍한 놈만 장비에 내려줌
    status = models.BooleanField('작업유무', default=False)  # 작업 완료 정보

    part_point = models.IntegerField(blank=True, null=True)  # 가공포인트수(자동계산)

    cutlist = models.JSONField()
    # cutlist : [{CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           {CUT:[가공거리, 매크로명, Param1, Param2, Param3, Param4, Param5]},
    #           ...]   가공수 만큼 증가됨

    view_data = models.CharField('부재번호', unique=True, null=True, max_length=50)  # 화면에 뿌려줄 부재번호

    description = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.view_data


    class Meta:
        # managed = False
        db_table = "tb_auto_press_machine"
        verbose_name_plural = "3. 자동프레스라인"
        ordering = ["ship_no", "por_no", "seq_no", "block_no", "pcs_no", "part_no" ]


# ==============================================================================
# 4. CAM Machine -------
# ==============================================================================

class SmartCamMachine(models.Model):
    id = models.AutoField(primary_key=True)
    cam_name = models.CharField(max_length=50, blank=True, null=True)
    cam_data = models.CharField(max_length=250, blank=True, null=True)
    origin_image = models.ImageField(upload_to='origin_image/%y/%m/%d')
    result_image = models.ImageField(upload_to='result_image/%y/%m/%d', blank=True, null=True)
    nc_file = models.FileField(upload_to='nc_file/%Y/%m/%d', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.cam_name} :: {self.origin_image} :: {self.result_image}'

    class Meta:
        # managed = False
        db_table = "tb_smart_cam_machine"
        verbose_name_plural = "**[Smart Cam Machine]**"
        ordering = ["-id", ]