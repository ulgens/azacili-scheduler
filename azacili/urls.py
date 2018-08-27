from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api import urls as api_urls
from schedule.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('', IndexView.as_view(), name="index"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
