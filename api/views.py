from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import CourseSerializer, ProgramSerializer, SectionSerializer
from schedule.models import Program, Course


class ProgramViewset(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    @action(detail=True)
    def courses(self, request, pk=None):
        program = self.get_object()
        serializer = CourseSerializer(program.course_set.all(), many=True)

        return Response(serializer.data)


class CourseViewset(ReadOnlyModelViewSet):
    queryset = Course.objects.filter()
    serializer_class = CourseSerializer

    @action(detail=True)
    def sections(self, request, pk=None):
        course = self.get_object()
        serializer = SectionSerializer(
            course.section_set.all().select_related(
                "lecturer",
            ).prefetch_related(
                "lesson_set",
                "lesson_set__building",
            ),
            many=True,
        )

        return Response(serializer.data)


