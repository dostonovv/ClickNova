import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zumcard.settings')

application = get_wsgi_application()

# Whitenoise qo‘sh — media fayllarni berish uchun
from whitenoise import WhiteNoise
from django.conf import settings  # <--- BU QATORNI QO‘SH!

application = WhiteNoise(application, root=settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)