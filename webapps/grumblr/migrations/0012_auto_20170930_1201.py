# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import grumblr.models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0011_auto_20170930_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[grumblr.models.tele_validate]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
