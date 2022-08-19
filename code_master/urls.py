from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('mark_excel_data/', views.UploadExcelData.as_view()),
    path('mark_list/', views.MarkList.as_view()),
    path('mark_gselect/', views.MarkGselect.as_view()),
    path('mark_gcancle/', views.MarkGcancle.as_view()),
    path('mark_data_load/', views.MarkDataLoad.as_view()),
    path('marked_data/', views.MarkedData.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)