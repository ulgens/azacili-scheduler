from django.contrib.auth.models import AbstractUser
from django.db import models

from schedule.models import Section


class User(AbstractUser):
    sections = models.ManyToManyField(Section)
