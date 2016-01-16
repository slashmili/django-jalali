# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date', django_jalali.db.models.jDateField()),
            ],
        ),
        migrations.CreateModel(
            name='BarTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('datetime', django_jalali.db.models.jDateTimeField()),
            ],
        ),
    ]
