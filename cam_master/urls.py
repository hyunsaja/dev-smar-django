from django.urls import path, include
from . import views

urlpatterns = [
    path('plate_chamfer_result_img/', views.plate_chamfer_result_img),
    path('plate_chamfer_ncfile/', views.plate_chamfer_ncfile),
    path('plate_chamfer_camshot/', views.plate_chamfer_camshot),

    path('rpcm_s300_result_img/', views.rpcm_s300_result_img),
    path('rpcm_s300_ncfile/', views.rpcm_s300_ncfile),
    path('rpcm_s300_camshot/', views.rpcm_s300_camshot),

    path('rpcm_agcut_result_img/', views.rpcm_agcut_result_img),
    path('rpcm_agcut_ncfile/', views.rpcm_agcut_ncfile),
    path('rpcm_agcut_camshot/', views.rpcm_agcut_camshot),

    path('coaming_result_img/', views.coaming_result_img),
    path('coaming_ncfile/', views.coaming_ncfile),
    path('coaming_camshot/', views.coaming_camshot),

    path('miju_robot_welding_result_img/', views.miju_robot_welding_result_img),
    path('miju_robot_welding_ncfile/', views.miju_robot_welding_ncfile),
    path('miju_robot_welding_camshot/', views.miju_robot_welding_camshot),
]