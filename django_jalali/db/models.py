import datetime
import re
import time
import warnings
from functools import partialmethod

import jdatetime
from django.conf import settings
from django.core import exceptions
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _

from django_jalali import forms

ansi_date_re = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}$")


class jQuerySet(models.QuerySet):
    """we need to rewrite this class to handle year filter"""

    def filter(self, *args, **kwargs):
        """if filter is year we divide to __gte and __lte"""
        new_kwargs = {}
        for k in kwargs:
            if "__year" in k:
                filed_name = k.split("__year")
                first_year = jdatetime.datetime(int(kwargs[k]), 1, 1)
                new_kwargs["%s__gte" % filed_name[0]] = jdatetime.datetime(
                    int(kwargs[k]), 1, 1
                )
                last_day = 29
                if first_year.isleap():
                    last_day = 30
                new_kwargs["%s__lte" % filed_name[0]] = jdatetime.datetime(
                    int(kwargs[k]), 12, last_day, 23, 59, 59
                )
            elif "__date" in k:
                jdate = kwargs[k]
                if isinstance(jdate, jdatetime.datetime):
                    gregorian_date = jdate.date().togregorian()
                elif isinstance(jdate, jdatetime.date):
                    gregorian_date = jdate.togregorian()
                elif isinstance(jdate, str):
                    year, month, day = map(int, jdate.split("-"))
                    gregorian_date = jdatetime.date(year, month, day).togregorian()
                else:
                    raise TypeError(
                        "`__date` filter Expected jdatetime.datetime, "
                        f"jdatetime.date or str, got `{jdate.__class__.__name__}`."
                    )
                new_kwargs[k] = gregorian_date
            else:
                new_kwargs[k] = kwargs[k]
        return super().filter(*args, **new_kwargs)


jManager = models.Manager.from_queryset(jQuerySet)


class jDateField(models.DateField):
    description = _("Date (without time)")
    empty_strings_allowed = False
    default_error_messages = {
        "invalid": _("Enter a valid date in YYYY-MM-DD format."),
        "invalid_date": _("Invalid date: %s"),
    }

    def __init__(
        self,
        verbose_name=None,
        name=None,
        auto_now=False,
        auto_now_add=False,
        default=models.NOT_PROVIDED,
        **kwargs,
    ):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        # HACKs : auto_now_add/auto_now should be
        # done as a default or a pre_save.
        if auto_now or auto_now_add:
            kwargs["editable"] = False
            kwargs["blank"] = True

        # Convert datetime.date default value to jdatetime.date
        if isinstance(default, datetime.date):
            default = jdatetime.date.fromgregorian(date=default)

        models.Field.__init__(self, verbose_name, name, default=default, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # Convert jdatetime.date default value to datetime.date
        if "default" in kwargs and isinstance(kwargs["default"], jdatetime.date):
            kwargs["default"] = kwargs["default"].togregorian()

        return name, path, args, kwargs

    def get_internal_type(self):
        return "DateField"

    @classmethod
    def parse_date(cls, date_obj):
        "Take a datetime object and convert it to jalali date"

        if isinstance(date_obj, datetime.datetime):
            return jdatetime.date.fromgregorian(date=date_obj.date())
        if isinstance(date_obj, datetime.date):
            return jdatetime.date.fromgregorian(date=date_obj)

        if not ansi_date_re.search(date_obj):
            raise exceptions.ValidationError(cls.default_error_messages["invalid"])
        # Now that we have the date string in YYYY-MM-DD format, check to make
        # sure it's a valid date.
        # We could use time.strptime here and catch errors, but datetime.date
        # produces much friendlier error messages.
        year, month, day = map(int, date_obj.split("-"))
        try:
            if year > 1500:
                return jdatetime.date.fromgregorian(
                    date=datetime.date(year, month, day)
                )
            else:
                return jdatetime.date(year, month, day)
        except ValueError as e:
            msg = cls.default_error_messages["invalid_date"] % _(str(e))
            raise exceptions.ValidationError(msg)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.parse_date(value)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value
        return self.parse_date(value)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = jdatetime.date.today()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        if not self.null:
            setattr(
                cls,
                "get_next_by_%s" % self.name,
                partialmethod(
                    cls._get_next_or_previous_by_FIELD, field=self, is_next=True
                ),
            )
            setattr(
                cls,
                "get_previous_by_%s" % self.name,
                partialmethod(
                    cls._get_next_or_previous_by_FIELD, field=self, is_next=False
                ),
            )

    def get_prep_lookup(self, lookup_type, value):
        """this class dosn't work in month and day search !"""
        # For "__month", "__day", and "__week_day" lookups, convert the value
        # to an int so the database backend always sees a consistent type.

        if lookup_type in ("exact", "gt", "gte", "lt", "lte"):
            prep = self.get_prep_value(value)
            if isinstance(prep, (datetime.datetime, datetime.date)):
                return prep
            return prep.togregorian()

        elif lookup_type in ("range", "in"):
            return [self.get_prep_value(v) for v in value]
        elif lookup_type == "year":
            # this else never happen !
            try:
                return int(value)
            except ValueError:
                raise ValueError("The __year lookup type requires an integer argument")

        if lookup_type in ("month", "day", "week_day"):
            raise ValueError("jDateField doesn't work with month, day and week_day !")

        return super().get_prep_lookup(lookup_type, value)

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

        return connection.ops.adapt_datefield_value(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            date_string = ""
        else:
            date_string = smart_str(value)
        return date_string

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.jDateField}
        kwargs.update(defaults)
        return super().formfield(**kwargs)


class jDateTimeField(models.DateTimeField):
    default_error_messages = {
        "invalid": _(
            "Enter a valid date/time in " "YYYY-MM-DD HH:MM[:ss[.uuuuuu]] format."
        ),
    }
    description = _("Date (with time)")

    def __init__(
        self,
        verbose_name=None,
        name=None,
        auto_now=False,
        auto_now_add=False,
        default=models.NOT_PROVIDED,
        **kwargs,
    ):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        # HACKs : auto_now_add/auto_now should be
        # done as a default or a pre_save.
        if auto_now or auto_now_add:
            kwargs["editable"] = False
            kwargs["blank"] = True

        # Convert datetime.datetime default value to jdatetime.datetime
        if isinstance(default, datetime.date):
            default = jdatetime.datetime.fromgregorian(datetime=default)

        models.Field.__init__(self, verbose_name, name, default=default, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # Convert jdatetime.datetime default value to datetime.datetime
        default = kwargs.get("default")
        if default and isinstance(default, (jdatetime.datetime)):
            kwargs["default"] = default.togregorian()

        return name, path, args, kwargs

    def get_internal_type(self):
        return "DateTimeField"

    @classmethod
    def parse_date(cls, datetime_obj):
        "Take a datetime object and convert it to jalali date"

        if isinstance(datetime_obj, datetime.datetime):
            try:
                if datetime_obj.year < 1700:
                    return jdatetime.datetime(
                        datetime_obj.year,
                        datetime_obj.month,
                        datetime_obj.day,
                        datetime_obj.hour,
                        datetime_obj.minute,
                        datetime_obj.second,
                        datetime_obj.microsecond,
                        datetime_obj.tzinfo,
                    )
                else:
                    return jdatetime.datetime.fromgregorian(datetime=datetime_obj)
            except ValueError:
                raise exceptions.ValidationError(cls.default_error_messages["invalid"])
        if isinstance(datetime_obj, datetime.date):
            try:
                if datetime_obj.year < 1700:
                    return jdatetime.datetime(
                        datetime_obj.year, datetime_obj.month, datetime_obj.day
                    )
                else:
                    return jdatetime.datetime.fromgregorian(date=datetime_obj)
            except ValueError:
                raise exceptions.ValidationError(cls.default_error_messages["invalid"])

        # Attempt to parse a datetime:
        datetime_obj = smart_str(datetime_obj)
        if not datetime_obj:
            return None
        # split usecs, because they are not recognized by strptime.
        if "." in datetime_obj:
            try:
                datetime_obj, usecs = datetime_obj.split(".")
                if "+" in usecs:
                    usecs, tz = usecs.split("+")
                usecs = int(usecs)
            except ValueError:
                raise exceptions.ValidationError(cls.default_error_messages["invalid"])
        else:
            usecs = 0
        kwargs = {"microsecond": usecs}

        formats = [
            ("%Y-%m-%d %H:%M:%S", 6),
            ("%Y-%m-%d %H:%M", 5),
            ("%Y-%m-%d", 3),
        ]
        for format, c in formats:
            try:  # Seconds are optional, so try converting seconds first.
                t = time.strptime(datetime_obj, format)
                if t.tm_year > 1700:
                    return datetime.datetime(
                        *time.strptime(datetime_obj, format)[:c], **kwargs
                    )
                else:
                    return jdatetime.datetime(
                        *time.strptime(datetime_obj, format)[:c], **kwargs
                    )
            except ValueError:
                try:
                    return jdatetime.datetime.strptime(
                        datetime_obj, "%Y-%m-%d %H:%M:%S"
                    ).replace(**kwargs)
                except ValueError:
                    pass
        raise exceptions.ValidationError(cls.default_error_messages["invalid"])

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        if value is not None and settings.USE_TZ:
            # Remove and set timezone information
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_naive(value, default_timezone)
            value = timezone.make_aware(value, default_timezone)

        return self.parse_date(value)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, jdatetime.datetime):
            return value
        if isinstance(value, jdatetime.date):
            try:
                return jdatetime.datetime(value.year, value.month, value.day)
            except ValueError:
                raise exceptions.ValidationError(self.error_messages["invalid"])
        return self.parse_date(value)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = jdatetime.datetime.now()
            if value is not None and settings.USE_TZ and timezone.is_naive(value):
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def get_prep_value(self, value):
        value = self.to_python(value)
        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            try:
                name = f"{self.model.__name__}.{self.name}"
            except AttributeError:
                name = "(unbound)"
            warnings.warn(
                "DateTimeField %s received a naive datetime (%s)"
                " while time zone support is active." % (name, value),
                RuntimeWarning,
            )
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_timezone)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)

        if isinstance(value, jdatetime.datetime):
            value = value.togregorian()

        return connection.ops.adapt_datefield_value(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            date_string = ""
        else:
            date_string = smart_str(value)
        return date_string

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        if not self.null:
            setattr(
                cls,
                "get_next_by_%s" % self.name,
                partialmethod(
                    cls._get_next_or_previous_by_FIELD, field=self, is_next=True
                ),
            )
            setattr(
                cls,
                "get_previous_by_%s" % self.name,
                partialmethod(
                    cls._get_next_or_previous_by_FIELD, field=self, is_next=False
                ),
            )

    def get_prep_lookup(self, lookup_type, value):
        """this class dosn't work in month and day search !"""
        # For "__month", "__day", and "__week_day" lookups, convert the value
        # to an int so the database backend always sees a consistent type.

        if lookup_type in ("exact", "gt", "gte", "lt", "lte"):
            prep = self.get_prep_value(value)
            if isinstance(prep, (datetime.datetime, datetime.date)):
                return prep
            return prep.togregorian()

        elif lookup_type in ("range", "in"):
            return [self.get_prep_value(v) for v in value]
        elif lookup_type == "year":
            # this else never happen !
            try:
                return int(value)
            except ValueError:
                raise ValueError("The __year lookup type requires an integer argument")

        if lookup_type in ("month", "day", "week_day"):
            raise ValueError(
                "jDateTimeField doesn't work with month, day and week_day !"
            )

        return super().get_prep_lookup(lookup_type, value)

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.jDateTimeField}
        kwargs.update(defaults)
        return super().formfield(**kwargs)
