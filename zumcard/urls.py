# zumcard/zumcard/urls.py — 100% ISHLAYDIGAN VERSIYA
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin0dostonov0zoirjo0click/', admin.site.urls),          # <--- BIRINCHI BO‘LSIN!
    path('', include('core.urls')),
    path('shop/', include('products.urls')),
    path('adminsupport/', include('support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)