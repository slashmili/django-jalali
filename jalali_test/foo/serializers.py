from rest_framework.serializers import ModelSerializer

from django_jalali.serializers.serializerfield import (
    JDateField as JDateFieldSerializer,
)

from .models import Bar


class JDateFieldSerialializer(ModelSerializer):
    date = JDateFieldSerializer()

    class Meta:
        model = Bar
        exclude = []
