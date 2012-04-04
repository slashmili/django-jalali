from django.db import models
from django_jalali.db import models as jmodels

class jDateModel(models.Model):
    objects = jmodels.jManager()
    date    = jmodels.jDateField()
    def __repr__(self):
        return str(self.date)

class jDateModelAutoNow(models.Model):
    objects = jmodels.jManager()
    date    = jmodels.jDateField(auto_now=True)
    def __repr__(self):
        return str(self.date)


class jDateTimeModel(models.Model):
    objects   = jmodels.jManager()
    date_time = jmodels.jDateTimeField()

class jDateTimeModelAutoNow(models.Model):
    objects   = jmodels.jManager()
    date_time = jmodels.jDateTimeField(auto_now=True)
