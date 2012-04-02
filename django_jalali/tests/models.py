from django.db import models
from django_jalali.db import models as jmodels

class jDateModel(models.Model):
    objects = jmodels.jManager()
    date    = jmodels.jDateField(auto_now=True)

class jDateTimeModel(models.Model):
    objects   = jmodels.jManager()
    date_time = jmodels.jDateTimeField()
