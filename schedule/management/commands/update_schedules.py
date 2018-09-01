from django.core.management.base import BaseCommand

from schedule.utils import update_buildings, update_courses, update_programs


class Command(BaseCommand):
    help = "Updates buildings, programs and courses."

    def handle(self, *args, **kwargs):
        update_programs()
        update_buildings()
        update_courses()
