import logging

import requests
from bs4 import BeautifulSoup

from azacili import settings
from schedule.models import Program, Section, Course, Building, Instructor, Lesson

logger = logging.getLogger(__name__)

BASE_CATALOG_URL = settings.BASE_CATALOG_URL
BUILDINGS_URL = settings.BUILDINGS_URL




def update_programs():
    r = requests.get(BASE_CATALOG_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get raw data
    program_options = soup.find("select").find_all("option")
    # Extract values
    program_options = map(lambda x: x.attrs["value"].strip(), program_options)
    # Remove empty items
    program_options = list(filter(lambda x: bool(x), program_options))

    for option in program_options:
        _, created = Program.objects.get_or_create(code=option)

        if created:
            logger.info(f"Program '{option}' has created.")

    # Check if any program is removed from SIS
    codes = Program.objects.all().values_list("code", flat=True)
    removed_programs = set(codes) - set(program_options)

    if removed_programs:
        logger.warning(f"Following programs are removed from SIS: {','.join(removed_programs)}")


def update_buildings():
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


