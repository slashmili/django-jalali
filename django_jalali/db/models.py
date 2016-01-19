import jdatetime
import datetime
import time
import re
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text, force_text, smart_str
from django_jalali import forms
from django import forms as mainforms
from django.utils.functional import curry
from django.core import exceptions
import django
from distutils.version import StrictVersion

ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
class jManager(models.Manager):
    """we need to rewrite this class to handle year filter"""
    def filter(self, *args, **kwargs):
        """if filter is year we divide to __gte and __lte"""
        new_kwargs = {}
        for k in kwargs:
            if '__year' in k :
                filed_name = k.split('__year')
                first_year = jdatetime.datetime(int(kwargs[k]),1 ,1)
                new_kwargs['%s__gte'%filed_name[0]] = jdatetime.datetime(int(kwargs[k]),1 ,1)
                last_day = 29
                if first_year.isleap() :
                    last_day = 30
                new_kwargs['%s__lte'%filed_name[0]] = jdatetime.datetime(int(kwargs[k]),12, last_day, 23, 59, 59)
            else :
                new_kwargs[k] = kwargs[k]
        return models.Manager.filter(self, *args, **new_kwargs )



class jDateField(models.Field):
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
        except ValueError as e:
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
        """this class dosn't work in month and day searh !"""
        # For "__month", "__day", and "__week_day" lookups, convert the value
        # to an int so the database backend always sees a consistent type.

        if lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
            prep  = self.get_prep_value(value)
            if type(prep) == datetime.datetime or type(prep) == datetime.date:
                return prep
            return prep.togregorian()

        elif lookup_type in ('range', 'in'):
            return [self.get_prep_value(v) for v in value]
        elif lookup_type == 'year':
            #this else never happen !
            try:
                return int(value)
            except ValueError:
                raise ValueError("The __year lookup type requires an integer argument")

        if lookup_type in ('month', 'day', 'week_day'):
            raise ValueError("jDateField dosn't work with month, day and week_day !")

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

        if StrictVersion(django.get_version()) >= StrictVersion('1.9'):
            return connection.ops.adapt_datefield_value(value)
        else :
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


class jDateTimeField(jDateField):
    default_error_messages = {
        'invalid': _(u'Enter a valid date/time in YYYY-MM-DD HH:MM[:ss[.uuuuuu]] format.'),
    }
    description = _("Date (with time)")

    def get_internal_type(self):
        return "DateTimeField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            try :
                if value.year < 1700 :
                    return jdatetime.datetime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond, value.tzinfo)
                else :
                    return jdatetime.datetime.fromgregorian(datetime=value)
            except ValueError :
                raise exceptions.ValidationError(self.error_messages['invalid'])
        if isinstance(value, datetime.date):
            try :
                if value.year < 1700 :
                    return jdatetime.datetime(value.year, value.month, value.day)
                else :
                    return jdatetime.datetime.fromgregorian(date=value)
            except ValueError :
                raise exceptions.ValidationError(self.error_messages['invalid'])
        if isinstance(value, jdatetime.datetime):
            return value
        if isinstance(value, jdatetime.date):
            try :
                d = jdatetime.datetime(value.year, value.month, value.day)
            except ValueError :
                raise exceptions.ValidationError(self.error_messages['invalid'])
            return d


        # Attempt to parse a datetime:
        value = smart_str(value)
        # split usecs, because they are not recognized by strptime.
        if '.' in value:
            try:
                value, usecs = value.split('.')
                usecs = int(usecs)
            except ValueError:
                raise exceptions.ValidationError(self.error_messages['invalid'])
        else:
            usecs = 0
        kwargs = {'microsecond': usecs}
        try: # Seconds are optional, so try converting seconds first.
            t = time.strptime(value, '%Y-%m-%d %H:%M:%S')
            if t.tm_year > 1700 :
                return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6],
                                     **kwargs)
            else :
                return jdatetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6],
                                    **kwargs)

        except ValueError:
            try: # Try without seconds.
                t = time.strptime(value, '%Y-%m-%d %H:%M')
                if t.tm_year > 1700:
                    return  datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M')[:5],
                                     **kwargs)
                else :
                    return  jdatetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M')[:5],
                                     **kwargs)

            except ValueError: # Try without hour/minutes/seconds.
                try:
                    t = time.strptime(value, '%Y-%m-%d')[:3]
                    if t[0] > 1700 :
                        return datetime.datetime(*time.strptime(value, '%Y-%m-%d')[:3],
                                             **kwargs)
                    else :
                        return jdatetime.datetime(*time.strptime(value, '%Y-%m-%d')[:3],
                                             **kwargs)
                except ValueError:
                    raise exceptions.ValidationError(self.error_messages['invalid'])

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = jdatetime.datetime.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(jDateTimeField, self).pre_save(model_instance, add)

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)

        if isinstance(value, jdatetime.datetime):
            value = value.togregorian()

        if StrictVersion(django.get_version()) >= StrictVersion('1.9'):
            return connection.ops.adapt_datefield_value(value)
        else :
            return connection.ops.value_to_db_datetime(value)



    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            d = datetime_safe.new_datetime(val)
            data = d.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.jDateTimeField}
        defaults.update(kwargs)
        return super(jDateTimeField, self).formfield(**defaults)
