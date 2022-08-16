from django.contrib import admin


# 공통 =======================================================================================
from django.contrib.auth.models import User
from machine.models import Machine
from machine.models import MachineOperator

#=============================================================================================
# 로봇 형강 가공기
from code_master.models import RobotCuttingMachine
@admin.register(RobotCuttingMachine)
class RobotCuttingMachineAdmin(admin.ModelAdmin):


    change_form_template = "admin/code_master/RobotCuttingMachine/_change_form.html"
    change_list_template = "admin/code_master/RobotCuttingMachine/_change_list.html"

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()
        #SHS
        if request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(author=request.user)
            return qs

    #get_form 또는 formfield_for_foreignkey 사용가능
    def get_form(self, request, obj=None, **kwargs):

        form = super(RobotCuttingMachineAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        else:
            form.base_fields['author'].queryset = User.objects.filter(id=request.user.id)

            operatorA = MachineOperator.objects.filter(user_id=request.user)

            machines = []
            for machineA in operatorA:
                machines.append(machineA.machine_id.id)

            form.base_fields['machine_id'].queryset = Machine.objects.filter(id__in=machines)
            return form



#=============================================================================================
# 자동 도트 마킹기

from code_master.models import AutoMarkMachine
@admin.register(AutoMarkMachine)
class MarkMachineAdmin(admin.ModelAdmin):
    # list_display = ("markdata", "machine_id", "ship_no", "por_no", "seq_no", "block_no", "pcs_no", "paint_code",
    #                 "lot_no", "work_quantity" "author")

    change_form_template = "admin/code_master/AutoMarkMachine/_change_form.html"
    change_list_template = "admin/code_master/AutoMarkMachine/_change_list.html"


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
#=============================================================================================
# 자동 프레스 라인

from code_master.models import AutoPressMachine
@admin.register(AutoPressMachine)
class AutoPressMachineAdmin(admin.ModelAdmin):
    # list_display = ("markdata", "machine_id", "ship_no", "por_no", "seq_no", "block_no", "pcs_no", "paint_code",
    #                 "lot_no", "work_quantity" "author")

    change_form_template = "admin/code_master/AutoPressMachine/_change_form.html"
    change_list_template = "admin/code_master/AutoPressMachine/_change_list.html"


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