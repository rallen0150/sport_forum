# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#For Token
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    username = models.OneToOneField('auth.User')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.FileField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.username)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "http://gtalogo.com/img/6753.png"

    @receiver(post_save, sender=User)
    def create(**kwargs):
        created = kwargs['created']
        instance = kwargs['instance']
        if created:
            Profile.objects.create(user=instance)


class Sport(models.Model):
    sport = models.CharField(max_length=100, unique=True)
    abbrev = models.CharField(max_length=10, unique=True)
    img = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.abbrev)

    @property
    def img_url(self):
        if self.img:
            return self.img.url
        return "http://alexedmans.com/wp-content/uploads/2017/03/Sports.jpg"


class Team(models.Model):
    team_name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=10)
    logo = models.FileField(null=True, blank=True)
    sport = models.ForeignKey(Sport)

    def __str__(self):
        return str(self.abbrev)

    @property
    def img_url(self):
        if self.img:
            return self.img.url
        return "http://africavoip.co/wp-content/uploads/2017/10/team-logo-design-ideas-89-best-sports-logos-images-on-pinterest-sports-logos-sport-ideas.jpg"


class Topic(models.Model):
    writer = models.ForeignKey('auth.User')
    topic = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    team_topic = models.ForeignKey(Team)

    def __str__(self):
        return self.topic

    def get_comment(self):
        return Comment.objects.filter(topic=self)


class Comment(models.Model):
    commenter = models.ForeignKey('auth.User')
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey('app.Topic')

    def __str__(self):
        return self.comment

    def get_comment(self):
        return Reply.objects.filter(comment=self)

class Reply(models.Model):
    replier = models.ForeignKey('auth.User')
    reply = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment)

    def __str__(self):
        return self.reply
