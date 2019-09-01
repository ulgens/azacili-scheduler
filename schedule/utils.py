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

    ## Clean data
    # Get raw data
    programs = soup.find("select").find_all("option")
    # Extract values
    programs = map(lambda x: x.attrs["value"].strip(), programs)
    # Remove empty items
    programs = list(filter(lambda x: bool(x), programs))
    # Sort alphabetically
    programs = sorted(programs)

    ## / Clean data

    sis_program_count = len(programs)
    db_program_count = Program.objects.count()

    logger.info("Programs:")
    logger.info(f"- {sis_program_count} programs came from SIS.")
    logger.info(f"- {db_program_count} programs found in database.")

    ## Import data
    for p in programs:
        program, created = Program.objects.get_or_create(code=p)

        if not created:
            logger.info(f"{program.code}.")
        else:
            logger.info(f"{program.code} - NEW")

    # Check if any program is removed from SIS
    codes = Program.objects.all().values_list("code", flat=True)
    removed_programs = set(codes) - set(programs)

    if removed_programs:
        logger.warning(f"Following programs are removed from SIS and should be handled manually: "
                       f"{','.join(removed_programs)}")
    ## / Import data


def update_buildings():
    r = requests.get(BUILDINGS_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    ## Clean data
    raw_table = soup.find_all("table")[-1]
    raw_buildings = raw_table.find_all("tr")

    buildings = {}
    for raw_b in raw_buildings:
        rows = raw_b.find_all("td")
        data = [row.get_text() for row in rows]

        code = data[0].strip()
        name = " ".join(data[1].split())

        buildings[code] = name
        # Sort alphabetically

    buildings = dict(sorted(buildings.items()))
    ## / Clean data

    sis_building_count = len(buildings)
    db_building_count = Building.objects.count()

    logger.info("Buildings:")
    logger.info(f"- {sis_building_count} buildings came from SIS.")
    logger.info(f"- {db_building_count} buildings found in database.")

    ## Import data
    for building_code, building_name in buildings.items():
        building, created = Building.objects.update_or_create(
            code=building_code,
            defaults={"name": building_name},
        )

        if not created:
            logger.info(f"{building_code}: {building_name}")
        else:
            logger.info(f"{building_code}: {building_name} - NEW")

    codes = Building.objects.all().values_list("code", flat=True)
    removed_buildings = set(codes) - set(buildings.keys())

    if removed_buildings:
        logger.warning(f"Following buildings are removed from SIS and should be handled manually: "
                       f"{','.join(removed_buildings)}")
    ## / Import data


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

        raw_table = soup.find("table", class_="dersprg")
        # First two tr are title
        raw_courses = raw_table.find_all("tr")[2:]

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

            if not course_created:
                logger.info(f"Course: {course_code} - {course_name}")
            else:
                logger.info(f"Course: {course_code} - {course_name} - NEW")

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
            section, section_created = Section.objects.update_or_create(
                code=section_code,
                course=course,
                defaults={"lecturer": instructor},
            )

            if not section_created:
                logger.info(f"Section: {section_code}")
            if section_created:
                logger.info(f"Section: {section_code} - NEW")

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
