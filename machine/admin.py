from django.contrib import admin

# Register your models here.

#=============================================================================================
from machine.models import MachineGroup
@admin.register(MachineGroup)
class MachineGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "astatus", "adate",)


#=============================================================================================
from machine.models import Machine
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("id", "company_id", "machine_group_id", "name", "description", "astatus", "adate",)



#=============================================================================================
from machine.models import MachineInit
@admin.register(MachineInit)
class MachineInitAdmin(admin.ModelAdmin):
    list_display = ("id", "machine_id",
        "set_value_1", "set_value_2",
        "set_value_3", "set_value_4",
        "description", "astatus", "adate",)


# =============================================================================================
from machine.models import MachineOperator
from django.contrib.auth.models import Group, User
from core.models import UserDetail


@admin.register(MachineOperator)
class MachineOperatorAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "machine_id",
                    "user_id",
                    "description", "astatus", "adate",)

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()

        # SHS
        if request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(user_id=request.user.id)
            return qs

    # get_form 또는 formfield_for_foreignkey 사용가능
    def get_form(self, request, obj=None, **kwargs):

        form = super(MachineOperatorAdmin, self).get_form(request, obj,
                                                          **kwargs)
        if request.user.is_superuser:
            return form
        else:
            currentUser = UserDetail.objects.get(user=request.user)

            companyUser = UserDetail.objects.get(company=currentUser.company)
            form.base_fields['user_id'].queryset = User.objects.filter(
                id__in=[companyUser.user.id])

            form.base_fields['machine_id'].queryset = Machine.objects.filter(
                company_id=currentUser.company)

            return form