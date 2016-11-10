from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from agent.models import Agent


@python_2_unicode_compatible
class Domain(models.Model):

    agent = models.ForeignKey(Agent)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DomainData(models.Model):

    domain = models.ForeignKey(Domain)

    def __str__(self):
        return ', '.join([d.name for d in self.domain])
