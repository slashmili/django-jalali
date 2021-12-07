import datetime
from urllib.parse import unquote

import jdatetime
from django import get_version
from django.contrib.admin import site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db.migrations.writer import MigrationWriter
from django.template import Context, Template
from django.test import (
    RequestFactory, TestCase, override_settings, skipUnlessDBFeature,
)
from django.test.utils import requires_tz_support
from django.utils import timezone
from django.utils.encoding import force_str
from foo.admin import BarTimeAdmin
from foo.models import (
    Bar, BarTime, DateTimeWithDefault, DateWithDefault, ModelWithAutoNowAdd,
)

from django_jalali.db import models as jmodels

from .serializers import JDateFieldSerializer, JDateTimeFieldSerializer


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

    def test_save_specific_datetime(self):
        Bar.objects.create(name='Test', date='1398-04-31')
        k = Bar.objects.filter(date='1398-04-31')
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
                'django_jalali.db.models.jDateField(default=datetime.date(2011, 9, 22))',
                {'import django_jalali.db.models', 'import datetime'}
            )
        )

    def test_serialize_default_datetime_value(self):
        dt1 = datetime.date(2013, 6, 2)
        field = jmodels.jDateField(default=dt1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                'django_jalali.db.models.jDateField(default=datetime.date(2013, 6, 2))',
                {'import django_jalali.db.models', 'import datetime'}
            )
        )

    def test_filtering(self):
        today = jdatetime.date.today()
        Bar.objects.create(date=today, name='test name')

        # search by year
        jdm_date = Bar.objects.filter(date__year=today.year)
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date.year, today.year)

        # search by string
        jdm_date = Bar.objects.filter(date='%s-%s-%s' % (today.year, today.month, today.day))
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        # save by geregorian date and retrive by jalali date
        g_2009 = datetime.date(2009, 9, 9)
        jd_model = Bar(date=g_2009)
        jd_model.save()

        jdm_date = Bar.objects.filter(date=g_2009)
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, jdatetime.date.fromgregorian(date=g_2009))

        jdm_date = Bar.objects.filter(date='%s-%s-%s' % (today.year, today.month, today.day))
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        jdm_date = Bar.objects.filter(date__in=['%s-%s-%s' % (today.year, today.month, today.day)])
        self.assertEqual(len(jdm_date), 1)
        self.assertEqual(jdm_date[0].date, today)

        # wrong day value
        with self.assertRaises(ValidationError):
            Bar.objects.filter(date='%s-%s-%s' % (today.year, today.month, 35))

        # invalid format
        with self.assertRaises(ValidationError):
            Bar.objects.filter(date='%s%s/%s' % (today.year, today.month, 35))

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
        self.assertEqual(obj.datetime1, jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000))
        self.assertEqual(obj.datetime2, jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000))

    def test_save_specific_datetime(self):
        BarTime.objects.create(name='Test', datetime='1398-04-31 12:12:12')
        k = BarTime.objects.filter(datetime='1398-04-31 12:12:12')
        self.assertEqual(k[0].datetime.day, 31)

    def test_filter_by_exact_datetime(self):
        bar_times = BarTime.objects.filter(datetime=self.datetime)
        self.assertEqual(len(bar_times), 1)

    @requires_tz_support
    @skipUnlessDBFeature('has_zoneinfo_database')
    @override_settings(USE_TZ=True, TIME_ZONE='Asia/Tehran')
    def test_lookup_date_with_use_tz(self):
        current_timezone = timezone.get_current_timezone()
        if get_version() >= '4.0':
            jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000, tzinfo=current_timezone)
        else:
            jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
            jdt1 = current_timezone.localize(jdt1)

        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), '1392-03-12 10:22:23.240000+0430')
        self.assertEqual(k[0].datetime.strftime('%z'), '+0430')

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE='Asia/Tehran')
    def test_lookup_date_with_use_tz_without_explicit_tzinfo(self):
        jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), '1392-03-12 10:22:23.240000+0430')
        self.assertEqual(k[0].datetime.strftime('%z'), '+0430')

    @requires_tz_support
    @override_settings(USE_TZ=False, TIME_ZONE='Asia/Tehran')
    def test_lookup_date_with_no_tz(self):
        jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
        BarTime.objects.create(name="with timezone", datetime=jdt1)
        k = BarTime.objects.filter(datetime=jdt1)
        self.assertEqual(str(k[0].datetime), '1392-03-12 10:22:23.240000')
        self.assertEqual(k[0].datetime.strftime('%z'), '')

    def test_lookup_auto_now_add(self):
        ModelWithAutoNowAdd.objects.create()
        dt = ModelWithAutoNowAdd.objects.all()[0].datetimefield
        objects = ModelWithAutoNowAdd.objects.filter(datetimefield=dt)
        self.assertEqual(objects[0].datetimefield, dt)

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE='Asia/Tehran')
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
                'django_jalali.db.models.jDateTimeField('
                'default=datetime.datetime(2011, 9, 22, 10, 22, 23, 240000))',
                {'import django_jalali.db.models', 'import datetime'}
            )
        )

    def test_serialize_default_datetime_value(self):
        dt1 = datetime.datetime(2013, 6, 2, 10, 22, 23, 240000)
        field = jmodels.jDateTimeField(default=dt1)
        self.assertEqual(
            MigrationWriter.serialize(field),
            (
                'django_jalali.db.models.jDateTimeField('
                'default=datetime.datetime(2013, 6, 2, 10, 22, 23, 240000))',
                {'import django_jalali.db.models', 'import datetime'}
            )
        )

    @requires_tz_support
    @override_settings(USE_TZ=True, TIME_ZONE='Asia/Tehran')
    def test_timezone(self):
        current_timezone = timezone.get_current_timezone()
        if get_version() >= '4.0':
            jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000, tzinfo=current_timezone)
        else:
            jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
            jdt1 = current_timezone.localize(jdt1)

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
        qs = BarTime.objects.filter(name=self.bar_time.name).filter(datetime__year=self.datetime.year)
        self.assertEqual(qs.count(), 1)


class JformatTestCase(TestCase):

    def setUp(self):
        date_time = jdatetime.date(1394, 11, 25)
        self.context = Context({'date_time': date_time})

    def test_jformat(self):
        _str = '{% load jformat %}{{ date_time|jformat:"%c" }}'
        output = 'Sun Bah 25 00:00:00 1394'
        t = Template(_str)
        self.assertEqual(t.render(self.context), output)

    def test_jformat_unicode(self):
        _str = u'{% load jformat %}'
        _str += u'{{ date_time|jformat:"ﺱﺎﻟ = %y، ﻡﺎﻫ = %m، ﺭﻭﺯ = %d" }}'
        output = u"ﺱﺎﻟ = 94، ﻡﺎﻫ = 11، ﺭﻭﺯ = 25"
        t = Template(_str)
        self.assertEqual(t.render(self.context), output)


def select_by(dictlist, key, value):
    return [x for x in dictlist if x[key] == value][0]


class ListFiltersTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()
        self.tomorrow = self.today + jdatetime.timedelta(days=1)
        self.one_week_ago = self.today - jdatetime.timedelta(days=7)
        if self.today.month == 12:
            self.next_month = self.today.replace(year=self.today.year + 1, month=1, day=1)
        else:
            self.next_month = self.today.replace(month=self.today.month + 1, day=1)
        self.next_year = self.today.replace(year=self.today.year + 1, month=1, day=1)

        # Bars
        self.mybartime = BarTime.objects.create(name="foo", datetime=self.today)

    def test_jdatefieldlistfilter(self):
        modeladmin = BarTimeAdmin(BarTime, site)

        request = self.request_factory.get('/')
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)
        request = self.request_factory.get(
            '/',
            {
                'datetime__gte': self.today.strftime('%Y-%m-%d %H:%M:%S'),
                'datetime__lt': self.tomorrow.strftime('%Y-%m-%d %H:%M:%S')
            },
        )
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)

        # Make sure the correct queryset is returned
        queryset = changelist.get_queryset(request)
        self.assertEqual(list(queryset), [self.mybartime])

        # Make sure the correct choice is selected
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), 'datetime')
        choice = select_by(filterspec.choices(changelist), "display", "Today")
        self.assertEqual(choice['selected'], True)

        self.assertEqual(
            unquote(choice['query_string']).replace('+', ' '),
            '?datetime__gte=%s&datetime__lt=%s' % (
                self.today.strftime('%Y-%m-%d %H:%M:%S'),
                self.tomorrow.strftime('%Y-%m-%d %H:%M:%S'),
            )
        )

        request = self.request_factory.get(
            '/',
            {
                'datetime__gte': self.today.replace(day=1),
                'datetime__lt': self.next_month
            },
        )
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)

    def get_changelist(self, request, model, modeladmin):
        args = [
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
            modeladmin.sortable_by,
        ]
        if get_version() >= '4.0':
            args.append(modeladmin.search_help_text)
        return ChangeList(*args)


class JDateFieldSerializerTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()

        # Bars
        self.mybar = Bar.objects.create(name="foo", date=self.today)

    def test_serializers_works_correctly_on_valid_date(self):
        serializer = JDateFieldSerializer(self.mybar)
        self.assertEqual(serializer.data['date'], str(self.today))

    def test_serializers_works_correctly_on_leap_year(self):
        """
        Make sure JDateFieldSerializer work's correctly on leap and normal year
        """
        # Date is not a leap yaer, So this is not acceptable
        serializer = JDateFieldSerializer(
            data={'name': 'leap-year', 'date': '1400-12-30'}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

        # Date is a leap year and is acceptable
        serializer = JDateFieldSerializer(
            data={'name': 'leap-year', 'date': '1399-12-30'}
        )
        self.assertTrue(serializer.is_valid())

    def test_serializer_save_date_correctly(self):
        data = {'name': 'fooo', 'date': '1400-12-29'}
        serializer = JDateFieldSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        bar = Bar.objects.get(name='fooo')
        self.assertEqual(str(bar.date), data['date'])


class JDateTimeFieldSerializerTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()
        self.now = jdatetime.datetime.now()

        # Bars
        self.mybartime = BarTime.objects.create(name="bartime", datetime=self.now)

    def test_serializer_works_correctly_on_valid_datetime(self):
        serializer = JDateTimeFieldSerializer(self.mybartime)
        self.assertEqual(
            serializer.data['datetime'],
            str(self.now)
            )

    def test_serializer_with_different_formatting(self):
        d_time = self.now.strftime("%Y-%m-%d %H:%M")
        bartime_object = BarTime.objects.create(name="formatted", datetime=d_time)
        self.assertEqual(
            JDateTimeFieldSerializer(bartime_object).data['datetime'],
            d_time
            )

    def test_serializer_with_invalid_datetime(self):
        serializer = JDateTimeFieldSerializer(
            data={'name': 'bartime', 'datetime': "1400-12-30 12:34:12"}
        )
        self.assertFalse(serializer.is_valid())

        serializer = JDateTimeFieldSerializer(
            data={'name': 'bartime', 'datetime': "1400-12-28 26:34:12"}
        )
        self.assertFalse(serializer.is_valid())
