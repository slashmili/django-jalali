import jdatetime
from django.test import TestCase

from django_jalali.forms import jDateField, jDateTimeField


class JDateFieldTest(TestCase):
    def test_field(self):
        tests = (
            "1400-11-27",
            jdatetime.date(1400, 11, 27),
            jdatetime.datetime(1400, 11, 27),
        )
        for value in tests:
            with self.subTest(value=value):
                f = jDateField()
                self.assertEqual(f.clean(value), jdatetime.date(1400, 11, 27))


class JDateTimeFieldTest(TestCase):
    def test_field(self):
        tests = (
            "1400-11-27 12:13:20",
            jdatetime.datetime(1400, 11, 27, 12, 13, 20),
        )
        for value in tests:
            with self.subTest(value=value):
                f = jDateTimeField()
                self.assertEqual(
                    f.clean(value), jdatetime.datetime(1400, 11, 27, 12, 13, 20)
                )
