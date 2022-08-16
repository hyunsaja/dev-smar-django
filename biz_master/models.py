from django.db import models
from django.contrib.auth.models import User

from core.models import Company

# ---------------------------------------------------------
# 수주 정보
class BizMaster(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    # 수주파일 다운로드(현대삼호 기준) --- blank=True, null=True
    ship_no = models.CharField(max_length=10, blank=True, null=True)
    por_no = models.CharField(max_length=10, blank=True, null=True)
    seq_no = models.CharField(max_length=10, blank=True, null=True)
    Contract_no = models.CharField(max_length=20, blank=True, null=True) # 계약번호
    average_weight = models.CharField(max_length=10, blank=True, null=True) # 단중
    total_weight = models.CharField(max_length=10, blank=True, null=True) # 총 중량
    quantity = models.CharField(max_length=10, blank=True, null=True) # 계약량
    price = models.CharField(max_length=20, blank=True, null=True) # 계약금액
    stock_amount = models.CharField(max_length=20, blank=True, null=True) # 입고량
    item_standard = models.CharField(max_length=50, blank=True, null=True) # 품명/재질/규격
    activity = models.CharField(max_length=20, blank=True, null=True) # ACTIVITY
    required_department = models.CharField(max_length=20, blank=True, null=True) # 소요부서
    maker = models.CharField(max_length=20, blank=True, null=True) # 제작업체
    treatment_company = models.CharField(max_length=20, blank=True, null=True) # 후처리업체
    por_pub_date = models.DateTimeField(blank=True, null=True) # por발행일
    contract_date = models.DateTimeField(blank=True, null=True) # 계약일
    mp_deliverty = models.DateTimeField(blank=True, null=True) # MP납기
    make_qc_limit_date = models.DateTimeField(blank=True, null=True) # 제작검사_시한
    make_qc_complate_date = models.DateTimeField(blank=True, null=True) # 제작검사_완료
    make_qc_diff_date = models.CharField(max_length=20, blank=True, null=True) # 제작검사_차이
    packing_qc_limit_date = models.DateTimeField(blank=True, null=True) # 포장검사_시한
    packing_qc_complate_date = models.DateTimeField(blank=True, null=True) # 포장검사_완료
    packing_qc_diff_date = models.CharField(max_length=20, blank=True, null=True) # 포장검사_차이
    production_resorve_date = models.DateTimeField(blank=True, null=True) # 제작관리_예약
    production_take_limit_date = models.DateTimeField(blank=True, null=True) # 제작관리_인계시한
    production_tack_date = models.DateTimeField(blank=True, null=True) # 제작관리 _인계입고
    production_arrival_date = models.DateTimeField(blank=True, null=True) # 제작관리 _입고
    production_diff_date = models.CharField(max_length=20, blank=True, null=True) # 제작관리_차이
    treatment_resolve_date = models.DateTimeField(blank=True, null=True) # 후처리_예약
    treatment_limit_date = models.DateTimeField(blank=True, null=True) # 후처리_시한
    treatment_complete_date = models.DateTimeField(blank=True, null=True) # 후처리_완료
    treatment_arrival_date = models.DateTimeField(blank=True, null=True) # 후처리_입고
    delevery_request_date = models.DateTimeField(blank=True, null=True) # 자재배송_요청
    delevery_complete_date = models.DateTimeField(blank=True, null=True) # 자재배송_완료
    delevery_difference_date = models.CharField(max_length=20, blank=True, null=True) # 자재배송_차이
    delevery_request_no = models.CharField(max_length=20, blank=True, null=True) # 배송요청번호
    delevery_request_place = models.CharField(max_length=20, blank=True, null=True) # 배송요청장소
    delevery_request_man = models.CharField(max_length=20, blank=True, null=True) # 배송요청자
    delevery_request_contact = models.CharField(max_length=20, blank=True, null=True) # 배송요청자 연락처
    delevery_request_department = models.CharField(max_length=20, blank=True, null=True)# 배송요청부서
    delevery_manager = models.CharField(max_length=20, blank=True, null=True) # 배송담당자
    give_request_no = models.CharField(max_length=20, blank=True, null=True) # 사급요청번호
    give_request_date = models.DateTimeField(blank=True, null=True) # 사급요청일
    give_request_company = models.CharField(max_length=20, blank=True, null=True) # 사급업체
    mppl  = models.CharField(max_length=20, blank=True, null=True) # MPPL 공사
    mppl_no = models.CharField(max_length=20, blank=True, null=True) # MPPL NO
    mppl_seq = models.CharField(max_length=20, blank=True, null=True) # MPPL SEQ
    purchase_manager = models.CharField(max_length=20, blank=True, null=True) # 구매담당

    # 작업선택 및 작업실적 데이터
    work_select = models.BooleanField(default=False)
    worked_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'[{self.pk}] {self.Material} :: {self.worked_date} :: {self.UserID}'


'''
# -------------------------------------------------------------------------------
# 피스정보
class CodeMaster(models.Model):
    # json 입력 데이터
    UserID = models.CharField(max_length=50)
    # MachineID = models.CharField(max_length=50)
    # material = ship_no ~ por_no - seq_no ~ pcs_no
    Material = models.CharField(max_length=50)
    quantity = models.CharField(max_length=3)
    work_date = models.CharField(max_length=30, blank=True, null=True)
    work_info = models.CharField(max_length=20, blank=True, null=True)
    creation_date = models.CharField(max_length=30, blank=True, null=True)
    update_date = models.CharField(max_length=30, blank=True, null=True)
    part = jsonfield.JSONField()
    # 가공기 실적 데이터
    worked_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}] {self.Material} :: {self.worked_date} :: {self.UserID}'
'''
