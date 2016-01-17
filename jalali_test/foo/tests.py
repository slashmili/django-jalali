from django.test import TestCase

from foo.models import Bar, BarTime
import jdatetime

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
