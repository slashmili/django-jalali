from django_jalali import forms as jforms
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe

import settings

class AdminjDateWidget(jforms.jDateInput):
    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "js/jcalendar.js",
            settings.ADMIN_MEDIA_PREFIX + "js/admin/jDateTimeShortcuts.js")
    def __init__(self, attrs={}, format=None):
        super(AdminjDateWidget, self).__init__(attrs={'class': 'vjDateField', 'size': '10'}, format=format)



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
