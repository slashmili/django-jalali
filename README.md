Django Jalali
=============
This module gives you a DateField same as Django's DateField but you can get and query data based on Jalali Date

Dependencies
------------
* [.jdatetime](http://pypi.python.org/pypi/jdatetime/) -- easy_install jdatetime
* [.Django](https://www.djangoproject.com/) -- easy_install django

Install
-------

    easy_install django_jalali

Usage
-----

### Direct Usage

1. Run : 

    $ django-admin.py startproject jalali_test

2. Start your app :

    $ python manage.py startapp foo

3. Edit settings.py and add django_jalali and your foo to your INSTALLED_APPS (also config DATABASES setting)

4. Edit foo/models.py 

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
    $ python manage.py syncdb

6. Test it
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
    >>> Bar.objects.filter(date='1363-08-01')
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

Admin Interface 
---------------

1. Create foo/admin.py

    from foo.models import Bar,BarTime
    from django.contrib import admin
    import django_jalali.admin.filterspecs #you need to import this for adding filter in admin interface
    import django_jalali.admin as jadmin #you need import this for adding jalali calander widget

    class BarAdmin(admin.ModelAdmin):
        list_filter = ['date']

    admin.site.register(Bar, BarAdmin)

    class BarTimeAdmin(admin.ModelAdmin):
        list_filter = ['datetime']

    admin.site.register(BarTime, BarTimeAdmin)

2. Config admin interface and fire up your django and enjoy using jalali date !
