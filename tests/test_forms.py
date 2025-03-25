import jdatetime
from django.forms.utils import from_current_timezone
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

    def test_field_with_one_input_format(self):
        tests = (
            "1400/11/27",
            jdatetime.date(1400, 11, 27),
            jdatetime.datetime(1400, 11, 27),
        )
        for value in tests:
            with self.subTest(value=value):
                f = jDateField(
                    input_formats=[
                        "%Y/%m/%d",
                    ]
                )
                self.assertEqual(f.clean(value), jdatetime.date(1400, 11, 27))

    def test_field_with_multiple_input_formats(self):
        tests = (
            "1400/11/27",
            "1400, 11, 27",
            jdatetime.date(1400, 11, 27),
            jdatetime.datetime(1400, 11, 27),
        )
        for value in tests:
            with self.subTest(value=value):
                f = jDateField(input_formats=["%Y, %m, %d", "%Y/%m/%d"])
                self.assertEqual(f.clean(value), jdatetime.date(1400, 11, 27))


class JDateTimeFieldTest(TestCase):
    def test_field(self):
        tests = (
            "1400-11-27 12:13:20",
            jdatetime.datetime(1400, 11, 27, 12, 13, 20),
        )
        expected = from_current_timezone(
            jdatetime.datetime(1400, 11, 27, 12, 13, 20).togregorian()
        )

        for value in tests:
            with self.subTest(value=value):
                f = jDateTimeField()
                self.assertEqual(f.clean(value), expected)

    def test_field_with_one_input_formats(self):
        tests = [
            "1400/11/27 12:13",
            jdatetime.datetime(1400, 11, 27, 12, 13, 20),
        ]
        expected_outputs = [
            jdatetime.datetime(1400, 11, 27, 12, 13, 0).togregorian(),
            jdatetime.datetime(1400, 11, 27, 12, 13, 20).togregorian(),
        ]
        for value in tests:
            with self.subTest(value=value):
                f = jDateTimeField(
                    input_formats=[
                        "%Y/%m/%d %H:%M",
                    ]
                )
                self.assertEqual(
                    f.clean(value), from_current_timezone(expected_outputs.pop(0))
                )

    def test_field_with_multiple_input_formats(self):
        tests = (
            "1400/11/27 12-13",
            "1400, 11, 27 12:13",
            jdatetime.datetime(1400, 11, 27),
        )
        for value in tests:
            with self.subTest(value=value):
                f = jDateTimeField(input_formats=["%Y, %m, %d %H:%M", "%Y/%m/%d %H-%M"])
                self.assertEqual(f.clean(value), jdatetime.date(1400, 11, 27))
