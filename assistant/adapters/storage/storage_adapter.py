# coding: utf-8

import json

from django.db import DataError

from .base_storage_adapter import BaseStorageAdapter
from ...conversation.models import Statement
from ...task import Task

from session.models import CustomerSession
from session.models import Session


class StorageAdapter(BaseStorageAdapter):
    """
    there django class can be used as models
    """

    def save(self, cls, **kwargs):
        cls = self.get_class(cls)

        instance = cls(**kwargs)
        try:
            if instance.is_valid():
                return instance.save()
        except DataError:
            pass  # Запись слишком длинная.

        raise BaseStorageAdapter.SerializerException(
            msg='Instance was not saved'
        )

    def get_task(self, customer):
        """
        get task object from Session table
        task object - task.Task
        :param customer: which task to process
        :return:
        """

        t = Task()

        statement = Statement.objects.filter(customer=customer).last()

        if not statement:
            return t

        c_session = CustomerSession.objects.filter(customer=customer).last()
        if not c_session.session.is_active:
            return t

        try:
            parameters = json.loads(c_session.session.parameters)
        except:
            parameters = []

        t.parameters = parameters

        t.intent = c_session.session.intent
        t.domain = t.intent.domain
        return t

    def set_task(self, task, customer):
        """
        write current task to Session table
        :param task:
        :return: True if task was written else False
        """
        if not task or not customer:
            return False

        c_s = CustomerSession.objects.filter(customer=customer).last()
        if not c_s:
            return False

        s = Session() if not c_s.session.is_active else c_s.session

        if task.parameters:
            s.parameters = json.dumps(task.parameters)

        s.is_active = task.status
        s.save()
        c_s.session = s
        c_s.save()

        return True
