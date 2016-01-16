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
