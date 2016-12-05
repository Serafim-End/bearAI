# coding: utf-8

import json

from django.db import DataError

from .base_storage_adapter import BaseStorageAdapter
from ...conversation.models import Statement
from ...task import Task

from session.models import CustomerSession


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

        c_session = CustomerSession.objects.filter(customer=customer).last()
        if not c_session:
            return False

        session = c_session.session

        is_active = True
        unknown_pars = []

        for parameter in task.parameters:
            for k, v in parameter.iteritems():
                if k == 'is_obligatory':
                    continue
                if not v and parameter.get('is_obligatory'):
                    unknown_pars.append(k)

        if len(unknown_pars) == 0:
            is_active = False

        session.parameters = json.dumps(task.parameters)
        session.is_active = is_active
        session.save()
        return True
