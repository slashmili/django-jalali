from django_jalali import forms
from django.utils.translation import ugettext as _

import settings

class AdminjDateWidget(forms.DateInput):
    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "js/jcalendar.js",
            settings.ADMIN_MEDIA_PREFIX + "js/admin/jDateTimeShortcuts.js")
    def __init__(self, attrs={}, format=None):
        super(AdminjDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format)


#class AdminTimeWidget(forms.TimeInput):
#    class Media:
#        js = (settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
#              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")
#
#    def __init__(self, attrs={}, format=None):
#        super(AdminTimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '8'}, format=format)

#class AdminSplitDateTime(forms.SplitDateTimeWidget):
#    """
#    A SplitDateTime Widget that has some admin-specific styling.
#    """
#    def __init__(self, attrs=None):
#        widgets = [AdminDateWidget, AdminTimeWidget]
#        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
#        # we want to define widgets.
#        forms.MultiWidget.__init__(self, widgets, attrs)
#
#    def format_output(self, rendered_widgets):
#        return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
#            (_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))
