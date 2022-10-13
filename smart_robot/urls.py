
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('code_master/', include('code_master.urls')),
    path('cam_master/', include('cam_master.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # path('biz_master/', include('biz_master.urls')),
    # path('bot_master/', include('robot_master.urls')),
