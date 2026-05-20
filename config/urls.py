from django.contrib import admin
from django.urls import path, include
from store import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ All routes handled by store app
    path('', include('store.urls')),

    path('online-payment/', views.online_payment, name='online_payment'),
    path('', include('store.urls')),
]

# ✅ MEDIA FILES (for images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)