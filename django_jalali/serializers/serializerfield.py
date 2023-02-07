import jdatetime
from django.core import exceptions
from rest_framework import serializers

from django_jalali.db.models import (
    jDateField as jDateFieldModel,
    jDateTimeField as jDateTimeFieldModel,
)


class JDateField(serializers.DateField):
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value
        return jDateFieldModel.parse_date(value)

    # This method is used by DRF to bringing value back to python form
    def to_internal_value(self, value):
        return self.to_python(value)


class JDateTimeField(serializers.DateTimeField):
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, str):
            for format in [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
            ]:
                try:
                    return jdatetime.datetime.strptime(value, format)
                except ValueError:
                    pass

        if isinstance(value, jdatetime.datetime):
            return value
        if isinstance(value, jdatetime.date):
            try:
                return jdatetime.datetime(value.year, value.month, value.day)
            except ValueError:
                raise exceptions.ValidationError(self.error_messages["invalid"])
        return jDateTimeFieldModel.parse_date(value)

    # This method is used by DRF to bringing value back to python form
    def to_internal_value(self, value):
        return self.to_python(value)

    # This method is used by DRF for representing object in string form
    # override this function with strftime if needed
    def to_representation(self, value):
        return str(value)
