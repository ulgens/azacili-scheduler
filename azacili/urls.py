from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from schedule.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
