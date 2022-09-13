from django.contrib import admin


# 공통 =======================================================================================
from django.contrib.auth.models import User
from machine.models import Machine
from machine.models import MachineOperator

#===============================================================================
# 1. 자동 도트 마킹기
# ==============================================================================

from code_master.models import AutoMarkMachine
@admin.register(AutoMarkMachine)
class MarkMachineAdmin(admin.ModelAdmin):
    list_display = ("mark_data",  "work_quantity", "worked_quantity", "work_select", "status", "updated_at")

    change_form_template = "admin/code_master/AutoMarkMachine/_change_form.html"
    change_list_template = "admin/code_master/AutoMarkMachine/_change_list.html"

    def changelist_view(self, request, extra_context=None):

        if request.user.id == 2 or request.user == 3:
            param = 2  # 1로 하면 수동 선택 ,2는 자동으로 머신id 넘김
            mid =1     # 미주꼬리표마킹기 machine_id = 1
        else:
            param = 1
            mid = 1

        operatorA = MachineOperator.objects.filter(user_id=request.user)
        machines = []
        for machineA in operatorA:
            machines.append(machineA.machine_id.id)
        print(request.user)

        extra_context = {
            'extra_Param': param,
            'extra_machines': list(Machine.objects.filter(id__in=machines)),
            'mid' : mid
        }

        shs = super(MarkMachineAdmin, self).changelist_view(
            request, extra_context=extra_context)
        return shs

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(author=request.user)
            return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super(MarkMachineAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        else:
            form.base_fields['author'].queryset = User.objects.filter(id=request.user.id)

            operatorA = MachineOperator.objects.filter(user_id=request.user)

            machines = []
            for machineA in operatorA:
                machines.append(machineA.machine_id.id)

            form.base_fields['machine_id'].queryset = Machine.objects.filter(id__in = machines)
            return form


#filter(gnumber=3 && gsubNumber=2 && Deep=1)
#===============================================================================
# 3. 자동 프레스 라인
# ==============================================================================
from django.utils.html import format_html
from code_master.models import AutoPressMachine
@admin.register(AutoPressMachine)
class AutoPressMachineAdmin(admin.ModelAdmin):
    list_display = ("view_data",  "show_firm_url", "work_quantity", "worked_quantity", "work_select", "status", "updated_at")

    change_form_template = "admin/code_master/AutoPressMachine/_change_form.html"
    change_list_template = "admin/code_master/AutoPressMachine/_change_list.html"


    def show_firm_url(self, obj):
        #return format_html("<a href='%s/svgEdit/'>%s</a>" % (obj.id, "svgEdit"))
        return format_html("<a href='#' onclick=\"editSVG('%s');\">%s</a>" % (obj.id, "svgEdit"))
    show_firm_url.short_description = "Firm URL"


    def changelist_view(self, request, extra_context=None):

        if request.user.id == 4 or request.user == 5:
            param = 2  # 1로 하면 수동 선택 ,2는 자동으로 머신id 넘김
            mid =3     # 미주꼬리표마킹기 machine_id = 1
        else:
            param = 1
            mid = 3

        operatorA = MachineOperator.objects.filter(user_id=request.user)
        machines = []
        for machineA in operatorA:
            machines.append(machineA.machine_id.id)
        print(request.user)

        extra_context = {
            'extra_Param': param,
            'extra_machines': list(Machine.objects.filter(id__in=machines)),
            'mid' : mid
        }

        shs = super(AutoPressMachineAdmin, self).changelist_view(
            request, extra_context=extra_context)
        return shs


    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            #qs = qs.filter(author__user=request.user)
            qs = qs.filter(author=request.user)
            return qs

    #get_form 또는 formfield_for_foreignkey 사용가능
    def get_form(self, request, obj=None, **kwargs):
        form = super(AutoPressMachineAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        else:
            form.base_fields['author'].queryset = User.objects.filter(id=request.user.id)

            operatorA = MachineOperator.objects.filter(user_id=request.user)

            machines = []
            for machineA in operatorA:
                machines.append(machineA.machine_id.id)

            form.base_fields['machine_id'].queryset = Machine.objects.filter(id__in = machines)
            return form



#===============================================================================
# 2. 로봇 플라즈마 컷팅 머신 ( 앵글 전용기 )
# ==============================================================================

from code_master.models import RpcagMachine
@admin.register(RpcagMachine)
class RpcagMachineAdmin(admin.ModelAdmin):
    list_display = ("view_data",  "show_firm_url", "work_quantity", "worked_quantity", "work_select", "status", "updated_at")

    change_form_template = "admin/code_master/RobotAgCuttingMachine/_change_form.html"
    change_list_template = "admin/code_master/RobotAgCuttingMachine/_change_list.html"


    def show_firm_url(self, obj):
        #return format_html("<a href='%s/svgEdit/'>%s</a>" % (obj.id, "svgEdit"))
        return format_html("<a href='#' onclick=\"editSVG('%s');\">%s</a>" % (obj.id, "svgEdit"))
    show_firm_url.short_description = "Firm URL"


    def changelist_view(self, request, extra_context=None):

        if request.user.id == 2 or request.user == 3:
            param = 2  # 1로 하면 수동 선택 ,2는 자동으로 머신id 넘김
            mid = 2     # 미주꼬리표마킹기 machine_id = 1
        else:
            param = 1
            mid = 2

        operatorA = MachineOperator.objects.filter(user_id=request.user)
        machines = []
        for machineA in operatorA:
            machines.append(machineA.machine_id.id)
        print(request.user)

        extra_context = {
            'extra_Param': param,
            'extra_machines': list(Machine.objects.filter(id__in=machines)),
            'mid': mid
        }

        shs = super(RpcagMachineAdmin, self).changelist_view(
            request, extra_context=extra_context)
        print(mid)
        return shs


    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            #qs = qs.filter(author__user=request.user)
            qs = qs.filter(author=request.user)
            return qs

    #get_form 또는 formfield_for_foreignkey 사용가능
    def get_form(self, request, obj=None, **kwargs):
        form = super(RpcagMachineAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        else:
            form.base_fields['author'].queryset = User.objects.filter(id=request.user.id)

            operatorA = MachineOperator.objects.filter(user_id=request.user)

            machines = []
            for machineA in operatorA:
                machines.append(machineA.machine_id.id)

            form.base_fields['machine_id'].queryset = Machine.objects.filter(id__in = machines)
            return form