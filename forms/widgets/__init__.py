from django.forms import widgets
from django.utils.encoding import smart_str
from django.utils import formats
import time
import datetime
import jdatetime

class DateInput(widgets.Input):
    input_type = 'text'
    format = None

    def __init__(self, attrs=None, format=None):
        super(DateInput, self).__init__(attrs)
        if format:
            self.format = format

    def _format_value(self, value):
        if value is None:
            return ''
        elif hasattr(value, 'strftime'):
            f = smart_str(self.format or formats.get_format('DATE_INPUT_FORMATS')[0])
            return value.strftime(f)

        return value

    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        return super(DateInput, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        # If our field has show_hidden_initial=True, initial will be a string
        # formatted by HiddenInput using formats.localize_input, which is not
        # necessarily the format used for this widget. Attempt to convert it.
        try:
            input_format = formats.get_format('DATE_INPUT_FORMATS')[0]
            initial = jdatetime.date(*time.strptime(initial, input_format)[:3])
        except (TypeError, ValueError):
            pass
        return super(DateInput, self)._has_changed(self._format_value(initial), data)

