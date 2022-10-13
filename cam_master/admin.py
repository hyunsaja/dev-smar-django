from django.contrib import admin
from .models import PlateChamferMachine, RpcmS300Machine, RpcmAgcutMachine
from .models import CoamingMachine, MijuRobotWeldingMachine

#===============================================================================
# 1. Plate Chamfer Machine
# ==============================================================================

@admin.register(PlateChamferMachine)
class PlateChamferMachineAdmin(admin.ModelAdmin):
    list_display = ("id",  "origin_image", "result_image", "ncfile", "updated_at")

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            return

#===============================================================================
# 2. Rpcm S300 Machine
# ==============================================================================

@admin.register(RpcmS300Machine)
class RpcmS300MachineAdmin(admin.ModelAdmin):
    list_display = ("id",  "origin_image", "result_image", "ncfile", "updated_at")

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            return

#===============================================================================
# 3. Rpcm Agcut Machine
# ==============================================================================

@admin.register(RpcmAgcutMachine)
class RpcmAgcutMachineAdmin(admin.ModelAdmin):
    list_display = ("id",  "origin_image", "result_image", "ncfile", "updated_at")

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            return

#===============================================================================
# 4. Coaming Machine
# ==============================================================================

@admin.register(CoamingMachine)
class CoamingMachineAdmin(admin.ModelAdmin):
    list_display = ("id",  "origin_image", "result_image", "ncfile", "updated_at")

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            return

#===============================================================================
# 5. Miju Robot Welding Machine
# ==============================================================================

@admin.register(MijuRobotWeldingMachine)
class MijuRobotWeldingMachineAdmin(admin.ModelAdmin):
    list_display = ("id",  "origin_image", "result_image", "ncfile", "updated_at")

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        #SHS
        if request.user.is_superuser:
            return qs
        else:
            return


