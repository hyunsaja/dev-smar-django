from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('hello/', views.hello),
    path('cutting_list/', views.cutting_list),
    path('init_list/', views.init_list),
    path('material_list/', views.material_list),
    path('speed_list/', views.speed_list),
    path('macro_list/', views.macro_list),
    path('ubolt_list/', views.ubolt_list),
    path('ubolt_detail/<str:pk>/', views.ubolt_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)