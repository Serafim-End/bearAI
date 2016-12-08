# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from agent.models import Agent


class Customer(User):
    """
    here possible to user inheritance of User class
    """
    # agent = models.ForeignKey(Agent)
    pass
