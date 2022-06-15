from datetime import date, datetime

import jdatetime
from django.template import Library

register = Library()


@register.filter(expects_localtime=True, is_safe=False)
def jformat(value, arg=None):
    """Formats a date or time according to the given format."""
    if value in (None, ""):
        return ""
    if arg is None:
        arg = "%c"
    try:
        if isinstance(value, datetime):
            value = jdatetime.datetime.fromgregorian(datetime=value)
        elif isinstance(value, date):
            value = jdatetime.date.fromgregorian(date=value)
        return value.strftime(arg)
    except AttributeError:
        return ""
