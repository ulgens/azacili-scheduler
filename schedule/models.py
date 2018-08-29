from django.db import models
from django.utils.translation import ugettext as _


DAY_OF_THE_WEEK = (
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
    (7, _('Sunday')),
)


class Instructor(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.code


class Program(models.Model):
    name = models.CharField(max_length=64, verbose_name="Bölüm Adı")
    code = models.CharField(max_length=8, verbose_name="Bölüm Kodu")

    def __str__(self):
        return self.code


class Course(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Section(models.Model):
    is_active = models.BooleanField(default=True)

    code = models.IntegerField(verbose_name="CRN")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    lecturer = models.ForeignKey(Instructor, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.code)


class Lesson(models.Model):
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(null=True)

    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    building = models.ForeignKey(Building, on_delete=models.PROTECT, null=True)
    room = models.CharField(max_length=16, null=True)
    day = models.PositiveSmallIntegerField(choices=DAY_OF_THE_WEEK, null=True)
    start_time = models.TimeField(verbose_name="Ders başlangıç saati", null=True)
    end_time = models.TimeField(verbose_name="Ders bitiş saati", null=True)

    def __str__(self):
        return f"{self.get_day_display()}: {self.start_time} - {self.end_time}"
