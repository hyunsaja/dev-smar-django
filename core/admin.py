from django.contrib import admin

# Register your models here.

from django.urls import path, include
from django.template.response import TemplateResponse
# from django.conf.urls import url
from django.urls import re_path as url 
from django.db.models import Max 
import datetime
from django.db.models import F
from django.utils.html import format_html
from django.db.models import Count
from django.contrib import messages

#=============================================================================================
#=============================================================================================


admin.site.site_header = 'SmartRobot'
admin.site.site_title = 'SmartRobot'
admin.site.title = 'SmartRobot'


from core.models import Code

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):

    # https://adriennedomingus.medium.com/adding-custom-views-or-templates-to-django-admin-740640cc6d42
    # Custom templates (designed to be over-ridden in subclasses)
    # add_form_template = None
    # change_form_template = None
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    # popup_response_template = None

    change_form_template = "admin/core/code/_change_form.html"
    change_list_template = "admin/core/code/_change_list.html"

    list_display = ("gNumber", "gSubNumber", "gDeep", "aNumber", "show_firm_url", "my_avarchar", "aint", "aint_count", "auser", "adate")
    search_fields = ("avarchar", )
    fields = ( "avarchar","aint", "atext")
    list_display_links = ['my_avarchar']
    list_per_page = 10

    # 펼침 기능 액센
    # messages 사용법
    def apply_send_device_actions(modeladmin, request, queryset):
        for item in queryset:
            print(item)
            messages.error(request, 'Error message  ' + str(item))
            messages.info(request, 'Error message  ' + str(item))

        # for book in queryset:
        #     book.price = book.price * decimal.Decimal('0.9')
        #     book.save()

    apply_send_device_actions.short_description = u'actions & messages 사용법'
    actions = [apply_send_device_actions, ]






    #SHS 댓글용
    is_reply = False

    # https://stackoverflow.com/questions/1949248/how-to-add-clickable-links-to-a-field-in-django-admin
    def show_firm_url(self, obj):
        return format_html("<a href='%s/reply/'>%s</a>" % (obj.aNumber, "Reply"))
    show_firm_url.short_description = "Firm URL"





    # get_queryset
    def aint_count(self, obj):
        return obj.aint

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            aint_count=Count("aint", distinct=True),
        )
        return queryset


    def my_avarchar(self, obj):
        return_value = ""
        for i in range(0, obj.gDeep):
            return_value = return_value + " &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "
        return_value = return_value + " > " + obj.avarchar
        return format_html(return_value)
    my_avarchar.empty_value_display = ""

    # overriding
    def get_urls(self):
        # urls = super(CourseAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super(CodeAdmin, self).get_urls()
        
        post_url = [
            path('<path:object_id>/reply/', self.admin_site.admin_view(self.reply_view), name='%s_%s_reply' % info),  #SHS 댓글용 추가
            path('a/', self.admin_site.admin_view(self.my_view)),
        ]
        #http://smapi.mynetgear.com:10288/admin/core/code/a/
        return post_url + urls


    # overriding 댓글용
    def add_view(self, request, form_url='', extra_context=None):
        self.is_reply = False   #SHS 댓글용
        return self.changeform_view(request, None, form_url, extra_context)

    # overriding 댓글용
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.is_reply = False   #SHS 댓글용
        return self.changeform_view(request, object_id, form_url, extra_context)
  
    # create 댓글용
    def reply_view(self, request, object_id, form_url='', extra_context=None):  #SHS 댓글용
        self.is_reply = True   #SHS 댓글용
        return self.changeform_view(request, object_id, form_url, extra_context)

    def my_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            # posts = Post.objects.all(),
            # key1 = value1,
            # key2 = value2,
            posts = "value",
        )
        print(context)
        return TemplateResponse(request, "admin/core/code/myView.html", {'ctx':context})

    #admin\options.py
    def save_model(self, request, obj, form, change):

        if self.is_reply:
            refObj = Code.objects.get(aNumber=obj.aNumber)
            print("----------------------------------")
            print(refObj)
            print("----------------------------------")
            obj.gNumber = (refObj.gNumber or 0)
            obj.gSubNumber = (refObj.gSubNumber or 0) + 1
            obj.gDeep = (refObj.gDeep or 0) + 1
            
            obj.aNumber = None
            obj.auser = request.user
            obj.astatus = 0
            obj.adate = datetime.datetime.now()

            Code.objects.filter(gNumber = refObj.gNumber, gSubNumber__gt=refObj.gSubNumber).update(gSubNumber = F('gSubNumber')  + 1)


        elif not change:  # Add
            refObj = Code.objects.aggregate(gNumber=Max('gNumber'))
            #obj.gNumber = (refObj.gNumber or 0) + 1
            obj.gNumber = (refObj['gNumber'] or 0) + 1
            obj.gSubNumber = 0
            obj.gDeep = 0
            obj.aNumber = None
            obj.auser = request.user
            obj.astatus = 0
            obj.adate = datetime.datetime.now()


        print("----------------------------------")
        print(obj)
        
        obj.save()  #실제 제장




#=============================================================================================
from core.models import Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "phone", "astatus", "adate",)
    





#=============================================================================================
#=============================================================================================


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserDetail

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserDetailInline(admin.StackedInline):
    model = UserDetail
    can_delete = False
    verbose_name_plural = 'UserDetail'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserDetailInline, )

    def get_inline_instances(self, request, obj=None):
            if not obj:
                return list()
            return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#=============================================================================================

from core.models import UserDetail
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "phone",)
    search_fields = ("user", )

