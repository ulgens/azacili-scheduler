from django.conf import settings
from django.db import models

from schedule.choices import Days

__all__ = (
    "Building",
    "Course",
    "Instructor",
    "Lesson",
    "Program",
    "Section",
)


class Building(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=8)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.code


class Course(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    program = models.ForeignKey(
        to="schedule.Program",
        on_delete=models.PROTECT,
        related_name="courses",
    )
    term = models.CharField(
        default=settings.ACTIVE_TERM,
        max_length=64,
        db_index=True,
    )

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(null=True)

    section = models.ForeignKey(
        to="schedule.Section",
        on_delete=models.PROTECT,
        related_name="lessons",
    )
    building = models.ForeignKey(
        "schedule.Building",
        on_delete=models.PROTECT,
        null=True,
        related_name="lessons",
    )
    room = models.CharField(max_length=16, null=True)
    day = models.PositiveSmallIntegerField(choices=Days.choices, null=True)
    start_time = models.TimeField(verbose_name="Ders başlangıç saati", null=True)
    end_time = models.TimeField(verbose_name="Ders bitiş saati", null=True)

    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time}"


class Program(models.Model):
    # name field is not used. SIS doesn't return names in program selection page.
    name = models.CharField(max_length=64, verbose_name="Bölüm Adı")
    code = models.CharField(max_length=8, verbose_name="Bölüm Kodu")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Section(models.Model):
    is_active = models.BooleanField(default=True)

    code = models.IntegerField(verbose_name="CRN")
    course = models.ForeignKey(
        "schedule.Course",
        on_delete=models.PROTECT,
        related_name="sections",
    )
    lecturer = models.ForeignKey(
        to="schedule.Instructor",
        on_delete=models.PROTECT,
        null=True,
        related_name="sections",
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return str(self.code)


