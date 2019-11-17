from django_jalali.db.models import jDateField, jDateTimeField
from django.contrib.admin import options
from django_jalali.admin import widgets
from django import forms


options.FORMFIELD_FOR_DBFIELD_DEFAULTS[jDateField] = {'widget': widgets.AdminjDateWidget}
options.FORMFIELD_FOR_DBFIELD_DEFAULTS[jDateTimeField] = {
    'form_class': forms.SplitDateTimeField,
    'widget': widgets.AdminSplitjDateTime,
}
# maybe we can use same time
# models.TimeField:       {'widget': widgets.AdminTimeWidget},
# models.DateTimeField: {
# 'form_class': forms.SplitDateTimeField,
# 'widget': widgets.AdminSplitDateTime
# }
