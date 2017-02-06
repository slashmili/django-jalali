Django Jalali
=============

This module gives you a DateField same as Django’s DateField but you can
get and query data based on Jalali Date

Status
------

.. image:: https://travis-ci.org/slashmili/django-jalali.svg?branch=master
   :target: https://travis-ci.org/slashmili/django-jalali

.. image:: https://img.shields.io/pypi/v/django_jalali.svg
   :target: https://pypi.python.org/pypi/django_jalali

.. image:: https://img.shields.io/pypi/dm/django_jalali.svg


Dependencies
------------

-  jdatetime_
-  Django_ > 1.7


Install
-------
``pip install django_jalali``

Usage
-----

1. Run :

.. code:: bash

  $ django-admin.py startproject jalali_test

2. Start your app :

.. code:: bash

  $ python manage.py startapp foo

3. Edit settings.py and add django_jalali and your foo to your INSTALLED_APPS (also config DATABASES setting) and set the date and time format settings.

    django_jalali should be added **before** your apps in order to work properly
    
.. code:: bash

      DATE_INPUT_FORMATS = ['%Y/%m/%d', '%Y-%m-%d']
      DATETIME_INPUT_FORMATS = ['%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S']

4. Edit foo/models.py

.. code:: python

    from django.db import models
    from django_jalali.db import models as jmodels

    class Bar(models.Model):
        objects = jmodels.jManager()
        name =  models.CharField(max_length=200)
        date =  jmodels.jDateField()
        def __str__(self):
            return "%s, %s"%(self.name, self.date)
    class BarTime(models.Model):
        objects = jmodels.jManager()
        name =  models.CharField(max_length=200)
        datetime = jmodels.jDateTimeField()
        def __str__(self):
            return "%s, %s" %(self.name, self.datetime)

5. Run

.. code:: bash

    $ python manage.py syncdb

6. Test it

.. code:: shell

    $ python manage.py shell
    Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39)
    [GCC 4.4.5] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from foo.models import Bar
    >>> import jdatetime
    >>> today = jdatetime.date(1390, 5, 12)
    >>> mybar = Bar(name="foo", date=today)
    >>> mybar.save()
    >>> mybar.date
    jdatetime.date(1390, 5, 12)
    >>> Bar.objects.filter(date=today)
    [<Bar: foo, 1390-05-12>]
    >>> Bar.objects.filter(date__gte="1390-5-12")
    [<Bar: foo, 1390-05-12>]
    >>> Bar.objects.filter(date='1363-8-01')
    []
    >>> from foo.models import BarTime
    >>> BarTime(name="Bar Time now", datetime=jdatetime.datetime(1380,8,2,12,12,12)).save()
    >>> BarTime.objects.filter(datetime__lt= jdatetime.datetime(1380,8,2,12,12,12 ))
    []
    >>> BarTime.objects.filter(datetime__lte= jdatetime.datetime(1380,8,2,12,12,12 ))
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__gt='1380-08-02')
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__gt=d)
    []
    >>> BarTime.objects.filter(datetime__year=1380)
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]

Using Templatetags
------------------

1. You can use `jformat` filter to format your dates in templates:

.. code:: python

    {% load jformat %}
    {{ my_date|jformat }} {# default formatting #}
    {{ my_date|jformat:"%A %d %B %Y %H:%M" }} {# specific formatting #}

Admin Interface
---------------


1. Create foo/admin.py

.. code:: python

    from foo.models import Bar,BarTime
    from django.contrib import admin

    from django_jalali.admin.filters import JDateFieldListFilter

    #you need import this for adding jalali calander widget
    import django_jalali.admin as jadmin

    class BarAdmin(admin.ModelAdmin):
        list_filter = (
            ('date', JDateFieldListFilter),
        )


    admin.site.register(Bar, BarAdmin)

    class BarTimeAdmin(admin.ModelAdmin):
        list_filter = (
            ('datetime', JDateFieldListFilter),
        )

    admin.site.register(BarTime, BarTimeAdmin)

2. Config admin interface and fire up your django and enjoy using jalali date !


Locale
------
In order to get the date string in farsi you need to set the locale to fa_IR

There are two ways to do achieve that, you can use of the approaches based on your needs 

* Run server with LC_ALL env:

.. code:: shell

    $ LC_ALL=fa_IR python manage.py runserver
 
* Set the locale in settings.py

.. code:: python

    LANGUAGE_CODE = 'fa-ir'
    import locale
    locale.setlocale(locale.LC_ALL, "fa_IR")
   

.. _jdatetime: https://github.com/slashmili/python-jalali
.. _Django: https://www.djangoproject.com/
