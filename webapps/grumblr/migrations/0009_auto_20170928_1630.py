# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0008_auto_20170920_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='introduction',
            field=models.TextField(max_length=420),
        ),
    ]