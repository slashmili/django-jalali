import datetime
import time

import jdatetime
from django.forms import widgets
from django.utils import formats
from django.utils.encoding import smart_str


class jDateInput(widgets.Input):
    input_type = "text"
    format = None

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        if format:
            self.format = format

    def _format_value(self, value):
        if value is None:
            return ""
        elif hasattr(value, "strftime"):
            f = smart_str(self.format or formats.get_format("DATE_INPUT_FORMATS")[0])
            return value.strftime(f)

        return value

    def render(self, name, value, attrs=None, renderer=None):
        value = self._format_value(value)
        return super().render(name, value, attrs)

    def _has_changed(self, initial, data):
        # If our field has show_hidden_initial=True, initial will be a string
        # formatted by HiddenInput using formats.localize_input, which is not
        # necessarily the format used for this widget. Attempt to convert it.
        try:
            input_format = formats.get_format("DATE_INPUT_FORMATS")[0]
            initial = jdatetime.date(*time.strptime(initial, input_format)[:3])
        except (TypeError, ValueError):
            pass
        return super()._has_changed(self._format_value(initial), data)


class jDateTimeInput(widgets.Input):
    input_type = "text"
    format = "%Y-%m-%d %H:%M:%S"  # '2006-10-25 14:30:59'

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        if format:
            self.format = formats
            self.manual_format = True
        else:
            self.format = formats.get_format("DATETIME_INPUT_FORMATS")[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        elif hasattr(value, "strftime"):
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        # If our field has show_hidden_initial=True, initial will be a string
        # formatted by HiddenInput using formats.localize_input, which is not
        # necessarily the format used for this widget. Attempt to convert it.
        try:
            input_format = formats.get_format("DATETIME_INPUT_FORMATS")[0]
            initial = datetime.datetime(*time.strptime(initial, input_format)[:6])
        except (TypeError, ValueError):
            pass
        return super()._has_changed(self._format_value(initial), data)
