import re
from typing import Union

import jdatetime
from django import forms
from django.core import exceptions, validators
from django.forms.utils import from_current_timezone, to_current_timezone
from django.utils.translation import gettext as _

from django_jalali.forms.widgets import jDateInput, jDateTimeInput


class jDateField(forms.Field):
    widget = jDateInput
    default_error_messages = {
        "invalid": _("Enter a valid date."),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_formats = input_formats

    def to_python(self, value) -> Union[jdatetime.date, None]:
        """
        Validates that the input can be converted to a date. Returns a Python
        jdatetime.date object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value

        if self.input_formats:
            for input_format in self.input_formats:
                try:
                    return jdatetime.datetime.strptime(value, input_format).date()
                except ValueError:
                    pass

        groups = re.search(
            r"(?P<year>[\d]{1,4})-(?P<month>[\d]{1,2})-(?P<day>[\d]{1,2})",
            value,
        )
        try:
            return jdatetime.date(
                year=int(groups.group(1)),
                month=int(groups.group(2)),
                day=int(groups.group(3)),
            )

        except (ValueError, AttributeError):
            pass

        raise exceptions.ValidationError(self.error_messages["invalid"])


class jDateTimeField(forms.Field):
    widget = jDateTimeInput
    default_error_messages = {
        "invalid": _("Enter a valid date/time."),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_formats = input_formats

    def prepare_value(self, value):
        if isinstance(value, jdatetime.datetime):
            value = to_current_timezone(value)
        return value

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, jdatetime.datetime):
            return from_current_timezone(value.togregorian())
        if isinstance(value, jdatetime.date):
            result = jdatetime.datetime(value.year, value.month, value.day)
            return from_current_timezone(result.togregorian())
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise exceptions.ValidationError(self.error_messages["invalid"])
            if (
                value[0] in validators.EMPTY_VALUES
                and value[1] in validators.EMPTY_VALUES
            ):
                return None
            value = "%s %s" % tuple(value)

        if self.input_formats:
            for input_format in self.input_formats:
                try:
                    return jdatetime.datetime.strptime(value, input_format).date()
                except ValueError:
                    pass

        groups = re.search(
            r"(?P<year>[\d]{1,4})-(?P<month>[\d]{1,2})-(?P<day>[\d]{1,2}) "
            r"(?P<hour>[\d]{1,2}):(?P<minute>[\d]{1,2})"
            r"(:(?P<second>[\d]{1,2}))?(.(?P<microsecond>[\d]{1,5}))?",
            value,
        )
        try:
            microsecond = int(groups.group("microsecond") or 0)
            second = int(groups.group("second") or 0)
            result = jdatetime.datetime(
                year=int(groups.group("year")),
                month=int(groups.group("month")),
                day=int(groups.group("day")),
                hour=int(groups.group("hour")),
                minute=int(groups.group("minute")),
                second=second,
                microsecond=microsecond,
            )
            return from_current_timezone(result.togregorian())

        except (ValueError, AttributeError):
            pass

        raise exceptions.ValidationError(self.error_messages["invalid"])
