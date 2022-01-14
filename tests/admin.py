from django.contrib import admin

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin  # noqa
from django_jalali.admin.filters import JDateFieldListFilter
from tests.models import Bar, BarTime


class BarAdmin(admin.ModelAdmin):
    list_filter = (
        ('date', JDateFieldListFilter),
    )


admin.site.register(Bar, BarAdmin)


class BarTimeAdmin(admin.ModelAdmin):
    list_filter = (
        ('datetime', JDateFieldListFilter),
    )


admin.site.register(BarTime, BarTimeAdmin)
