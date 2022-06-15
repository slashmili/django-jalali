from rest_framework.serializers import ModelSerializer

from django_jalali.serializers.serializerfield import (
    JDateField,
    JDateTimeField,
)

from .models import Bar, BarTime


class JDateFieldSerializer(ModelSerializer):
    date = JDateField()

    class Meta:
        model = Bar
        exclude = []


class JDateTimeFieldSerializer(ModelSerializer):
    datetime = JDateTimeField()

    class Meta:
        model = BarTime
        exclude = []
