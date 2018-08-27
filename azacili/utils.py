import logging

import requests
from bs4 import BeautifulSoup

from azacili import settings
from schedule.models import Program, Section


logger = logging.getLogger(__name__)

BASE_CATALOG_URL = settings.BASE_CATALOG_URL


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

