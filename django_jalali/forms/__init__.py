from django_jalali.forms.widgets import jDateInput, jDateTimeInput
from django import forms
import time
import datetime
import jdatetime
from django.core import validators, exceptions
from django.utils import datetime_safe, formats
from django.utils.translation import ugettext as _
from .widgets import jDateInput, jDateTimeInput

class jDateField(forms.Field):
    widget = jDateInput
    default_error_messages = {
        'invalid': _(u'Enter a valid date.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(jDateField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats

    def to_python(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value
        for format in self.input_formats or formats.get_format('DATE_INPUT_FORMATS'):
            try:
                return jdatetime.date(*time.strptime(value, format)[:3])
            except ValueError:
                continue
        raise exceptions.ValidationError(self.error_messages['invalid'])


class jDateTimeField(forms.Field):
    widget = jDateTimeInput
    default_error_messages = {
        'invalid': _(u'Enter a valid date/time.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(jDateTimeField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, jdatetime.datetime):
            return value
        if isinstance(value, jdatetime.date):
            return jdatetime.datetime(value.year, value.month, value.day)
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'])
            if value[0] in validators.EMPTY_VALUES and value[1] in validators.EMPTY_VALUES:
                return None
            value = '%s %s' % tuple(value)
        for format in self.input_formats or formats.get_format('DATETIME_INPUT_FORMATS'):
            try:
                return jdatetime.datetime(*time.strptime(value, format)[:6])
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])

