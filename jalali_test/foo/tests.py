# -*- coding: utf-8 -*-
import datetime

from django.db.migrations.writer import MigrationWriter
from django.test import (
    TestCase, RequestFactory, override_settings, skipUnlessDBFeature,
)
from django.test.utils import requires_tz_support
from django.utils.encoding import force_text
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import site
from django.contrib.auth.models import AnonymousUser
from django.template import Context, Template
from django_jalali.db import models as jmodels

from django import get_version
from django.utils import timezone

from foo.models import Bar, BarTime, DateWithDefault, DateTimeWithDefault
import jdatetime
from urllib.parse import unquote

from foo.admin import BarTimeAdmin


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
        jdt1 = jdatetime.datetime(1392, 3, 12, 10, 22, 23, 240000)
        jdt1 = current_timezone.localize(jdt1)

        new_bartime = BarTime.objects.create(name="with timezone", datetime=jdt1)
        self.assertTrue(hasattr(new_bartime.datetime.tzinfo, 'localize'))
        self.assertEqual(
            new_bartime.datetime.tzinfo.utcoffset(new_bartime.datetime),
            datetime.timedelta(seconds=16200),
        )

        k = BarTime.objects.filter(datetime=jdt1)
        self.assertTrue(hasattr(k[0].datetime.tzinfo, 'localize'))
        self.assertEqual(
            k[0].datetime.tzinfo.utcoffset(k[0].datetime),
            datetime.timedelta(seconds=16200),
        )


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
        self.assertEqual(force_text(filterspec.title), 'datetime')
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
        ]
        if get_version() >= '2.1':
            args.append(modeladmin.sortable_by)
        return ChangeList(*args)
