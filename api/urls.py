from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.views import ProgramViewset, CourseViewset


router = DefaultRouter()
router.register("programs", ProgramViewset)
router.register("courses", CourseViewset)

urlpatterns = [
    url(r'', include(router.urls))
]
