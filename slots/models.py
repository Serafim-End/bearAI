from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

from intent.models import Intent


@python_2_unicode_compatible
class Parameter(models.Model):

    intent = models.ForeignKey(Intent)
    is_obligatory = models.BooleanField()
    name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        pass


@python_2_unicode_compatible
class ParameterData(models.Model):

    parameter = models.ForeignKey(Parameter)

    def __str__(self):
        pass
