from django_jalali import forms as jforms
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.admin.templatetags.admin_static import static
from django.utils.safestring import mark_safe

class AdminjDateWidget(jforms.jDateInput):
    @property
    def media(self):
        js = ["admin/jalalijscalendar/jalali.js", "admin/jalalijscalendar/calendar.js",
              "admin/jalalijscalendar/calendar-setup.js",
              "admin/jalalijscalendar/calendar-fa.js", "admin/jDateTimeShortcuts.js"]
        # css = ["calendar-green.css"]
        return forms.Media(js=[static("admin/js/%s" % path) for path in js],
                           css={'all': ('admin/css/calendar-green.css',)})

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vjDateField', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminjDateWidget, self).__init__(attrs=final_attrs, format=format)



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
        return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
            (_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))
