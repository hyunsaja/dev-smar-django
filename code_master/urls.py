from django.urls import path
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('mark_excel_data/', views.UploadExcelData.as_view(), name="ExcelUPload"),
    path('work_data_load/', views.MworkDataLoad.as_view()),
    path('mark_gselect/', views.MarkGselect.as_view()),
    path('mark_all_select/', views.MarkAselect.as_view()),
    path('mark_gcancle/', views.MarkGcancle.as_view()),
    path('mark_data_load/', views.MarkDataLoad.as_view()),
    path('marked_data/', views.MarkedData.as_view()),

    path('press_cutting_view/', views.PressCuttingView.as_view()),
    path('press_excel_data/', views.UploadPressExcelData.as_view(), name="pressExcelUPload"),
    path('press_work_data_load/', views.PressWorkDataLoad.as_view()),
    path('press_gselect/', views.PressGselect.as_view()),
    path('press_allselect/', views.PressASelect.as_view()),
    path('press_allcancle/', views.PressGcancle.as_view()),
    path('press_worked_data/', views.PressWorkedData.as_view()),
    path('press_part_data_load/', views.PressPartDataLoad.as_view()),
    path('press_part_data_optimize/', views.PressPartDataOptimize.as_view()),
    path('press_cut_data_load/', views.PressCutDataLoad.as_view()),

    path('rpcag_cutting_view/', views.RpcagCuttingView.as_view()),
    path('rpcag_json_data/', views.UploadRpcagJsonData.as_view(), name="rpcagJsonUPload"),
    path('rpcag_work_data_load/', views.RpcagWorkDataLoad.as_view()),
    path('rpcag_req_material/', views.RpcagReqMaterial.as_view()),
    path('rpcag_part_data_load/', views.RpcagPartDataLoad.as_view()),
    path('rpcag_gselect/', views.RpcagGselect.as_view()),
    path('rpcag_allselect/', views.RpcagASelect.as_view()),
    path('rpcag_allcancle/', views.RpcagAcancle.as_view()),
    path('rpcag_worked_data/', views.RpcagWorkedData.as_view()),
    path('rpcag_cut_data_load/', views.RpcagCutDataLoad.as_view()),
    path('rpcag_material_spec/', views.RpcagMaterialSpec.as_view()),
    path('rpcag_speed_spec/', views.RpcagSpeedSpec.as_view()),
    path('rpcag_camshot/', views.RpcagCamshot.as_view()),

    path('rpcm_camshot/', views.RpcmCamshot.as_view()),

]
# urlpatterns = format_suffix_patterns(urlpatterns)