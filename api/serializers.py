from rest_framework import serializers

from schedule.models import Program, Course


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    kod = serializers.CharField(source="code")
    ders_adi = serializers.CharField(source="name")

    class Meta:
        model = Course
        fields = ("id", "kod", "ders_adi")
