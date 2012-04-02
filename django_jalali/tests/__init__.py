from django.test import TestCase
from django.core import exceptions
from django.db.utils import IntegrityError
import jdatetime
import datetime


from django_jalali.tests.models import jDateModel, jDateTimeModel

from  custom_settings import change_settings
settings_manager = change_settings(append_apps=['django_jalali.tests'])




class CreateModelTestCase(TestCase):
    def tearDown(self):
        global settings_manager
        settings_manager.revert()

    def test_simple_save(self):
        """test simple function, including saving and retrieving jalali date from database"""
        jd_model = jDateModel(date=jdatetime.date.today())
        jd_model.save()
        d = jDateModel.objects.filter(date=jdatetime.date.today())
        self.assertEqual(d[0].date.togregorian(), datetime.date.today())
        
        j_date_time = jdatetime.datetime.today()
        jdt_model = jDateTimeModel(date_time=j_date_time)
        jdt_model.save()
        dt = jDateTimeModel.objects.filter(date_time=j_date_time)
        self.assertEqual(dt[0].date_time.togregorian(), j_date_time.togregorian())
    def test_diffrent_saveing(self):
        jd_model = jDateModel(date='1391-01-01')
        jd_model.save()

        jd_model = jDateModel(date=datetime.datetime.now())
        jd_model.save()

        jd_model = jDateModel()
        jd_model.save()

        jd_model = jDateModel(date=jdatetime.datetime.now())
        jd_model.save()

        #to_python
        jdt_model = jDateTimeModel(date_time='1391-01-01')
        #TODO: Find the correct exceptions
        #with self.assertRaises(Exception):
        #    jdt_model.date_time = None
        
        jdt_model.date_time = datetime.datetime(1390,01,02)
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=datetime.datetime(1390,01,02))[0].date_time , jdt_model.date_time)
        
        jdt_model.date_time = jdatetime.date.today()
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=jdatetime.date.today())[0].date_time, jdt_model.date_time)

        jdt_model.date_time = datetime.date.today()
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=datetime.date.today())[0].date_time, jdt_model.date_time)

        jdt_model.date_time = datetime.date(1390,01,01)
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=jdatetime.date(1390,01,01))[0].date_time, jdt_model.date_time)

        jdt_model.date_time = '1391-01-01 12:12'
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=jdatetime.datetime(1391,01,01,12,12))[0].date_time, jdt_model.date_time)
        

        jdt_model.date_time = '1391-01-01 12:12:12'
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time=jdatetime.datetime(1391,01,01,12,12,12))[0].date_time, jdt_model.date_time)

        jdt_model.date_time = '2012-01-01 12:12'
        jdt_model.save()
        #TODO: fixus, we'r broken
        #self.assertEqual(jDateTimeModel.objects.filter(date_time='2012-01-01 12:12')[0].date_time, jdt_model.date_time)
        #self.assertEqual(jDateTimeModel.objects.filter(date_time=datetime.datetime(2012, 01, 01, 12, 12))[0].date_time, jdt_model.date_time)
        jdt_model.date_time = '2012-01-01 12:12:12'

        jdt_model.date_time = '1391-01-01 12:12:12.2222'
        jdt_model.save()
        self.assertEqual(jDateTimeModel.objects.filter(date_time = '1391-01-01 12:12:12.2222')[0] , jdt_model)

    def test_filtering(self):
        """test filtering"""
        today = jdatetime.date.today()
        jd_model = jDateModel(date=today)
        jd_model.save()
        dt = jDateModel.objects.filter(date__year=today.year)
        print jDateModel.objects.filter(date="%s-%s-%s"%(today.year, today.month, today.day))
        today = datetime.date.today()
        jd_model = jDateModel(date=today)
        jd_model.save()
        print jDateModel.objects.filter(date=today)
        print jDateModel.objects.filter(date="%s-%s-%s"%(today.year, today.month, today.day))
        print str(jDateModel.objects.filter(date__in =["%s-%s-%s"%(today.year, today.month, today.day)]))
        try :
            print str(jDateModel.objects.filter(date__how =["%s-%s-%s"%(today.year, today.month, today.day)]))
        except :
            pass




        #wrong day value
        with self.assertRaises(exceptions.ValidationError):
            jDateModel.objects.filter(date="%s-%s-%s"%(today.year, today.month, 35))

        #invalid format
        with self.assertRaises(exceptions.ValidationError):
            jDateModel.objects.filter(date="%s%s/%s"%(today.year, today.month, 35))

        #invalid search
        with self.assertRaises(ValueError):
            jDateModel.objects.filter(date__month="12")

