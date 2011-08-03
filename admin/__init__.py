from django_jalali.db.models import jDateField
from django.contrib.admin import options
import django_jalali.admin.widgets 
options.FORMFIELD_FOR_DBFIELD_DEFAULTS[jDateField] = {'widget': widgets.AdminjDateWidget }
#maybe we can use same time
#models.TimeField:       {'widget': widgets.AdminTimeWidget},
#models.DateTimeField: {
#'form_class': forms.SplitDateTimeField,
#'widget': widgets.AdminSplitDateTime
#}

