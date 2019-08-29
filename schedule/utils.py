# TODO:
#       - Add change detection for all updates and print them to logs
#       update_or_create doesn't return "if updated" information.


import datetime
import logging
from time import strptime

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from schedule.models import Building, Course, Instructor, Lesson, Program, Section

logger = logging.getLogger(__name__)

BASE_CATALOG_URL = settings.BASE_CATALOG_URL
BUILDINGS_URL = settings.BUILDINGS_URL


DAYS_TURKISH = {
    "pazartesi": 1,
    "salı": 2,
    "çarşamba": 3,
    "perşembe": 4,
    "cuma": 5,
    "cumartesi": 6,
    "pazar": 7,
}


def update_programs():
    r = requests.get(BASE_CATALOG_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get raw data
    program_options = soup.find("select").find_all("option")
    # Extract values
    program_options = map(lambda x: x.attrs["value"].strip(), program_options)
    # Remove empty items
    program_options = list(filter(lambda x: bool(x), program_options))
    # Sort alphabetically
    program_options = sorted(program_options)

    sis_program_count = len(program_options)
    db_program_count = Program.objects.count()

    logger.info("Programs:")
    logger.info(f"- {sis_program_count} programs came from SIS.")
    logger.info(f"- {db_program_count} programs found in database.")

    for option in program_options:
        program, created = Program.objects.get_or_create(code=option)

        if not created:
            logger.info(f"{program.code}.")
        else:
            logger.info(f"{program.code} - NEW")


    # Check if any program is removed from SIS
    codes = Program.objects.all().values_list("code", flat=True)
    removed_programs = set(codes) - set(program_options)

    if removed_programs:
        logger.warning(f"Following programs are removed from SIS: {','.join(removed_programs)}")


def update_buildings():
    # TODO:
    #       - Copy logging output from update_programs()
    r = requests.get(BUILDINGS_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    raw_table = soup.find_all("table")[-1]

    raw_buildings = raw_table.find_all("tr")

    for b in raw_buildings:
        rows = b.find_all("td")
        data = [row.get_text() for row in rows]

        building_code = data[0]
        building_name = data[1]
        building_name = " ".join(building_name.split())

        _, created = Building.objects.get_or_create(
            code=building_code,
            defaults={"name": building_name},
        )

        if created:
            logger.info(f"Building '{building_code}: {building_name}' has created.")


def update_courses(program_codes=None):
    # TODO:
    #       - Copy logging output from update_programs()

    # Update all programs as default behaviour
    if not program_codes:
        programs = Program.objects.all()
    else:
        programs = Program.objects.filter(code__in=program_codes)

    for program in programs.iterator():
        r = requests.get(BASE_CATALOG_URL + program.code)
        soup = BeautifulSoup(r.content, "html5lib")

        # Convert <br> to new line.
        # .get_text() doesn't handle br as new line
        for br in soup.find_all("br"):
            br.replace_with("\n")

        sections = Section.objects.filter(course__program=program)
        crns = sections.values_list()
        active_sections = sections.filter(is_active=True)

        raw_table = soup.find("table", class_="dersprg")
        # First two tr are title
        raw_courses = raw_table.find_all("tr")[2:]

        new_sections = []

        for course in raw_courses:
            rows = course.find_all("td")
            data = [row.get_text() for row in rows]

            section_code = int(data[0].strip())
            course_code = data[1].strip()
            course_name = data[2].strip()
            instructor_name = data[3].strip()
            buildings = data[4].strip()
            days = data[5].strip()
            times = data[6].strip()
            rooms = data[7].strip()

            # Import course
            course, course_created = Course.objects.get_or_create(
                code=course_code,
                program=program,
                term=settings.ACTIVE_TERM,
                defaults={"name": course_name},
            )

            if course_created:
                logger.info(f"Course '{course_code}: {course_name}' has created.")

            # Import instructor
            if instructor_name in ("***", "--"):
                instructor = None
            else:
                instructor, instructor_created = Instructor.objects.get_or_create(
                    name=instructor_name,
                )

                if instructor_created:
                    logger.info(f"Instructor '{instructor_name}' has created.")

            # Import section
            section, section_created = Section.objects.get_or_create(
                code=section_code,
                course=course,
                defaults={"lecturer": instructor},
            )

            if section_created:
                logger.info(f"Section '{section_code}' for {course_code} has created.")

            # Import lesson
            lesson_data = zip(buildings.split(), rooms.split(), days.split(), times.split())

            for index, (building, room, day, lesson_time) in enumerate(lesson_data, 1):

                if building == "---":
                    building = None
                else:
                    building, building_created = Building.objects.get_or_create(code=building)

                    if building_created:
                        logger.info(f"Building '{building.code}' has created.")

                if room == "---" or not room:
                    room = None

                if day == "----" or not day:
                    day = None
                else:
                    day = DAYS_TURKISH[day.lower()]

                try:
                    start_time, end_time = map(lambda x: strptime(x, "%H%M"), lesson_time.split("/"))
                except ValueError:
                    start_time = None
                    end_time = None
                else:
                    start_time = datetime.time(start_time.tm_hour, start_time.tm_min)
                    end_time = datetime.time(end_time.tm_hour, end_time.tm_min)

                lesson, lesson_created = Lesson.objects.update_or_create(
                    section=section,
                    order=index,

                    defaults={
                        "building": building,
                        "room": room,
                        "day": day,
                        "start_time": start_time,
                        "end_time": end_time,
                    }
                )

                if lesson_created:
                    logger.info(f"Lesson '{index}' for {section.code} has created.")
