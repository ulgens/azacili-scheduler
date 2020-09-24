from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import CourseSerializer, ProgramSerializer, SectionSerializer
from schedule.models import Course, Program, Section


class ProgramViewset(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    @action(detail=True)
    def courses(self, request, pk=None):
        courses = Course.objects.filter(
            program_id=pk,
            term=settings.ACTIVE_TERM,
        )
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)


class CourseViewset(ReadOnlyModelViewSet):
    queryset = Course.objects.filter(term=settings.ACTIVE_TERM)
    serializer_class = CourseSerializer

    @action(detail=True)
    def sections(self, request, pk=None):
        sections = Section.objects.filter(
            course_id=pk,
        ).select_related(
            "lecturer",
        ).prefetch_related(
            "lessons",
            "lessons__building",
        )
        serializer = SectionSerializer(sections, many=True)

        return Response(serializer.data)


