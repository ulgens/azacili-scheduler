from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import ProgramSerializer, CourseSerializer
from schedule.models import Program


class ProgramViewset(ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    @action(detail=True)
    def courses(self, request, pk=None):
        program = self.get_object()
        serializer = CourseSerializer(program.course_set.all(), many=True)

        return Response(serializer.data)



