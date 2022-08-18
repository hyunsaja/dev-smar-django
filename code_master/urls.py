from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('mark_machine/', views.UploadExcelData.as_view()),
    # path('mark_machine/<int:pk>/', views.MarkMachine.as_view()),
    # path('ubolt_list/', views.ubolt_list),
    # path('ubolt_detail/<str:pk>/', views.ubolt_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)