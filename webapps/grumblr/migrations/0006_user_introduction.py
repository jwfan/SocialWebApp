# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20170918_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='introduction',
            field=models.TextField(default='Welcome to my grumblr page!'),
        ),
    ]