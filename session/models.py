# coding: utf-8

from __future__ import unicode_literals

import json

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from customer.models import Customer
from intent.models import Intent
from domain.models import Domain
from slots.models import Parameter


@python_2_unicode_compatible
class Session(models.Model):
    # miserable default values, refactor it

    domain = models.ForeignKey(
        Domain, default=lambda: Domain.objects.get(id=1)
    )

    intent = models.ForeignKey(
        Intent, default=lambda: Intent.objects.get(id=1)
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        default=lambda: Customer.objects.get(id=1)
    )

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


@python_2_unicode_compatible
class CustomerSession(models.Model):

    customer = models.ForeignKey(Customer)
    session = models.ForeignKey(Session)

    def __str__(self):
        return '{}'.format(self.customer.username)
