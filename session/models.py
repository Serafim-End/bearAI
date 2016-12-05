# coding: utf-8

from __future__ import unicode_literals

import json

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from intent.models import Intent
from slots.models import Parameter


@python_2_unicode_compatible
class Session(models.Model):

    intent = models.ForeignKey(Intent)
    is_active = models.BooleanField()
    parameters = models.TextField(default=None)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def param_dict(self, parameter):
        param_dict = {
            'is_obligatory': parameter.is_obligatory,
            '{}'.format(parameter.name): ''
        }
        return param_dict

    def load_parameters(self):
        parameters = Parameter.objects.filter(intent=self.intent)
        param_list = [self.param_dict(parameter) for parameter in parameters]
        self.parameters = json.dumps(param_list)

    def __str__(self):
        return '{}'.format(self.parameters)
# Create your models here.
