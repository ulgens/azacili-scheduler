from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from api import urls as api_urls
from schedule.views import SchedulerView, LoginView, save_courses

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),

    path('scheduler', SchedulerView.as_view(), name="scheduler"),
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('dersprogrami', RedirectView.as_view(url=reverse_lazy("scheduler"))),
    path('save', save_courses, name="save-courses"),

    path('', include('social_django.urls', namespace='social')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
