# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0014_auto_20171001_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='/media/grumblr/images/noprofile.jpg', max_length=200, upload_to='profile-images'),
        ),
    ]