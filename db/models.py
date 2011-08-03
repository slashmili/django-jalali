import jdatetime
import datetime
import re
from django.db import models
from django.utils.translation import ugettext as _
from django_jalali import forms
from django.utils.functional import curry
from django.core import exceptions

ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
class jManager(models.Manager):
    """we need to rewrite this class to handle year filter"""
    def filter(self, *args, **kwargs):
        """if filter is year we divide to __gte and __lte"""
        new_kwargs = {}
        for k in kwargs:
            if '__year' in k :
                first_year = jdatetime.datetime(int(kwargs[k]),1 ,1)
                new_kwargs['da__gte'] = jdatetime.datetime(int(kwargs[k]),1 ,1)
                last_day = 29
                if first_year.isleap() :
                    last_day = 30
                new_kwargs['da__lte'] = jdatetime.datetime(int(kwargs[k]),12, last_day, 23, 59, 59)
            else :
                new_kwargs[k] = kwargs[k]
        return models.Manager.filter(self, *args, **new_kwargs )



class jDateField(models.Field):
    #objects = JDManager()
    description = _("Date (without time)")
    __metaclass__ = models.SubfieldBase
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _('Enter a valid date in YYYY-MM-DD format.'),
        'invalid_date': _('Invalid date: %s'),
    }

    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs):

        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        #HACKs : auto_now_add/auto_now should be done as a default or a pre_save.
        if auto_now or auto_now_add:
            kwargs['editable'] = False
            kwargs['blank'] = True
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return "DateField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return jdatetime.date.fromgregorian(date=value.date())
        if isinstance(value, datetime.date):
            return jdatetime.date.fromgregorian(date=value)

        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value

        if not ansi_date_re.search(value):
            raise exceptions.ValidationError(self.error_messages['invalid'])
        # Now that we have the date string in YYYY-MM-DD format, check to make
        # sure it's a valid date.
        # We could use time.strptime here and catch errors, but datetime.date
        # produces much friendlier error messages.
        year, month, day = map(int, value.split('-'))
        try:
            if year > 1500 :
                return jdatetime.date.fromgregorian(date=datetime.date(year, month, day))
            else:
                return jdatetime.date(year,month,day)
        except ValueError, e:
            msg = self.error_messages['invalid_date'] % _(str(e))
            raise exceptions.ValidationError(msg)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = jdatetime.date.today()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(jDateField, self).pre_save(model_instance, add)

    def contribute_to_class(self, cls, name):
        super(jDateField,self).contribute_to_class(cls, name)
        if not self.null:
            setattr(cls, 'get_next_by_%s' % self.name,
                curry(cls._get_next_or_previous_by_FIELD, field=self, is_next=True))
            setattr(cls, 'get_previous_by_%s' % self.name,
                curry(cls._get_next_or_previous_by_FIELD, field=self, is_next=False))

    def get_prep_lookup(self, lookup_type, value):
        # For "__month", "__day", and "__week_day" lookups, convert the value
        # to an int so the database backend always sees a consistent type.
        if lookup_type == 'year':
            date_start = jdatetime.date(int(value), 1, 1)
            date_end   = jdatetime.date(int(value), 12, 29)
            return date_start.togregorian().year
        #return super(jDateField, self).get_prep_lookup(lookup_type, value)
        if lookup_type in (
                'regex', 'iregex', 'month', 'day', 'week_day', 'search',
                'contains', 'icontains', 'iexact', 'startswith', 'istartswith',
                'endswith', 'iendswith', 'isnull'
            ):
            return value

        elif lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
            prep  = self.get_prep_value(value)
            return prep.togregorian()

        elif lookup_type in ('range', 'in'):
            return [self.get_prep_value(v) for v in value]
        elif lookup_type == 'year':
            try:
                return int(value)
            except ValueError:
                raise ValueError("The __year lookup type requires an integer argument")

        if lookup_type in ('month', 'day', 'week_day'):
            return int(value)

        return super(jDateField, self).get_prep_lookup(lookup_type, value)

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)

        if isinstance(value, jdatetime.datetime):
            value = value.togregorian().date()
        if isinstance(value, jdatetime.date):
            value = value.togregorian()

        return connection.ops.value_to_db_date(value)

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = "te" #datetime_safe.new_date(val).strftime("%Y-%m-%d")
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.jDateField}
        defaults.update(kwargs)
        return super(jDateField, self).formfield(**defaults)
