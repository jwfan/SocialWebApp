# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0017_auto_20171002_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='/media/profile-images/noprofile.jpg', upload_to='profile-images'),
        ),
    ]
