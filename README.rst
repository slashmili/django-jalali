Django Jalali
=============

This module gives you a DateField same as Django’s DateField but you can
get and query data based on Jalali Date

Status
------

.. image:: https://github.com/slashmili/django-jalali/workflows/Tests/badge.svg?branch=main
   :target: https://github.com/slashmili/django-jalali/actions

.. image:: https://img.shields.io/pypi/v/django_jalali.svg
   :target: https://pypi.python.org/pypi/django_jalali

.. image:: https://img.shields.io/pypi/pyversions/django-jalali.svg
   :target: https://pypi.org/project/django_jalali

.. image:: https://img.shields.io/pypi/djversions/django-jalali.svg
   :target: https://pypi.org/project/django-jalali/

Dependencies
------------

-  jdatetime_
-  Django_ > 4.2

    Looking for Django 1.X support? Checkout *2.4.6* version in pypi.org
- `Django REST Framework`_ > 3.12 (If install with ``drf`` dependency)

Supported Databases
-------------------

- SQLite
- PostgreSQL

Install
-------
.. code:: bash

   pip install django_jalali

To use DRF serializer field:

.. code:: bash

   pip install django_jalali[drf]

Usage
-----

1. Run :

.. code:: bash

  $ django-admin startproject jalali_test

2. Start your app :

.. code:: bash

  $ python manage.py startapp foo

3. Edit your Django project's ``settings.py`` file to include ``django_jalali`` and your application in the ``INSTALLED_APPS`` list. Make sure that ``django_jalali`` is listed **before** your apps for proper functionality.

   Additionally, you can configure library settings using the ``JALALI_SETTINGS`` dictionary. If a setting is not explicitly defined, the default values will be used.

   .. code-block:: python

      # settings.py
      INSTALLED_APPS = [
          "django.contrib.admin",
          "django.contrib.auth",
          "django.contrib.contenttypes",
          "django.contrib.sessions",
          "django.contrib.messages",
          "django.contrib.staticfiles",
          "django_jalali",  # Place this before your custom apps
      ]

      JALALI_SETTINGS = {
          # JavaScript static files for the admin Jalali date widget
          "ADMIN_JS_STATIC_FILES": [
              "admin/jquery.ui.datepicker.jalali/scripts/jquery-1.10.2.min.js",
              "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js",
              "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js",
              "admin/jquery.ui.datepicker.jalali/scripts/calendar.js",
              "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js",
              "admin/main.js",
          ],
          # CSS static files for the admin Jalali date widget
          "ADMIN_CSS_STATIC_FILES": {
              "all": [
                  "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
                  "admin/css/main.css",
              ]
          },
      }

4. Edit foo/models.py_

.. code:: python

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

5. Run

.. code:: bash

    $ python manage.py makemigrations
    Migrations for 'foo':
      foo/migrations/0001_initial.py:
         - Create model Bar
         - Create model BarTime
    $ python manage.py migrate
    Running migrations:
        Applying foo.0001_initial... OK

6. Test it

.. code:: shell

    $ python manage.py shell
    Python 3.8.18 (default, Nov 26 2018, 15:26:54)
    [GCC 6.3.0 20170516] on linux
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
    >>> BarTime.objects.filter(datetime__date=jdatetime.datetime(1380,8,2,12,12,12))
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__date=jdatetime.date(1380,8,2))
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__date="1380-08-02")
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__lt=jdatetime.datetime(1380,8,2,12,12,12))
    []
    >>> BarTime.objects.filter(datetime__lte=jdatetime.datetime(1380,8,2,12,12,12))
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__gt='1380-08-02')
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]
    >>> BarTime.objects.filter(datetime__gt=d)
    []
    >>> BarTime.objects.filter(datetime__year=1380)
    [<BarTime: Bar Time now, 1380-08-0212:12:12>]

⚠️ `__month` filter is not supported as explained in here_

Using Templatetags
------------------

1. You can use ``jformat`` filter to format your dates in templates:

.. code:: python

    {% load jformat %}
    {{ my_date|jformat }} {# default formatting #}
    {{ my_date|jformat:"%A %d %B %Y %H:%M" }} {# specific formatting #}

Admin Interface
---------------


1. Create foo/admin.py_

.. code:: python

    from foo.models import Bar, BarTime
    from django.contrib import admin

    from django_jalali.admin.filters import JDateFieldListFilter

    # You need to import this for adding jalali calendar widget
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


Django rest framework
---------------------

There are serializer fields corresponding to ``jmodels.JDateField`` and ``jmodels.JDateTimeField`` for DRF:


.. code:: python

    from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
    from rest_framework.serializers import ModelSerializer

    from foo.models import Bar, BarTime


    class JDateFieldSerialializer(ModelSerializer):
        date = JDateField()

        class Meta:
            model = Bar
            exclude = []

    class JDateTimeFieldSerializer(ModelSerializer):
        datetime = JDateTimeField()

        class Meta:
            model = BarTime
            exclude = []


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
    locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")

* If using Docker, add the following to your Dockerfile:

.. code:: dockerfile

    FROM python:3.11-slim-bookworm

    RUN apt-get update && apt-get -y install locales && \
     sed -i -e 's/# fa_IR UTF-8/fa_IR UTF-8/' /etc/locale.gen && \
     dpkg-reconfigure --frontend=noninteractive locales
   

Timezone Settings
-----------------
From *django_jalali* version 3 and *Django* 2 you can use ``TIME_ZONE`` and ``USE_TZ`` settings_ to save datetime with project timezone

Development
-----------

You can contribute to this project forking it from GitHub and sending pull requests.

First fork_ the repository_ and then clone it:

.. code:: shell

    $ git clone git@github.com:<you>/django-jalali.git

Initialize a virtual environment for development purposes:

.. code:: shell

    $ python -m venv django_jalali_env
    $ source ~/django_jalali_env/bin/activate

Then install the necessary requirements:

.. code:: shell

    $ cd django-jalali
    $ pip install -r requirements-test.txt

Unit tests are located in the ``tests`` folder and can be easily run with the pytest tool:

.. code:: shell

    $ pytest

Before committing, you can run all the above tests against all supported Python and Django versions with tox.
You need to install tox first:

.. code:: shell

    $ pip install tox

And then you can run all tests:

.. code:: shell

    $ tox

If you wish to limit the testing to specific environment(s), you can parametrize the tox run:

.. code:: shell

    $ tox -e py39-django42

To add a new value to the Jalali settings, just add its default value to the ``DEFAULTS`` dictionary located in ``django_jalali/setting.py``.

You can access the new setting in your code as shown below:

.. code-block:: python

    from django_jalali.settings import jalali_settings

    custom_settings = jalali_settings.CUSTOM_SETTINGS

.. _jdatetime: https://github.com/slashmili/python-jalali
.. _Django: https://www.djangoproject.com/
.. _settings.py: https://github.com/slashmili/django-jalali/blob/master/jalali_test/jalali_test/settings.py#L40
.. _models.py: https://github.com/slashmili/django-jalali/blob/master/jalali_test/foo/models.py
.. _admin.py: https://github.com/slashmili/django-jalali/blob/master/jalali_test/foo/admin.py
.. _settings: https://github.com/slashmili/django-jalali/blob/master/jalali_test/jalali_test/settings.py#L116
.. _Django REST Framework: https://www.django-rest-framework.org/
.. _fork: https://help.github.com/en/articles/fork-a-repo
.. _repository: https://github.com/slashmili/django-jalali
.. _here: https://github.com/slashmili/django-jalali/issues/142#issuecomment-887464050
