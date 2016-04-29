from foo.models import Bar, BarTime
from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

#you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

class BarAdmin(admin.ModelAdmin):
    list_filter = (
        ('date', JDateFieldListFilter),
    )
    pass

admin.site.register(Bar, BarAdmin)

class BarTimeAdmin(admin.ModelAdmin):
    list_filter = (
        ('datetime', JDateFieldListFilter),
    )

admin.site.register(BarTime, BarTimeAdmin)
