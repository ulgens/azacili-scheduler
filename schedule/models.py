from django.db import models


class Lecturer(models.Model):
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
    name = models.CharField(max_length=32)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)


class Section(models.Model):
    code = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
