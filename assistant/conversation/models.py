from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

from domain.models import Domain
from customer.models import Customer
from intent.models import Intent


@python_2_unicode_compatible
class Statement(models.Model):

    domain = models.ForeignKey(Domain, default=None)
    intent = models.ForeignKey(Intent, default=None)
    customer = models.ForeignKey(Customer)
    message = models.CharField(
        max_length=300,
        blank=False,
    )

    def __str__(self):
        return self.message


@python_2_unicode_compatible
class Response(models.Model):
    statement = models.ForeignKey('Statement', related_name='in_response_to')
    response = models.ForeignKey('Statement', related_name='+')

    unique_together = (('statement', 'response'),)

    def __str__(self):
        return '{} -> {}'.format(self.statement.text, self.response.text)
