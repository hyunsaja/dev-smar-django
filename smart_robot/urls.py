
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('code_master/', include('code_master.urls')),
]
    # path('biz_master/', include('biz_master.urls')),
    # path('cam_master/', include('cam_master.urls')),
    # path('bot_master/', include('robot_master.urls')),
