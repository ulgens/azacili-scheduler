from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.views import ProgramViewset


router = DefaultRouter()
router.register("programs", ProgramViewset)

urlpatterns = [
    url(r'', include(router.urls))
]
