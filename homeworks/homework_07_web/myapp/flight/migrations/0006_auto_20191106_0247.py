# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-06 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0005_auto_20191106_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='aircraft_type',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name=b'airport name'),
        ),
        migrations.AlterField(
            model_name='airport',
            name='airport_name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name=b'airport name'),
        ),
        migrations.AlterModelTable(
            name='aircraft',
            table=None,
        ),
        migrations.AlterModelTable(
            name='airflight',
            table=None,
        ),
        migrations.AlterModelTable(
            name='airport',
            table=None,
        ),
    ]
