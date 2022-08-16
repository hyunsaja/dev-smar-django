from django.urls import path, include
from . import views

urlpatterns = [
    path('result_img/', views.result_img),
    path('ncfile/', views.ncfile),
    path('camshot/', views.camshot),
    # path('camshot_detail/', views.camshot_detail),
]