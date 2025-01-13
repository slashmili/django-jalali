from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from django_jalali import forms as jforms
from django_jalali.settings import jalali_settings


class AdminjDateWidget(jforms.jDateInput):

    class Media:
        js = jalali_settings.ADMIN_JS_STATIC_FILES
        css = jalali_settings.ADMIN_CSS_STATIC_FILES

    def __init__(self, attrs=None, format=None):
        final_attrs = {"class": "vjDateField", "size": "10"}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format)


class AdminSplitjDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [AdminjDateWidget, AdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(
            '<p class="datetime">%s %s<br />%s %s</p>'
            % (
                _("Date:"),
                rendered_widgets[0],
                _("Time:"),
                rendered_widgets[1],
            )
        )
