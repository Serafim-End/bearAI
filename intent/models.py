from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from domain.models import Domain


@python_2_unicode_compatible
class Intent(models.Model):

    domain = models.ForeignKey(Domain)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class IntentData(models.Model):
    intent = models.ForeignKey(Intent)
    text = models.TextField(default=None)

    def __str__(self):
        return ', '.join([i.name for i in self.intent])
