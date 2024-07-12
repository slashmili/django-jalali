import datetime

import jdatetime
from django.core.exceptions import ValidationError
from django.db.migrations.writer import MigrationWriter
from django.test import TestCase, override_settings, skipUnlessDBFeature
from django.test.utils import requires_tz_support
from django.utils import timezone

from django_jalali.db import models as jmodels
from tests.models import (
    Bar,
    BarTime,
    DateTimeWithDefault,
    DateWithDefault,
    ModelWithAutoNowAdd,
)


class BarTestCase(TestCase):
    def setUp(self):
        self.today_string = "1390-5-12"
        self.today = jdatetime.date(1390, 5, 12)
        self.mybar = Bar(name="foo", date=self.today)
        self.mybar.save()

    def test_save_date(self):
        self.assertEqual(self.mybar.date, self.today)

    def test_default_value(self):
        obj = DateWithDefault.objects.create()
        self.assertEqual(obj.date1, jdatetime.datetime(1390, 6, 31))
        self.assertEqual(obj.date2, jdatetime.datetime(1390, 6, 31))

    def test_save_specific_date(self):
        Bar.objects.create(name="Test", date="1398-04-31")
        k = Bar.objects.filter(date="1398-04-31")
        self.assertEqual(k[0].date.day, 31)

    def test_filter_by_exact_date(self):
        bars = Bar.objects.filter(date=self.today_string)
        self.assertEqual(len(bars), 1)

    def test_filter_by_exact_date_no_match(self):
        bars = Bar.objects.filter(date="1390-5-11")
        self.assertEqual(len(bars), 0)

    def test_filter_by_gte_date(self):
        bars = Bar.objects.filter(date__gte=self.today_string)
        self.assertEqual(len(bars), 1)

    def test_serialize_default_jdatetime_value(self):
        jd1 = jdatetime.date(1390, 6, 31)
        field = jmodels.jDateField(default=jd1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                "django_jalali.db.models.jDateField(default=datetime.date(2011, 9, 22))",
                {"import django_jalali.db.models", "import datetime"},
            ),
        )

    def test_serialize_default_datetime_value(self):
        dt1 = datetime.date(2013, 6, 2)
        field = jmodels.jDateField(default=dt1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                "django_jalali.db.models.jDateField(default=datetime.date(2013, 6, 2))",
                {"import django_jalali.db.models", "import datetime"},
            ),
        )

    def test_filtering(self):
        today = jdatetime.date.today()
        Bar.objects.create(date=today, name="test name")

        # search by year
        jdm_date = Bar.objects.filter(date__year=today.year)
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date.year, today.year)

        # search by string
        jdm_date = Bar.objects.filter(date=f"{today.year}-{today.month}-{today.day}")
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        # save by geregorian date and retrive by jalali date
        g_2009 = datetime.date(2009, 9, 9)
        jd_model = Bar(date=g_2009)
        jd_model.save()

        jdm_date = Bar.objects.filter(date=g_2009)
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, jdatetime.date.fromgregorian(date=g_2009))

        jdm_date = Bar.objects.filter(date=f"{today.year}-{today.month}-{today.day}")
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        jdm_date = Bar.objects.filter(
            date__in=[f"{today.year}-{today.month}-{today.day}"]
        )
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        # wrong day value
        with self.assertRaises(ValidationError):
            Bar.objects.filter(date=f"{today.year}-{today.month}-{35}")

        # invalid format
        with self.assertRaises(ValidationError):
            Bar.objects.filter(date=f"{today.year}{today.month}/{35}")

        # invalid search
        with self.assertRaises(ValueError):
            Bar.objects.filter(date__month="test")


class BarTimeTestCase(TestCase):
    def setUp(self):
        self.date_string = "1380-08-02"
        self.datetime = jdatetime.datetime(1380, 8, 2, 12, 12, 12)
        self.bar_time = BarTime.objects.create(name="bar time", datetime=self.datetime)

    def test_save_datetime(self):
        self.assertEqual(self.bar_time.datetime, self.datetime)

    def test_default_value(self):
        obj = DateTimeWithDefault.objects.create()
        self.assertEqual(
            obj.datetime1, jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000)
        )
        self.assertEqual(
            obj.datetime2, jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000)
        )

    def test_save_specific_datetime(self):
        BarTime.objects.create(name="Test", datetime="1398-04-31 12:12:12")
        k = BarTime.objects.filter(datetime="1398-04-31 12:12:12")
        self.assertEqual(k[0].datetime.day, 31)

    def test_date_lookup_filter(self):
        jdatetime_ = jdatetime.datetime(1378, 10, 10)
        bartime = BarTime.objects.create(name="Test", datetime=jdatetime_)
        self.assertEqual(BarTime.objects.get(datetime__date=jdatetime_), bartime)
        self.assertEqual(BarTime.objects.get(datetime__date=jdatetime_.date()), bartime)
        self.assertEqual(BarTime.objects.get(datetime__date="1378-10-10"), bartime)
        with self.assertRaisesMessage(
            TypeError,
            "`__date` filter Expected jdatetime.datetime, jdatetime.date or str, got `int`.",
        ):
            BarTime.objects.get(datetime__date=1)

    def test_filter_by_exact_datetime(self):
        bar_times = BarTime.objects.filter(datetime=self.datetime)
        self.assertEqual(len(bar_times), 1)

    @requires_tz_support
    @skipUnlessDBFeature("has_zoneinfo_database")
    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Tehran")
    def test_lookup_date_with_use_tz(self):
        current_timezone = timezone.get_current_timezone()
        jdt1 = jdatetime.datetime(
            1392, 3, 12, 10, 22, 23, 240000, tzinfo=current_timezone
        )

        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), "1392-03-12 10:22:23.240000+0430")
        self.assertEqual(k[0].datetime.strftime("%z"), "+0430")

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Tehran")
    def test_lookup_date_with_use_tz_without_explicit_tzinfo(self):
        jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), "1392-03-12 10:22:23.240000+0430")
        self.assertEqual(k[0].datetime.strftime("%z"), "+0430")

    @requires_tz_support
    @override_settings(USE_TZ=False, TIME_ZONE="Asia/Tehran")
    def test_lookup_date_with_no_tz(self):
        jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), "1392-03-12 10:22:23.240000")
        self.assertEqual(k[0].datetime.strftime("%z"), "")

    def test_lookup_auto_now_add(self):
        ModelWithAutoNowAdd.objects.create()
        dt = ModelWithAutoNowAdd.objects.all()[0].datetimefield
        objects = ModelWithAutoNowAdd.objects.filter(datetimefield=dt)
        self.assertEqual(objects[0].datetimefield, dt)

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Tehran")
    def test_lookup_auto_now_add_datetime_with_tz(self):
        ModelWithAutoNowAdd.objects.create()
        dt = ModelWithAutoNowAdd.objects.all()[0].datetimefield
        objects = ModelWithAutoNowAdd.objects.filter(datetimefield=dt)
        self.assertEqual(objects[0].datetimefield, dt)

    def test_serialize_default_jdatetime_value(self):
        jdt1 = jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000)
        field = jmodels.jDateTimeField(default=jdt1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                "django_jalali.db.models.jDateTimeField("
                "default=datetime.datetime(2011, 9, 22, 10, 22, 23, 240000))",
                {"import django_jalali.db.models", "import datetime"},
            ),
        )

    def test_serialize_default_datetime_value(self):
        dt1 = datetime.datetime(2013, 6, 2, 10, 22, 23, 240000)
        field = jmodels.jDateTimeField(default=dt1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                "django_jalali.db.models.jDateTimeField("
                "default=datetime.datetime(2013, 6, 2, 10, 22, 23, 240000))",
                {"import django_jalali.db.models", "import datetime"},
            ),
        )

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE="Asia/Tehran")
    def test_timezone(self):
        current_timezone = timezone.get_current_timezone()
        jdt1 = jdatetime.datetime(
            1392, 3, 12, 10, 22, 23, 240000, tzinfo=current_timezone
        )

        new_bartime = BarTime.objects.create(name="with timezone", datetime=jdt1)
        self.assertEqual(
            new_bartime.datetime.utcoffset(),
            datetime.timedelta(seconds=16200),
        )

        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(
            k[0].datetime.utcoffset(),
            datetime.timedelta(seconds=16200),
        )

    def test_chain_filters(self):
        qs = BarTime.objects.filter(name=self.bar_time.name).filter(
            datetime__year=self.datetime.year
        )
        self.assertEqual(qs.count(), 1)
