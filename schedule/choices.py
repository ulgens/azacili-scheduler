from django.db.models import IntegerChoices
from django.utils.translation import ugettext as _


__all__ = (
    "Days",
)


class Days(IntegerChoices):
    MONDAY = 1, _("Monday")
    TUESDAY = 2, _("Tuesday")
    WEDNESDAY = 3, _("Wednesday")
    THURSDAY = 4, _("Thursday")
    FRIDAY = 5, _("Friday")
    SATURDAY = 6, _("Saturday")
    SUNDAY = 7, _("Sunday")
