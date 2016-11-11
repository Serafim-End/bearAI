from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Developer(User):
    """
    here possible to user inheritance of User class
    """
    account_status = models.CharField(
        choices=(
            ('LO', 'LOW'),
            ('ST', 'STANDART'),
            ('EX', 'EXPENSIVE'),
        )
    )
