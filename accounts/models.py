from django.contrib.auth.models import AbstractUser
from django.db import models

from schedule.models import Section


class User(AbstractUser):
    sections = models.ManyToManyField(Section)

    class Meta(AbstractUser.Meta):
        ordering = ("-date_joined", )

