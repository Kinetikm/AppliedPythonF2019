# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-06 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0004_auto_20191106_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aircraft',
            name='id',
        ),
        migrations.RemoveField(
            model_name='airport',
            name='id',
        ),
        migrations.AlterField(
            model_name='aircraft',
            name='aircraft_type',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name=b'airport name'),
        ),
        migrations.AlterField(
            model_name='airport',
            name='airport_name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name=b'airport name'),
        ),
    ]
