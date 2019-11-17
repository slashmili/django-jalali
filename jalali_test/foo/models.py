from django.db import models
from django_jalali.db import models as jmodels


class Bar(models.Model):
    objects = jmodels.jManager()
    name = models.CharField(max_length=200)
    date = jmodels.jDateField()

    def __str__(self):
        return "%s, %s" % (self.name, self.date)


class BarTime(models.Model):
    objects = jmodels.jManager()
    name = models.CharField(max_length=200)
    datetime = jmodels.jDateTimeField()

    def __str__(self):
        return "%s, %s" % (self.name, self.datetime)
