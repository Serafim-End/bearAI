# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from agent.models import Agent


@python_2_unicode_compatible
class Customer(models.Model):

    agent = models.ForeignKey(Agent)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def __str__(self):
        return '{}{}'.format(self.username, self.email)
