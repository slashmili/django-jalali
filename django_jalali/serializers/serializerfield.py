import serializers
import re
import datetime
import jdatetime
from django.Exception import validationError

class JDateField(serializers.DateField):

    def parse_date(self, date_obj):
        ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')

        "Take a datetime object and convert it to jalali date"

        if isinstance(date_obj, datetime.datetime):
            return jdatetime.date.fromgregorian(date=date_obj.date())
        if isinstance(date_obj, datetime.date):
            return jdatetime.date.fromgregorian(date=date_obj)

        if not ansi_date_re.search(date_obj):
            raise ValidationError(self.error_messages['invalid'])
        # Now that we have the date string in YYYY-MM-DD format, check to make
        # sure it's a valid date.
        # We could use time.strptime here and catch errors, but datetime.date
        # produces much friendlier error messages.

        year, month, day = map(int, date_obj.split('-'))
        try:
            if year > 1500:
                return jdatetime.date.fromgregorian(
                    date=datetime.date(year, month, day))
            else:
                return jdatetime.date(year, month, day)
        except ValueError as e:
            msg = "invalid date %s" % str(e)
            raise ValidationError(msg)


    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, jdatetime.datetime):
            return value.date()
        if isinstance(value, jdatetime.date):
            return value
        return self.parse_date(value)


    def to_internal_value(self, value):
        return self.to_python(value)
