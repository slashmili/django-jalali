import datetime

import jdatetime
from django.db import models
from django_jalali.db import models as jmodels


class Bar(models.Model):
    objects = jmodels.jManager()
    name = models.CharField(max_length=200)
    date = jmodels.jDateField()


class DateWithDefault(models.Model):
    objects = jmodels.jManager()
    date1 = jmodels.jDateTimeField(default=jdatetime.datetime(1390, 6, 31))
    date2 = jmodels.jDateTimeField(default=datetime.datetime(2011, 9, 22))


class BarTime(models.Model):
    objects = jmodels.jManager()
    name = models.CharField(max_length=200)
    datetime = jmodels.jDateTimeField()


class DateTimeWithDefault(models.Model):
    objects = jmodels.jManager()
    datetime1 = jmodels.jDateTimeField(default=jdatetime.datetime(1390, 6, 31, 10, 22, 23, 240000))
    datetime2 = jmodels.jDateTimeField(default=datetime.datetime(2011, 9, 22, 10, 22, 23, 240000))


class ModelWithAutoNowAdd(models.Model):
    objects = jmodels.jManager()
    datetimefield = jmodels.jDateTimeField(auto_now_add=True)
