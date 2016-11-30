from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from developer.models import Developer


@python_2_unicode_compatible
class Agent(models.Model):
    developer = models.ForeignKey(Developer)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    username = models.CharField(_('username'), max_length=150)

    REQUIRED_FIELDS = ['developer_id']

    def __str__(self):
        return self.developer_id
