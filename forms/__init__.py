from django_jalali.forms.widgets import jDateInput
from django import forms
import time
import datetime
import jdatetime 
from django.core import validators
from django.utils import datetime_safe, formats
from django.utils.translation import ugettext as _
from widgets import *
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
        raise ValidationError(self.error_messages['invalid'])


