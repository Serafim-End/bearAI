# coding: utf-8
from django.db import DataError

from base_storage_adapter import BaseStorageAdapter
from ...task import Task


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

    def get_task(self):
        """
        get task object from Session table
        task object - task.Task
        :return:
        """
        return Task()

    def set_task(self, task):
        """
        write current task to Session table
        :param task:
        :return: True if task was written else False
        """
        pass
