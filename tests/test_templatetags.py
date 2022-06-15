import jdatetime
from django.template import Context, Template
from django.test import TestCase


class JformatTestCase(TestCase):
    def setUp(self):
        date_time = jdatetime.date(1394, 11, 25)
        self.context = Context({"date_time": date_time})

    def test_jformat(self):
        _str = '{% load jformat %}{{ date_time|jformat:"%c" }}'
        output = "Sun Bah 25 00:00:00 1394"
        t = Template(_str)
        self.assertEqual(t.render(self.context), output)

    def test_jformat_unicode(self):
        _str = "{% load jformat %}"
        _str += '{{ date_time|jformat:"ﺱﺎﻟ = %y، ﻡﺎﻫ = %m، ﺭﻭﺯ = %d" }}'
        output = "ﺱﺎﻟ = 94، ﻡﺎﻫ = 11، ﺭﻭﺯ = 25"
        t = Template(_str)
        self.assertEqual(t.render(self.context), output)
