from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from api import urls as api_urls
from schedule.views import SchedulerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),

    path('scheduler', SchedulerView.as_view(), name="scheduler"),
    path('', RedirectView.as_view(url=reverse_lazy("scheduler"))),
    path('dersprogrami/', RedirectView.as_view(url=reverse_lazy("scheduler"))),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
