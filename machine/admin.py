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

#=============================================================================================
from machine.models import MachineOperator
@admin.register(MachineOperator)
class MachineOperatorAdmin(admin.ModelAdmin):
    list_display = ("id",
        "machine_id",
        "user_id",
        "description", "astatus", "adate",)