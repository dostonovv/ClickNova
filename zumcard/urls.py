# zumcard/zumcard/urls.py — FINAL VERSIYA (RASMLAR ISHLAYDI!)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin0dostonov0zoirjo0click/', admin.site.urls),  # xavfsiz admin url
    path('', include('core.urls')),
    path('shop/', include('products.urls')),
    path('adminsupport/', include('support.urls')),
]

# <--- YANGI: DEBUG=False bo‘lganda ham media ishlaydi
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)