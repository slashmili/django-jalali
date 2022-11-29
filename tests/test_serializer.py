import jdatetime
from django.test import RequestFactory, TestCase

from tests.models import Bar, BarTime
from tests.serializers import JDateFieldSerializer, JDateTimeFieldSerializer


class JDateFieldSerializerTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()

        # Bars
        self.mybar = Bar.objects.create(name="foo", date=self.today)

    def test_serializers_works_correctly_on_valid_date(self):
        serializer = JDateFieldSerializer(self.mybar)
        self.assertEqual(serializer.data["date"], str(self.today))

        serializer = JDateFieldSerializer(data={"name": "foo", "date": "1400-06-31"})
        self.assertTrue(serializer.is_valid())

    def test_serializers_works_correctly_on_leap_year(self):
        """
        Make sure JDateFieldSerializer work's correctly on leap and normal year
        """
        # Date is not a leap yaer, So this is not acceptable
        serializer = JDateFieldSerializer(
            data={"name": "leap-year", "date": "1400-12-30"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("date", serializer.errors)

        # Date is a leap year and is acceptable
        serializer = JDateFieldSerializer(
            data={"name": "leap-year", "date": "1399-12-30"}
        )
        self.assertTrue(serializer.is_valid())

    def test_serializer_save_date_correctly(self):
        data = {"name": "fooo", "date": "1400-12-29"}
        serializer = JDateFieldSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        bar = Bar.objects.get(name="fooo")
        self.assertEqual(str(bar.date), data["date"])


class JDateTimeFieldSerializerTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()
        self.now = jdatetime.datetime.now()

        # Bars
        self.mybartime = BarTime.objects.create(name="bartime", datetime=self.now)

    def test_serializer_works_correctly_on_valid_datetime(self):
        serializer = JDateTimeFieldSerializer(self.mybartime)
        self.assertEqual(serializer.data["datetime"], str(self.now))

        serializer = JDateTimeFieldSerializer(
            data={"name": "bartime", "datetime": "1401-06-31"}
        )
        self.assertTrue(serializer.is_valid())

        serializer = JDateTimeFieldSerializer(
            data={"name": "bartime", "datetime": "1401-06-31 00:00"}
        )
        self.assertTrue(serializer.is_valid())

        serializer = JDateTimeFieldSerializer(
            data={"name": "bartime", "datetime": "1401-06-31 01:01:00"}
        )
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_different_formatting(self):
        d_time = self.now.strftime("%Y-%m-%d %H:%M")
        bartime_object = BarTime.objects.create(name="formatted", datetime=d_time)
        self.assertEqual(
            JDateTimeFieldSerializer(bartime_object).data["datetime"], d_time
        )

    def test_serializer_with_invalid_datetime(self):
        serializer = JDateTimeFieldSerializer(
            data={"name": "bartime", "datetime": "1400-12-30 12:34:12"}
        )
        self.assertFalse(serializer.is_valid())

        serializer = JDateTimeFieldSerializer(
            data={"name": "bartime", "datetime": "1400-12-28 26:34:12"}
        )
        self.assertFalse(serializer.is_valid())
