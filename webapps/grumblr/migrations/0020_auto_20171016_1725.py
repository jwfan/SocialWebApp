# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 17:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0019_auto_20171006_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='following',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='follower_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Following',
        ),
    ]
