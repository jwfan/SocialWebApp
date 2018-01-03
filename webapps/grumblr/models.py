# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.db.models import Max
from django.utils.html import escape

# Data model for username
def tele_validate(value):
    telere = re.compile(r'^\(\d{3}\)\d{3}-\d{4}$')
    if not telere.match(value):
        raise ValidationError('Wrong telephone')


class Profile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to="profile-images", default='profile-images/noprofile.jpg', blank=True)
    introduction = models.TextField(max_length=420, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=20, validators=[tele_validate, ], null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    follower = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='follower_set')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.__unicode__()


class Post(models.Model):
    content = models.TextField(max_length=42)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField('post time', auto_now_add=True)

    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_posts(user):
        return Post.objects.filter(user=user).order_by('-timestamp')

    @staticmethod
    def get_changes(time="1970-01-01 00:00:00.000000+00:00"):
        return Post.objects.filter(timestamp__gt=time).distinct().order_by('timestamp')

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('timestamp'))['timestamp__max'] or "1970-01-01 00:00:00.000000+00:00"

    @staticmethod
    def get_from_id(post_id):
        if Post.objects.filter(id=post_id).exists():
            return Post.objects.get(id=post_id)
        else:
            return None

    @staticmethod
    def get_followchanges(user,time="1970-01-01 00:00:00.000000+00:00"):
        return Post.objects.filter(user__in=user.profile.follower.all(),timestamp__gt=time).distinct().order_by('timestamp')

class Comment(models.Model):
    content = models.TextField(max_length=42)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField('comment time', auto_now_add=True)

    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_comments(post):
        return Comment.objects.filter(post=post).order_by('timestamp')

    @staticmethod
    def get_changes(time="1970-01-01 00:00:00.000000+00:00"):
        return Comment.objects.filter(timestamp__gt=time).distinct().order_by('timestamp')

    @staticmethod
    def get_followchanges(posts,time="1970-01-01 00:00:00.000000+00:00"):
        return Comment.objects.filter(post__in=posts,timestamp__gt=time).distinct().order_by('timestamp')

    @staticmethod
    def get_max_time():
        return Comment.objects.all().aggregate(Max('timestamp'))['timestamp__max'] or "1970-01-01 00:00:00.000000+00:00"