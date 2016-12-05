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

        parameters = json.loads(c_session.session.parameters)
        for k, v in parameters.iteritems():
            # Example of vocabulary
            # {'key1': {'value': 'some_value', 'is_obligatory': True}}
            # k - 'key1' and v - {'value': 'some_value', 'is_obligatory': True}
            t.parameters[k] = v

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

        is_active = False
        if task.parameters:
            s.parameters = json.dumps(task.parameters)

            while not is_active and task.parameters:
                k, v = task.parameters.popitem()
                if task.parameters[k]['value'] is None:
                    is_active = True

        s.is_active = is_active
        s.save()

        return True
