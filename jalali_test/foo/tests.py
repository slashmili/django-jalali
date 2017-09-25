# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.utils.encoding import force_text
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import site
from django.template import Context, Template

from foo.models import Bar, BarTime
import jdatetime
from django_jalali.templatetags import jformat
try:
    from urllib import unquote  # Python 2.X
except ImportError:
    from urllib.parse import unquote  # Python 3+

from foo.admin import BarTimeAdmin

class BarTestCase(TestCase):

    def setUp(self):
        self.today_string = "1390-5-12"
        self.today = jdatetime.date(1390, 5, 12)
        self.mybar = Bar(name="foo", date=self.today)
        self.mybar.save()

    def test_save_date(self):
        self.assertEqual(self.mybar.date, self.today)

    def test_filter_by_exact_date(self):
        bars = Bar.objects.filter(date=self.today_string)
        self.assertEqual(len(bars), 1)

    def test_filter_by_exact_date_no_match(self):
        bars = Bar.objects.filter(date="1390-5-11")
        self.assertEqual(len(bars), 0)


    def test_filter_by_gte_date(self):
        bars = Bar.objects.filter(date__gte=self.today_string)
        self.assertEqual(len(bars), 1)

class BarTimeTestCase(TestCase):

    def setUp(self):
        self.date_string = "1380-08-02"
        self.datetime = jdatetime.datetime(1380,8,2,12,12,12)
        self.bar_time = BarTime(name="foo time", datetime=self.datetime)
        self.bar_time.save()

    def test_save_date(self):
        self.assertEqual(self.bar_time.datetime, self.datetime)

    def test_filter_by_exact_datetime(self):
        bar_times = BarTime.objects.filter(datetime=self.datetime)
        self.assertEqual(len(bar_times), 1)


class  JformatTestCase(TestCase):

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

        #Bars
        self.mybartime = BarTime.objects.create(name="foo", datetime=self.today)


    def test_jdatefieldlistfilter(self):
        modeladmin = BarTimeAdmin(BarTime, site)

        request = self.request_factory.get('/')
        changelist = self.get_changelist(request, BarTime, modeladmin)
        request = self.request_factory.get('/', {'datetime__gte': self.today.strftime('%Y-%m-%d %H:%M:%S'),
                                                 'datetime__lt': self.tomorrow.strftime('%Y-%m-%d %H:%M:%S')})

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

        request = self.request_factory.get('/', {'datetime__gte': self.today.replace(day=1),
                                                 'datetime__lt': self.next_month})
        changelist = self.get_changelist(request, BarTime, modeladmin)

    def get_changelist(self, request, model, modeladmin):
        return ChangeList(
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
        )
