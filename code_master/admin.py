from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.contrib import messages

from django.db.models import Max
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.urls import path, include
from django.utils.html import format_html
from django.contrib import messages

#=============================================================================================
from code_master.models import MaterialSpec
@admin.register(MaterialSpec)
class MaterialSpecAdmin(admin.ModelAdmin):
    #list_display = ("id", "texture", "m_kinds", "standard", "name", "name", 'description')
    list_display = ("id", "spec", "m_param", 'description')



#=============================================================================================
from code_master.models import CodeMaster
@admin.register(CodeMaster)
class FieldMasterAdmin(admin.ModelAdmin):
    list_display = ("id", "machine_id", "ship_no", "por_no", "seq_no", "pcs_no", "part_no", "quantity",
        "texture", "material_spec_id", "author")


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